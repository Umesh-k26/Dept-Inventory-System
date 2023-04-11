from pydantic import BaseModel


class User(BaseModel):
    user_id : str
    first_name : str | None = None
    last_name : str | None = None
    gmail : str | None = None
    user_type : str | None = None
    department : str | None = None


    