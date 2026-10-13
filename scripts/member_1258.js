// Sai Charan Teja (1258) - read-only member demonstration
const project = db.getSiblingDB('relieflink_incidents');
print('My collections'); printjson(project.getCollectionNames());
print('Sample document'); printjson(project.events.findOne());
print('Count'); print(project.events.countDocuments());
print('Sorted sample'); printjson(project.events.find({record_version:1},{_id:1,disaster_type:1,affected_people:1}).sort({affected_people:-1}).limit(5).toArray());
print('Grouped report'); printjson(project.events.aggregate([
 {$group:{_id:'$disaster_type',records:{$sum:1},total:{$sum:'$affected_people'}}},
 {$sort:{total:-1,_id:1}}
]).toArray());
print('Local relationship'); printjson(project.events.aggregate([
 {$lookup:{from:'areas',localField:'area_id',foreignField:'_id',as:'related'}},
 {$project:{_id:1,area_id:1,related:1}},{$limit:1}
]).toArray());
