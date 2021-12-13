from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi import HTTPException, Depends, APIRouter
from ..db.base_class import Base
from ..dependencies import get_db
from typing import List, Optional
from ..reactions import controller

"""
-----------------------------------------
DATABASE MODIFICATIONS
-----------------------------------------
"""

"""
-----------------------------------------
SQL Models Definition
-----------------------------------------
"""
# Class to define a basic action


class Actions(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    target = Column(String, nullable=False)
    workdir = Column(String)
    action_type_id = Column(Integer, ForeignKey("action_types.id"))

    action_type = relationship("Action_Types", back_populates="actions")

# Identify what command needs to be sent
# (define here or in action class in code)


class Action_Types(Base):
    __tablename__ = "action_types"
    id = Column(Integer, primary_key=True, index=True)
    command = Column(String, nullable=False)
    actions = relationship("Actions", back_populates="action_type")


"""
-----------------------------------------
SCHEMAS and Routers
-----------------------------------------
"""
# Action Schema Creation #


class ActionBase(BaseModel):
    description: str
    target: str
    workdir: Optional[str]
    action_type_id: int


class Action_Schema(ActionBase):
    id: int

    class Config:
        orm_mode = True


class ActionCreate_Schema(ActionBase):
    pass


action_router = SQLAlchemyCRUDRouter(
    schema=Action_Schema,
    create_schema=ActionCreate_Schema,
    db_model=Actions,
    db=get_db,
    prefix='actions'
)

# Action Type Schemas #


class ActionTypeBase(BaseModel):
    command: str


class ActionType_Schema(ActionTypeBase):
    id: int
    actions: List[Action_Schema]

    class Config:
        orm_mode = True


class ActionTypeCreate_Schema(ActionTypeBase):
    pass


actiontype_router = SQLAlchemyCRUDRouter(
    schema=ActionType_Schema,
    create_schema=ActionTypeCreate_Schema,
    db_model=Action_Types,
    db=get_db,
    prefix='action_types'
)

"""
-----------------------------------------
Default Route Overwrite

Since we want to get the command used
when we query just one we overwrite the
usual get_item route created by
CrudRouter
-----------------------------------------
"""


class ActionWthType(BaseModel):
    id: int
    description: str
    target: str
    action_type_id: int
    workdir: Optional[str]
    command: str


def get_action(db: Session, action_id: int):
    action = (db.query(Actions)
              .join(Action_Types)
              .filter(Actions.id == action_id)
              .with_entities(Actions.id, Actions.description,
                             Actions.action_type_id,
                             Actions.target,
                             Actions.workdir,
                             Action_Types.command)
              .first())
    if action is None:
        raise HTTPException(status_code=404, detail="Action Type not found")
    return action


@action_router.get('/{item_id}', response_model=ActionWthType)
def overloaded_get_one(item_id: int, db: Session = Depends(get_db)):
    return get_action(db, item_id)


"""
-----------------------------------------
MANAGE REACTIONS
-----------------------------------------
"""

reaction_router = APIRouter(
    prefix="/commands",
    tags=["commands"],
    responses={404: {"description": "Not found"}},
)


@reaction_router.post('/{command_id}')
def fire_off_command(command_id: int, db: Session = Depends(get_db)):
    command = get_action(db, command_id)
    cmd = controller.command(command.command, command.workdir, command.target)
    fire = cmd.__getattribute__(cmd.ctype)
    cmdreturncode = fire()
    try:
        print('Status Code', cmdreturncode)
    except Exception as e:
        print('Error Check Logs', e.args)
    return command
