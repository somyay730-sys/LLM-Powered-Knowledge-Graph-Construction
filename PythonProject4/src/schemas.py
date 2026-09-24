from pydantic import BaseModel


class Entity(BaseModel):
    name: str
    type: str


class Relationship(BaseModel):
    source: str
    relation: str
    target: str


class KnowledgeGraph(BaseModel):
    entities: list[Entity]
    relationships: list[Relationship]