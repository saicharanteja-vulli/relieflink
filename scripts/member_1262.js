// Harsha (1262) - read-only member demonstration
const project = db.getSiblingDB('relieflink_volunteers');
print('My collections'); printjson(project.getCollectionNames());
print('Sample document'); printjson(project.assignments.findOne());
print('Count'); print(project.assignments.countDocuments());
print('Sorted sample'); printjson(project.assignments.find({record_version:1},{_id:1,role:1,hours_planned:1}).sort({hours_planned:-1}).limit(5).toArray());
print('Grouped report'); printjson(project.assignments.aggregate([
 {$group:{_id:'$role',records:{$sum:1},total:{$sum:'$hours_planned'}}},
 {$sort:{total:-1,_id:1}}
]).toArray());
print('Local relationship'); printjson(project.assignments.aggregate([
 {$lookup:{from:'profiles',localField:'volunteer_id',foreignField:'_id',as:'related'}},
 {$project:{_id:1,volunteer_id:1,related:1}},{$limit:1}
]).toArray());
