from enum import Enum
from pydantic import BaseModel
from typing import Optional


class Datatype(Enum):
    INTEGER = int
    REAL = float
    TEXT = str
    BLOB = bytes


class PrimaryKeyType(Enum):
    Ascending = 'ASC'
    Descending = 'DESC'


class TableColumn(BaseModel):
    name: str
    datatype: Datatype
    nullable: Optional[bool] = False
    primary_key: Optional[PrimaryKeyType] = None
