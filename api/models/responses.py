from pydantic import BaseModel
from models.db import Person

class PersonList(BaseModel):
    persons: list[Person]