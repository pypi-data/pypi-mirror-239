from typing import Optional

from aiohttp import web
from aiohttp.typedefs import LooseHeaders
from pydantic import BaseModel, TypeAdapter

from aiohttp_simple.template.data_model import (
    Paginate,
    ResponseBase,
    ResponsePaginateBody,
)
from aiohttp_simple.template.db_table import BaseTable


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
    return web.Response(
        text=text,
        body=body,
        status=status,
        reason=reason,
        headers=headers,
        content_type=content_type,
    )


def success_response(dataModel=None, data=None, paginate: Optional[Paginate] = None):
    if not isinstance(data, dict):
        if data and isinstance(data, list) and isinstance(data[0], BaseTable):
            data = [item.to_dict() for item in data]
        elif isinstance(data, BaseTable):
            data = data.to_dict()
    if paginate:
        body = ResponsePaginateBody(
            data=TypeAdapter(dataModel).validate_python(data),
            current_page=paginate.current_page,
            page_size=paginate.page_size,
            total_page=paginate.total_page,
            total_count=paginate.total_count,
        )
    else:
        body = TypeAdapter(dataModel).validate_python(data)
    return model_json_response(
        data=ResponseBase(
            code="0000",
            body=body,
            message="success",
        )
    )


def error_response(code: str = "0001", message="error"):
    return model_json_response(data=ResponseBase(code=code, message=message))
