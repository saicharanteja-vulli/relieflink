// Adithya (1259) - read-only member demonstration
const project = db.getSiblingDB('relieflink_rescue');
print('My collections'); printjson(project.getCollectionNames());
print('Sample document'); printjson(project.requests.findOne());
print('Count'); print(project.requests.countDocuments());
print('Sorted sample'); printjson(project.requests.find({record_version:1},{_id:1,priority:1,people_count:1}).sort({people_count:-1}).limit(5).toArray());
print('Grouped report'); printjson(project.requests.aggregate([
 {$group:{_id:'$priority',records:{$sum:1},total:{$sum:'$people_count'}}},
 {$sort:{total:-1,_id:1}}
]).toArray());
print('Local relationship'); printjson(project.requests.aggregate([
 {$lookup:{from:'teams',localField:'team_id',foreignField:'_id',as:'related'}},
 {$project:{_id:1,team_id:1,related:1}},{$limit:1}
]).toArray());
