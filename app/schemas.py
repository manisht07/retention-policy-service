
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime

class ConditionBlock(BaseModel):
    combinator: Optional[str] = Field(None, example="all")
    conditions: Optional[List[Any]] = None
    field: Optional[str] = None
    operator: Optional[str] = None
    value: Optional[Any] = None

class CalculationBlock(BaseModel):
    field: str
    operator: str
    value: Any

class RuleBlock(BaseModel):
    if_: Optional[ConditionBlock] = Field(None, alias="if")
    then: Optional[dict]
    else_: Optional[dict] = Field(None, alias="else")

class RetentionPolicyBase(BaseModel):
    name: str
    description: Optional[str]
    application: str
    schemas: List[str]
    tables: List[str]
    conditions: dict

class RetentionPolicyCreate(RetentionPolicyBase):
    pass

class RetentionPolicyUpdate(BaseModel):
    description: Optional[str]
    schemas: Optional[List[str]]
    tables: Optional[List[str]]
    conditions: Optional[dict]

class RetentionPolicyOut(RetentionPolicyBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
