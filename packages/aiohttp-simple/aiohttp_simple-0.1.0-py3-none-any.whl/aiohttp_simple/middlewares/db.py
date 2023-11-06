
from __future__ import annotations

from aiohttp_simple.utils.setting import SETTING
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from aiohttp_simple.template.template import Base

async def mysql_stroage_engine(app):
    app['mysql_stroage_engine'] =  create_async_engine(SETTING.mysql_url, echo=True)
    engine = app['mysql_stroage_engine']
    for subapp in app._subapps:
        subapp['mysql_stroage_engine'] = app['mysql_stroage_engine']
    # 初始化表结构
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()

