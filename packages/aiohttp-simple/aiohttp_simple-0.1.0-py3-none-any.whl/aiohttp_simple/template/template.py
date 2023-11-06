from datetime import datetime
import math
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, computed_field

from aiohttp.typedefs import LooseHeaders
from pydantic import BaseModel, TypeAdapter
from aiohttp import web
from sqlalchemy.orm import declarative_base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
import logging

logger = logging.getLogger(__name__)


class BaseTable:
    is_delete = Column(Boolean, default=False)
    create_time = Column(DateTime, default=func.now(), onupdate=func.now())
    create_user = Column(Integer, default=None)
    update_time = Column(DateTime, default=None, onupdate=func.now())
    update_user = Column(Integer, default=None)

    @classmethod
    def from_model(cls, user):
        user_dict = user.model_dump()
        return cls(**user_dict)  # type: ignore
    
    def to_dict(self):
        return {
            key: value
            for key,value in self.__dict__.items()
            if not key.startswith('__')
        }

Base = declarative_base(cls=BaseTable)

class ResponsePaginateBody(BaseModel):
    data: Optional[List] = None
    current_page: int
    page_size: int
    total_page: Optional[int] = None
    total_count: Optional[int] = None

class ResponseBase(BaseModel):
    code: str
    body: Optional[Union[Dict, List, ResponsePaginateBody]] = None
    message: Optional[str] = None


class Paginate(BaseModel):
    current_page: int = 1
    page_size: int = 10
    total_count: Optional[int] = None

    @computed_field
    def offset(self) -> int:
        return (self.current_page - 1) * self.page_size
    
    @computed_field
    def limit(self) -> int:
        return self.page_size
    
    @computed_field
    def total_page(self) ->Union[int, None]:
        if self.total_count is None:
            return None
        return math.ceil(self.total_count / self.page_size)


def model_json_response(
    data: Optional[BaseModel] = None,
    *,
    text: Optional[str] = None,
    body: Optional[bytes] = None,
    status: int = 200,
    reason: Optional[str] = None,
    headers: Optional[LooseHeaders] = None,
    content_type: str = "application/json",
):
    if data is not None and isinstance(data, BaseModel):
        if text or body:
            raise ValueError("only one of data, text, or body should be specified")
        else:
            text = data.model_dump_json()
            logger.info(f"text: {text}")
            logger.info(f"data: {data}")
            logger.info(f"data: {data.model_dump_json()}")
    return web.Response(
        text=text,
        body=body,
        status=status,
        reason=reason,
        headers=headers,
        content_type=content_type,
    )


def success_response(dataModel=None, data=None, paginate: Optional[Paginate]=None):
    if not isinstance(data, dict):
        if data and isinstance(data, list) and isinstance(data[0], BaseTable):
            data = [ item.to_dict() for item in data]
        elif isinstance(data, BaseTable):
            data = data.to_dict()
    if paginate:
        body = ResponsePaginateBody(
                    data=TypeAdapter(dataModel).validate_python(data),
                    current_page = paginate.current_page,
                    page_size = paginate.page_size,
                    total_page = paginate.total_page,
                    total_count = paginate.total_count
                )
    else:
        body=TypeAdapter(dataModel).validate_python(data)
    return model_json_response(
        data=ResponseBase(
            code="0000",
            body=body,
            message="success",
        )
    )


def error_response(code: str = "0001", message="error"):
    return model_json_response(data=ResponseBase(code=code, message=message))