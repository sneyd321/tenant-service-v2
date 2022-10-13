from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update, delete
from sqlalchemy.future import select
from models.models import Tenant
from sqlalchemy import func


class DB:

    def __init__(self, user, password, host, database):
        self.engine = create_async_engine(f"mysql+aiomysql://{user}:{password}@{host}/{database}", echo=False, pool_pre_ping=True)
        Session = sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)
        self.session = Session()
        

    def get_session(self):
        return self.session
        

    async def get(self, data):
        result = await self.session.execute(select(Tenant).where(Tenant.id == data.id))
        return result.scalars().first()


    async def get_by_house_id(self, data):
        result = await self.session.execute(select(Tenant).where(Tenant.houseId == data.houseId))
        return result.scalars().all()

    
    async def get_emails(self, tenant):
        result = await self.session.execute(select(Tenant.email))
        return result.scalars().all()


    async def get_tenant_by_email(self, tenant):
        result = await self.session.execute(select(Tenant).where(Tenant.email == tenant.email))
        return result.scalars().first()


    async def count_tenants_in_house(self, tenant):
        result = await self.session.execute(select(func.count(Tenant.houseId)).where(Tenant.houseId == tenant.houseId))
        return result.scalars().first()


    async def insert(self, data):
        self.session.add(data)


    async def commit(self):
        await self.session.commit()
    

    async def rollback(self):
        await self.session.rollback()
    

    async def update(self, data):
        await self.session.execute(update(Tenant).where(Tenant.id == data.id).values(data.to_dict()))
       
       
    async def update_device_id(self, data):
        await self.session.execute(update(Tenant).where(Tenant.id == data.id).values(data.to_dict()))
