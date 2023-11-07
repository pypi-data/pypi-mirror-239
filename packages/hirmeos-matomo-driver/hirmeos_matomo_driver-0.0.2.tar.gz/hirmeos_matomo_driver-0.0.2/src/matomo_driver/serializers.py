from pydantic import BaseModel, Field


class MatomoUrlResult(BaseModel):
    visits: int = Field(alias='nb_visits')
    url: str


class MatomoEventCategory(BaseModel):
    name: str = Field(alias='label')
    id: int = Field(alias='idsubdatatable')


class MatomoEvent(BaseModel):
    visits: int = Field(alias='nb_visits')
    identifier: str = Field(alias='label')
    category: str
