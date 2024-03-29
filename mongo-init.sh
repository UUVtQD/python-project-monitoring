#!/bin/bash
set -e

mongosh <<EOF
db = db.getSiblingDB('monitoring')

db.createUser({
  user: 'monitoring',
  pwd: 'monitoring',
  roles: [{ role: 'readWrite', db: 'monitoring' }],
});
db.createCollection('records')

EOF