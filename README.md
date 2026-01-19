# Run MongoDB as replica set (required for transactions)

```
docker compose up -d
docker exec -it $(docker ps -q --filter name=mongo) mongosh --eval 'rs.initiate({_id:"rs0",members:[{_id:0,host:"localhost:27017"}]})'
pytest -q
```
