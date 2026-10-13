// Mounica Sai (1267) - read-only member demonstration
const project = db.getSiblingDB('relieflink_donations');
print('My collections'); printjson(project.getCollectionNames());
print('Sample document'); printjson(project.donations.findOne());
print('Count'); print(project.donations.countDocuments());
print('Sorted sample'); printjson(project.donations.find({record_version:1},{_id:1,payment_method:1,amount_inr:1}).sort({amount_inr:-1}).limit(5).toArray());
print('Grouped report'); printjson(project.donations.aggregate([
 {$group:{_id:'$payment_method',records:{$sum:1},total:{$sum:'$amount_inr'}}},
 {$sort:{total:-1,_id:1}}
]).toArray());
print('Local relationship'); printjson(project.donations.aggregate([
 {$lookup:{from:'donors',localField:'donor_id',foreignField:'_id',as:'related'}},
 {$project:{_id:1,donor_id:1,related:1}},{$limit:1}
]).toArray());
