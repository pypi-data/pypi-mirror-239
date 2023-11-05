from typing import Set, Dict

from pydantic import BaseModel, field_validator


class Remote(BaseModel):
    url: str  # TODO strip trailing slash
    email: str
    password: str


class Doc(BaseModel):
    id: str
    text: str
    time: int
    tags: Set

    # noinspection PyNestedDecorators
    @field_validator('tags')
    @classmethod
    def tags_as_set_for_hashing(cls, v) -> Set:
        return set(v)

    def __hash__(self):
        return self.model_dump_json().__hash__()


Index = Dict[int, Doc]
