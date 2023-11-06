import math
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, computed_field


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
    def total_page(self) -> Union[int, None]:
        if self.total_count is None:
            return None
        return math.ceil(self.total_count / self.page_size)
