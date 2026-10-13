# ReliefLink
### A MongoDB data model for disaster relief coordination

ReliefLink is an academic group project that connects incidents, rescue operations, shelters, donations, volunteers and logistics through a structured MongoDB dataset.

## At a glance
- **6 databases · 60 collections · 3,000 synthetic documents**
- Collection validators, indexes and cross-collection references
- CRUD demonstrations, aggregation reports and validation scripts
- Python generator for reproducible demonstration data

## Run locally
Install MongoDB Community Server and `mongosh`, start a local server, then run these commands from the repository root:

```sh
mongosh "mongodb://127.0.0.1:27017" --file scripts/setup.js
mongosh "mongodb://127.0.0.1:27017" --file scripts/validate.js
mongosh "mongodb://127.0.0.1:27017" --file scripts/demo.js
```

Setup refuses nonempty target databases. Use a fresh local server if setup was interrupted; it does not overwrite existing databases.

## Explore the project
| Folder | Contents |
|---|---|
| `data/` | Extended JSON seed data |
| `scripts/` | Setup, validation, queries and generator |
| `manifest.json` | Schemas, references and expected counts |
| `evidence/` | Saved validation results from the original project run |

## Scope
All records are fictional. This is a classroom database demonstration, not a deployed emergency response service. Production authentication, live integrations and multi-document transactions are not implemented. Saved validation evidence is historical, not a fresh database run.

## Credits
Created as a six-member academic group project. Module ownership is preserved in the manifest and member query scripts.
