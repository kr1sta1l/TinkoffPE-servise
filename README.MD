## Спридонов Дима БПИ214

### Процесс запуска всего этого добра:

* В директории `tools/database-dev/`: `docker-compose up`
* В директории `product_engine/`:

```
sudo docker run --rm --network="fintech-network" -v "$(pwd)/migrations":/app liquibase/liquibase:4.19.0 --defaultsFile=/app/dev.properties update
```

* В директории `product_engine/src/`:

```
sudo docker run --network="fintech-network" -d -p 8000:8000 product_engine:lastest
```

##### После этого по адресу: http://127.0.0.1:8000/... все(сервис PE) должно работать по документации