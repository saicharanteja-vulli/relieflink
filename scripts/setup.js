// Run from the ReliefLink folder: mongosh "mongodb://127.0.0.1:27017" --file scripts/setup.js
const fs = require('fs'), path = require('path');
const root = process.env.RELIEFLINK_ROOT || process.cwd();
const manifest = JSON.parse(fs.readFileSync(path.join(root,'manifest.json'),'utf8'));
const selected = process.env.RELIEFLINK_DB;
const targets=manifest.databases.filter(d=>!selected||d.name===selected);
if(!targets.length) throw Error('RELIEFLINK_DB must match a database in manifest.json');
// Preflight all targets before writing. Refuse to overwrite any existing collection.
for (const d of targets) if(db.getSiblingDB(d.name).getCollectionNames().length) throw Error(d.name+' already contains collections. Use a fresh server or a backup; setup never overwrites data.');
for(const d of targets){
 const target=db.getSiblingDB(d.name);
 for(const c of d.collections){
  target.createCollection(c.name,{validator:{$jsonSchema:c.schema},validationLevel:'strict',validationAction:'error'});
  const docs=EJSON.parse(fs.readFileSync(path.join(root,'data',d.name,c.name+'.json'),'utf8'));
  target.getCollection(c.name).insertMany(docs);
  for(const r of c.references) target.getCollection(c.name).createIndex({[r.field]:1});
  print(d.name+'.'+c.name+': '+docs.length+' documents');
 }
}
if(!selected||selected==='relieflink_rescue') db.getSiblingDB('relieflink_rescue').requests.createIndex({priority:1,reported_at:-1});
print('SETUP COMPLETE');
