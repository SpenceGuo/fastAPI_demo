from typing import List

from pydantic import BaseModel, Field


class DataStream(BaseModel):
    date: str = Field(..., example='2020-12-01')
    active: int = Field(..., example=0)
    confirmed: int = Field(..., example=0)
    deaths: int = Field(..., example=0)
    recovered: int = Field(..., example=0)


class DataToday(BaseModel):
    name: str = Field(..., example='Country/Province/State name')
    active: int = Field(..., example=0)
    confirmed: int = Field(..., example=0)
    deaths: int = Field(..., example=0)
    recovered: int = Field(..., example=0)


class CityToday(BaseModel):
    province: str = Field(..., example='Indiana')
    city: str = Field(..., example='Bartholomew')
    active: int = Field(..., example=0)
    confirmed: int = Field(..., example=0)
    deaths: int = Field(..., example=0)
    recovered: int = Field(..., example=0)


class WorldTodayModel(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example='')
    date: str = Field(..., example='2021-01-29')
    data: List[DataToday]


class ProvinceTodayModel(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example='')
    country: str = Field(..., example='China/United States of America')
    data: List[DataToday]


class CountryDataStreamModel(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example='')
    country: str = Field(..., example='China')
    startDate: str = Field(..., example='2020-12-01')
    endDate: str = Field(..., example='2021-01-29')
    data: List[DataStream]


class CityDataTodayModel(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example='')
    country: str = Field(..., example='China/United States of America')
    data: List[CityToday]
