from __future__ import annotations

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from aiohttp_simple.template.db_table import DbTableBase
from aiohttp_simple.utils.log import logger
from aiohttp_simple.utils.setting import SETTING


async def mysql_stroage_engine(app):
    app["mysql_stroage_engine"] = create_async_engine(SETTING.mysql_url, echo=True)
    engine = app["mysql_stroage_engine"]
    for subapp in app._subapps:
        subapp["mysql_stroage_engine"] = app["mysql_stroage_engine"]
    try:
        # 初始化表结构
        async with engine.begin() as conn:
            # await conn.run_sync(DbTableBase.metadata.drop_all)
            await conn.run_sync(DbTableBase.metadata.create_all)
    except Exception as e:
        logger.info(f"初始化表失败")

    yield engine
    await engine.dispose()
