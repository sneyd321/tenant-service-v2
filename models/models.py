
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.exc import OperationalError, IntegrityError
import datetime
from passlib.context import CryptContext


Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Tenant(Base):
    __tablename__ = 'tenant'

    id = Column(Integer(), primary_key=True)
    houseId = Column(Integer(), nullable=False)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    tenantPosition = Column(Integer(), nullable=False)
    tenantState = Column(String(30), nullable=False)
    deviceId = Column(String(180), nullable=True)

    def __init__(self, houseId, tenantPosition, **kwargs):
        self.houseId = houseId
        self.firstName = kwargs.get("firstName")
        self.lastName = kwargs.get("lastName")
        self.email = kwargs.get("email")
        self.password = self.get_password_hash(kwargs.get("password"))
        self.tenantPosition = tenantPosition
        self.tenantState = kwargs.get("tenantState")
        self.deviceId = kwargs.get("deviceId", "")

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def to_json(self):
        return {
            "houseId": self.houseId,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "tenantState": self.tenantState,
            "tenantPosition": self.tenantPosition,
             "deviceId": self.deviceId
        }

    def to_dict(self):
        return {
            "houseId": self.houseId,
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "tenantState": self.tenantState,
            "deviceId": self.deviceId
        }
    

