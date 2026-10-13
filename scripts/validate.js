const fs=require('fs'),path=require('path');
const root=process.env.RELIEFLINK_ROOT||process.cwd();
const manifest=JSON.parse(fs.readFileSync(path.join(root,'manifest.json'),'utf8'));
const selected=process.env.RELIEFLINK_DB;
if(selected&&!manifest.databases.some(d=>d.name===selected)) throw Error('Unknown RELIEFLINK_DB');
let failures=[],rows=[],referenceChecks=0;
function check(ok,msg){if(!ok)failures.push(msg);}
for(const d of manifest.databases.filter(d=>!selected||d.name===selected)){
 const target=db.getSiblingDB(d.name);check(target.getCollectionNames().length>=10,d.name+': fewer than 10 collections');
 for(const c of d.collections){
  const coll=target.getCollection(c.name),docs=coll.find().toArray();
  const minFields=docs.length?Math.min(...docs.map(x=>Object.keys(x).filter(k=>k!=='_id').length)):0;
  check(docs.length>=50,d.name+'.'+c.name+': fewer than 50 documents');check(minFields>=10,d.name+'.'+c.name+': fewer than 10 fields');
  check(coll.countDocuments({$nor:[{$jsonSchema:c.schema}]})===0,d.name+'.'+c.name+': schema mismatch');
  for(const r of c.references){
   // With a single-member installation, external databases are optional.
   if(selected&&r.database!==d.name)continue;
   const ids=new Set(db.getSiblingDB(r.database).getCollection(r.collection).find({}, {_id:1}).toArray().map(x=>x._id));
   for(const doc of docs){referenceChecks++;check(ids.has(doc[r.field]),c.name+': broken reference '+r.field);}
  }
  rows.push({database:d.name,collection:c.name,documents:docs.length,minFieldsExcludingId:minFields});
 }
}
if(!selected){
 const s=db.getSiblingDB('relieflink_shelters'),l=db.getSiblingDB('relieflink_logistics'),f=db.getSiblingDB('relieflink_donations');
 for(const x of s.occupancy_snapshots.find().toArray()){
  const sh=s.shelters.findOne({_id:x.shelter_id});
  const admitted=s.admissions.aggregate([{$match:{shelter_id:x.shelter_id,admission_state:'active'}},{$group:{_id:null,n:{$sum:'$people_admitted'}}}]).toArray()[0]?.n||0;
  check(x.people_present===admitted&&x.people_present<=sh.capacity_people&&x.available_places===sh.capacity_people-admitted,'Occupancy mismatch '+x._id);
 }
 for(const x of l.stock_batches.find().toArray()){
  const shipped=l.shipments.aggregate([{$match:{batch_id:x._id}},{$group:{_id:null,n:{$sum:'$quantity'}}}]).toArray()[0]?.n||0;
  check(x.quantity_available===x.quantity_received-shipped&&x.quantity_available>=0,'Stock balance '+x._id);
 }
 for(const x of l.purchase_orders.find().toArray())check(x.total_inr===x.quantity*x.unit_price_inr,'Order arithmetic '+x._id);
 for(const x of f.donations.find().toArray()){
  const allocations=f.allocations.find({donation_id:x._id}).toArray();check(allocations.reduce((s,a)=>s+a.amount_inr,0)<=x.amount_inr,'Donation overspent '+x._id);
  for(const a of allocations)check(f.expenses.find({allocation_id:a._id}).toArray().reduce((s,e)=>s+e.amount_inr,0)<=a.amount_inr,'Allocation overspent '+a._id);
 }
}
const result={passed:failures.length===0,databases:new Set(rows.map(x=>x.database)).size,collections:rows.length,documents:rows.reduce((s,x)=>s+x.documents,0),referenceChecks,rows,failures};
print(JSON.stringify(result,null,2));
if(failures.length)throw Error('Validation failed');
