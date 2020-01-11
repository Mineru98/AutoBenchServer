import graphene
import pymongo
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Department as DepartmentModel
from models import Employee as EmployeeModel
from models import Role as RoleModel
from models import Task as TaskModel
from models import CPUInfo as CPUInfoModel
from models import GPUInfo as GPUInfoModel
from models import MainBoardInfo as MainBoardInfoModel
from models import RAMInfo as RAMInfoModel
from models import DiskDriveInfo as DiskDriveInfoModel

class CPU(MongoengineObjectType):
  class Meta:
    model = CPUInfoModel
    interfaces = (Node,)
    
class GPU(MongoengineObjectType):
  class Meta:
    model = GPUInfoModel
    interfaces = (Node,)

class RAM(MongoengineObjectType):
  class Meta:
    model = RAMInfoModel
    interfaces = (Node,)

class MainBoard(MongoengineObjectType):
  class Meta:
    model = MainBoardInfoModel
    interfaces = (Node,)
    
class DiskDrive(MongoengineObjectType):
  class Meta:
    model = DiskDriveInfoModel
    interfaces = (Node,)

class Department(MongoengineObjectType):
  class Meta:
    model = DepartmentModel
    interfaces = (Node,)


class Role(MongoengineObjectType):
  class Meta:
    model = RoleModel
    interfaces = (Node,)


class Task(MongoengineObjectType):
  class Meta:
    model = TaskModel
    interfaces = (Node,)


class Employee(MongoengineObjectType):
  class Meta:
    model = EmployeeModel
    interfaces = (Node,)

class Query(graphene.ObjectType):
  node = Node.Field()
  all_employees = MongoengineConnectionField(Employee)
  all_roles = MongoengineConnectionField(Role)
  all_cpu = MongoengineConnectionField(CPU)
  all_gpu = MongoengineConnectionField(GPU)
  all_mainboard = MongoengineConnectionField(MainBoard)
  all_diskdrive = MongoengineConnectionField(DiskDrive)
  cpu = graphene.Field(CPU, rank=graphene.Int(required=False))
  cpu_socket = graphene.List(CPU, socket=graphene.String(required=False))
  gpu = graphene.Field(GPU, rank=graphene.Int(required=False))
  diskdrive = graphene.Field(DiskDrive, rank=graphene.Int(required=False))
  mainboard = graphene.Field(MainBoard, model_name=graphene.String(required=False))
  mainboard_socket = graphene.List(MainBoard, socket=graphene.String(required=False))

  def resolve_cpu(parent, info, rank):
    myclient = pymongo.MongoClient("mongodb://localhost/autobench")
    document = myclient["autobench"]
    results = document["cpu"].find({"rank": rank})
    return CPUInfoModel(rank=results[0]['rank'], model_name=results[0]['model_name'],score=results[0]['score'],socket=results[0]['socket'],chipset=results[0]['chipset'],manufacturer=results[0]['manufacturer'])
  
  def resolve_cpu_socket(parent, info, socket):
    myclient = pymongo.MongoClient("mongodb://localhost/autobench")
    document = myclient["autobench"]
    results = document["cpu"].find({"socket": socket})
    list = []
    for i in results:
      list.push(CPUInfoModel(rank=i['rank'], model_name=i['model_name'],score=i['score'],socket=i['socket'],chipset=i['chipset'],manufacturer=i['manufacturer']))
    print(len(list))
    return list
  
  def resolve_gpu(parent, info, rank):
    myclient = pymongo.MongoClient("mongodb://localhost/autobench")
    document = myclient["autobench"]
    results = document["gpu"].find({"rank": rank})
    return GPUInfoModel(rank=results[0]['rank'], model_name=results[0]['model_name'],score=results[0]['score'],slot_type=results[0]['slot_type'],manufacturer=results[0]['manufacturer'])
  
  def resolve_diskdrive(parent, info, rank):
    myclient = pymongo.MongoClient("mongodb://localhost/autobench")
    document = myclient["autobench"]
    results = document["diskdrive"].find({"rank": rank})
    return DiskDriveInfoModel(rank=results[0]['rank'], model_name=results[0]['model_name'],score=results[0]['score'])
  
  def resolve_mainboard(parent, info, model_name):
    myclient = pymongo.MongoClient("mongodb://localhost/autobench")
    document = myclient["autobench"]
    results = document["mainboard"].find({"model_name": model_name})
    return MainBoardInfoModel(model_name=results[0]['model_name'],score=results[0]['score'],socket=results[0]['socket'],chipset=results[0]['chipset'],manufacturer=results[0]['manufacturer'])
  
  def resolve_mainboard_socket(parent, info, socket):
    myclient = pymongo.MongoClient("mongodb://localhost/autobench")
    document = myclient["autobench"]
    print(socket)
    results = document["mainboard"].find({"socket": socket})
    list = []
    for i in results:
      list.append(MainBoardInfoModel(model_name=i['model_name'],manufacturer=i['manufacturer'],socket=i['socket'],chipset=i['chipset']))
    return list

schema = graphene.Schema(query=Query, types=[Department, Employee, Role, CPU, GPU, RAM, DiskDrive, MainBoard])