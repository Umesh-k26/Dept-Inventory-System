from pydantic import BaseModel

class Person(BaseModel):
    person_name: str
    person_age: int
    