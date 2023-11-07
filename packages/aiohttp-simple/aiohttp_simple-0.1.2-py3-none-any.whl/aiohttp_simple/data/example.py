from typing import List, Optional

from aiohttp import web
from aiohttp_simple.middlewares.db import mysql_stroage_engine
from aiohttp_simple.template.service import BaseService

routes = web.RouteTableDef()

import logging
from datetime import datetime

from aiohttp_simple import DbTableBase, Paginate, success_response
from aiohttp_simple.utils.log import Log
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.future import select

Log().init_log()

logger = logging.getLogger(__name__)


class User(DbTableBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    age = Column(Integer, nullable=False)
    mail = Column(String(32), nullable=False)
    phone = Column(String(32), nullable=True)


class UserModel(BaseModel):
    id: Optional[int] = None
    name: str
    age: Optional[int] = None
    mail: str
    phone: Optional[str] = None
    is_delete: Optional[bool] = None
    create_time: Optional[datetime] = None
    create_user: Optional[int] = None
    update_time: Optional[datetime] = None
    update_user: Optional[int] = None


class UserService(BaseService):
    async def add_user(self, user: UserModel):
        async with self.async_session() as session:
            async with session.begin():
                session.add(User.from_model(user))
                logger.info(f"add user {user}")

    async def get_user_list(self, paginate: Paginate):
        async with self.async_session() as session:
            base_sql = select(User).filter_by()
            sql, sql_total = self.generate_query(base_sql, paginate=paginate)

            userList = await session.execute(sql)
            userList_ = list(userList.scalars())
            count = await session.execute(sql_total)
            paginate.total_count = count.scalar()
            if len(userList_) == 0 and not count:
                paginate.current_page = 1
            return userList_


@routes.get("/get_user_list")
async def get_user_list(request: web.Request) -> web.Response:
    user_service = UserService(request=request)
    paginate = Paginate.model_validate(request.query)
    user_list = await user_service.get_user_list(paginate)
    return success_response(List[UserModel], user_list, paginate)


@routes.post("/add_user")
async def add_user(request: web.Request) -> web.Response:
    user_service = UserService(request=request)
    userInfo = await request.json()
    user = UserModel.model_validate(userInfo)
    await user_service.add_user(user)
    return success_response()


app = web.Application()


if __name__ == "__main__":
    app.add_routes(routes)
    app.cleanup_ctx.append(mysql_stroage_engine)
    web.run_app(app)
