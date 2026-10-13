// Each CRUD cycle creates and removes only its own temporary record.
const fs=require('fs'),path=require('path');
const manifest=JSON.parse(fs.readFileSync(path.join(process.env.RELIEFLINK_ROOT||process.cwd(),'manifest.json'),'utf8'));
const reports={
 incidents:['events',[{$group:{_id:'$disaster_type',events:{$sum:1},affectedPeople:{$sum:'$affected_people'}}},{$sort:{events:-1,_id:1}}]],
 rescue:['requests',[{$group:{_id:'$priority',requests:{$sum:1},people:{$sum:'$people_count'}}},{$sort:{_id:1}}]],
 shelters:['admissions',[{$lookup:{from:'shelters',localField:'shelter_id',foreignField:'_id',as:'shelter'}},{$unwind:'$shelter'},{$project:{_id:0,shelter:'$shelter.shelter_name',people:'$people_admitted',capacity:'$shelter.capacity_people'}},{$limit:5}]],
 logistics:['stock_batches',[{$lookup:{from:'items',localField:'item_id',foreignField:'_id',as:'item'}},{$unwind:'$item'},{$group:{_id:'$item.category',availableUnits:{$sum:'$quantity_available'}}},{$sort:{_id:1}}]],
 volunteers:['assignments',[{$group:{_id:'$role',assignments:{$sum:1},plannedHours:{$sum:'$hours_planned'}}},{$sort:{_id:1}}]],
 donations:['donations',[{$group:{_id:'$payment_method',donations:{$sum:1},totalINR:{$sum:'$amount_inr'}}}]]
};
for(const d of manifest.databases.filter(d=>!process.env.RELIEFLINK_DB||d.name===process.env.RELIEFLINK_DB)){
 print('\n'+d.member+' ('+d.roll+') - '+d.name);
 const target=db.getSiblingDB(d.name),coll=target.getCollection(d.collections[0].name);
 const original=coll.findOne(), temp={...original,_id:'DEMO-'+Date.now()+'-'+d.key};
 try{
  coll.insertOne(temp);if(!coll.findOne({_id:temp._id}))throw Error('Create/read failed');
  coll.updateOne({_id:temp._id},{$set:{record_version:2}});if(coll.findOne({_id:temp._id}).record_version!==2)throw Error('Update failed');
 }finally{coll.deleteOne({_id:temp._id});}
 if(coll.findOne({_id:temp._id}))throw Error('Delete failed');print('CRUD PASS: created, read, updated, deleted temporary record');
 const bad={...original,_id:'INVALID-'+Date.now()};delete bad[d.collections[0].fields[1]];
 let rejected=false;try{coll.insertOne(bad);}catch(e){if(e.code===121)rejected=true;else throw e;}
 if(!rejected){coll.deleteOne({_id:bad._id});throw Error('Validator accepted invalid document');}print('SCHEMA PASS: incomplete document rejected');
 const [name,pipeline]=reports[d.key];print('AGGREGATION '+name);printjson(target.getCollection(name).aggregate(pipeline).toArray());
 print('FILTER / SORT / LIMIT');printjson(coll.find({record_version:1},{_id:1}).sort({_id:1}).limit(3).toArray());
}
print('ALL DEMOS PASSED');
