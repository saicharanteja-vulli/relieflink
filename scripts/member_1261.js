// Divya (1261) - read-only member demonstration
const project = db.getSiblingDB('relieflink_logistics');
print('My collections'); printjson(project.getCollectionNames());
print('Sample document'); printjson(project.stock_batches.findOne());
print('Count'); print(project.stock_batches.countDocuments());
print('Sorted sample'); printjson(project.stock_batches.find({record_version:1},{_id:1,quality_state:1,quantity_available:1}).sort({quantity_available:-1}).limit(5).toArray());
print('Grouped report'); printjson(project.stock_batches.aggregate([
 {$group:{_id:'$quality_state',records:{$sum:1},total:{$sum:'$quantity_available'}}},
 {$sort:{total:-1,_id:1}}
]).toArray());
print('Local relationship'); printjson(project.stock_batches.aggregate([
 {$lookup:{from:'items',localField:'item_id',foreignField:'_id',as:'related'}},
 {$project:{_id:1,item_id:1,related:1}},{$limit:1}
]).toArray());
