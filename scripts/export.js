const fs=require('fs'),path=require('path');
const root=process.env.RELIEFLINK_ROOT||process.cwd();
const manifest=JSON.parse(fs.readFileSync(path.join(root,'manifest.json'),'utf8'));
const dest=path.join(root,'exports',new Date().toISOString().replace(/[:.]/g,'-'));
for(const d of manifest.databases){
 fs.mkdirSync(path.join(dest,d.name),{recursive:true});
 for(const c of d.collections){
  const docs=db.getSiblingDB(d.name).getCollection(c.name).find().sort({_id:1}).toArray();
  fs.writeFileSync(path.join(dest,d.name,c.name+'.json'),EJSON.stringify(docs,null,2));
 }
}
print(dest);
