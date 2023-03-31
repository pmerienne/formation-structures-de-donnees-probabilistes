from random import randint

import names
from pydantic import BaseModel
from pydantic.fields import Field


class User(BaseModel):
    first_name: str = Field(default_factory=names.get_first_name)
    last_name: str = Field(default_factory=names.get_last_name)
    age: int = Field(default_factory=lambda: randint(0, 100))

