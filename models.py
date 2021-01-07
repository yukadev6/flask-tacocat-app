from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('taco.db')

class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField(max_length=100)
    
    class Meta:
        database = DATABASE
        
    def get_tacos(self):
        return Taco.select().where(Taco.user == self)
    
    
    @classmethod
    def create_user(cls, email, password):
        try:
            cls.create(email=email, password=generate_password_hash(password))              
        except IntegrityError:
            raise ValueError("Email already exists.")    

            
class Taco(Model):
    protein = CharField()
    shell = CharField()
    cheese = BooleanField(default=False)
    extras = CharField()
    user = ForeignKeyField(rel_model=User, related_name='tacos')
    
    class Meta:
        database = DATABASE
        
    @classmethod
    def create_taco(cls, protein, shell, cheese, extras, user):
        with DATABASE.transaction():
                cls.create(
                    protein=protein,
                    shell=shell,
                    cheese=cheese,
                    extras=extras,
                    user=user
                )

                
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Taco], safe=True)
    DATABASE.close()    