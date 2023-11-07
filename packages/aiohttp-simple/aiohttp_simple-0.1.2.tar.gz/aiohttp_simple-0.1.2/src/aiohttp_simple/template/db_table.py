from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import declarative_base


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
            for key, value in self.__dict__.items()
            if not key.startswith("__")
        }


DbTableBase = declarative_base(cls=BaseTable)
