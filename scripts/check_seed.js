const fs=require('fs'),path=require('path');
const root=process.env.RELIEFLINK_ROOT||process.cwd();
const m=JSON.parse(fs.readFileSync(path.join(root,'manifest.json'),'utf8'));
let checked=0;
for(const d of m.databases)for(const c of d.collections){
 const expected=EJSON.parse(fs.readFileSync(path.join(root,'data',d.name,c.name+'.json'),'utf8'));
 for(const x of expected){
  const got=db.getSiblingDB(d.name).getCollection(c.name).findOne({_id:x._id});
  if(EJSON.stringify(got)!==EJSON.stringify(x))throw Error('Seed mismatch '+x._id);
  checked++;
 }
}
print('PASS: '+checked+' live documents match the supplied seed files exactly.');
