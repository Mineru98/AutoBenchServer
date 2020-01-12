# AutoBenchServer

```python
nohup python -u scheduler.py & # Background Process
ps -ef | grep {filename} # Search Process ID
kill {process id} # Exit Process
```

```python
db.createCollection("user", { capped: true, size: 6142800, max: 10000 })
db.createCollection("cpu", { capped: true, size: 6142800, max: 10000 })
db.createCollection("gpu", { capped: true, size: 6142800, max: 10000 })
db.createCollection("ram", { capped: true, size: 6142800, max: 10000 })
db.createCollection("mainboard", { capped: true, size: 6142800, max: 10000 })
db.createCollection("diskdrive", { capped: true, size: 6142800, max: 10000 })
```
[참고자료](https://www.roytuts.com/python-flask-rest-api-mongodb-crud-example/)