import json
import pymongo
from mongoengine import connect
from models import Department, Employee, Role, Task, CPUInfo, GPUInfo, MainBoardInfo, RAMInfo, DiskDriveInfo

connect('autobench', host='mongodb://localhost/autobench', alias='default')

# data load
with open('/workspace/AutoBenchServer/database/cpu/cpu.json','rb') as f:
  cpu_data = json.load(f)
with open('/workspace/AutoBenchServer/database/gpu/gpu_new.json','rb') as f:
  gpu_data = json.load(f)
with open('/workspace/AutoBenchServer/database/mainboard/mainboard.json','rb') as f:
  mainboard_data = json.load(f)
with open('/workspace/AutoBenchServer/database/drive/drive.json','rb') as f:
  drive_data = json.load(f)

def init_db(mode):
  if mode == 0:
    pass
  elif mode == 1:
    # Document Reset
    myclient = pymongo.MongoClient("mongodb://localhost/autobench")
    document = myclient["autobench"]
    document["cpu"].drop()
    document["gpu"].drop()
    document["ram"].drop()
    document["diskdrive"].drop()
    document["mainboard"].drop()
    
    # Create the fixtures
    for list in cpu_data:
      cpu = CPUInfo(rank=list['rank'],model_name=list['model_name'],score=list['score'],socket='BGA1288',chipset='HM55',manufacturer='intel')
      cpu.save()
    
    for list in gpu_data:
      gpu = GPUInfo(rank=list['rank'],model_name=list['model_name'],score=list['score'],slot_type=list['slot type'],manufacturer=list['manufacturer'])
      gpu.save()
      
    for list in mainboard_data:
      mainboard = MainBoardInfo(model_name=list['model_name'],socket=list['socket'],chipset=list['chipset'],manufacturer=list['manufacturer'])
      mainboard.save()
      
    for list in drive_data:
      drive = DiskDriveInfo(rank=list['rank'],model_name=list['model_name'],score=list['score'])
      drive.save()
  