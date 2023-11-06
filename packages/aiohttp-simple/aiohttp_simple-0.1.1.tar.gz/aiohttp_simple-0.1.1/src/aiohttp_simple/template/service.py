from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from aiohttp_simple.template.data_model import Paginate


class BaseService:
    def __init__(self, request):
        self.request = request
        self.engine = self.request.app["mysql_stroage_engine"]

    @property
    def async_session(self):
        return sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    def generate_query(self, base_sql, paginate: Paginate):
        query_sql = base_sql.offset(paginate.offset).limit(paginate.limit)
        total_sql = select(func.count()).select_from(base_sql)
        return query_sql, total_sql
