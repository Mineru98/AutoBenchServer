from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField,
    ListField, ReferenceField, StringField, ImageField, IntField
)

class CPUInfo(Document):
  meta = {'collection': 'cpu'}
  rank = IntField()
  model_name = StringField()
  score = IntField()
  socket = StringField()
  chipset = StringField()
  manufacturer = StringField()
  model_image = ImageField()

class GPUInfo(Document):
  meta = {'collection': 'gpu'}
  rank = IntField()
  model_name = StringField()
  score = IntField()
  slot_type = StringField()
  manufacturer = StringField()
  model_image = ImageField()
  
class MainBoardInfo(Document):
  meta = {'collection': 'mainboard'}
  model_name = StringField()
  manufacturer = StringField()
  socket = StringField()
  formfactor = StringField()
  chipset = StringField()
  memory_count = IntField()
  memory_type = IntField()
  memory_max_speed = IntField()
  memory_max_capacity = IntField()
  # ... usb / pci / m2 / multi gpu support
  model_image = ImageField()
  
class RAMInfo(Document):
  meta = {'collection': 'ram'}
  model_name = StringField()
  manufacturer = StringField()
  memory_type = IntField()
  latency = IntField()
  read_speed = IntField()
  write_speed = IntField()
  model_image = ImageField()

class DiskDriveInfo(Document):
  meta = {'collection': 'diskdrive'}
  rank = IntField()
  model_name = StringField()
  score = IntField()
  manufacturer = StringField()
  model_image = ImageField()

class Department(Document):
  meta = {'collection': 'department'}
  name = StringField()

class Role(Document):
  meta = {'collection': 'role'}
  name = StringField()

class Task(EmbeddedDocument):
  name = StringField()
  deadline = DateTimeField(default=datetime.now)

class Employee(Document):
  meta = {'collection': 'employee'}
  name = StringField()
  hired_on = DateTimeField(default=datetime.now)
  department = ReferenceField(Department)
  roles = ListField(ReferenceField(Role))
  leader = ReferenceField('Employee')
  tasks = ListField(EmbeddedDocumentField(Task))