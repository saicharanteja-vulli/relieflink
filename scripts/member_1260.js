// Sreedhar (1260) - read-only member demonstration
const project = db.getSiblingDB('relieflink_shelters');
print('My collections'); printjson(project.getCollectionNames());
print('Sample document'); printjson(project.admissions.findOne());
print('Count'); print(project.admissions.countDocuments());
print('Sorted sample'); printjson(project.admissions.find({record_version:1},{_id:1,admission_state:1,people_admitted:1}).sort({people_admitted:-1}).limit(5).toArray());
print('Grouped report'); printjson(project.admissions.aggregate([
 {$group:{_id:'$admission_state',records:{$sum:1},total:{$sum:'$people_admitted'}}},
 {$sort:{total:-1,_id:1}}
]).toArray());
print('Local relationship'); printjson(project.admissions.aggregate([
 {$lookup:{from:'shelters',localField:'shelter_id',foreignField:'_id',as:'related'}},
 {$project:{_id:1,shelter_id:1,related:1}},{$limit:1}
]).toArray());
