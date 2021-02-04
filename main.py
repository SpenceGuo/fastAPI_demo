from fastapi import FastAPI, Query
from get_response_msg import *
from model import *

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "COVID-19 DATA OF CN, USA & THE WORLD"}


@app.get("/ncov/world_today", response_model=WorldTodayModel)
async def get_world_data_today():
    data = get_world_today()
    return data


@app.get("/ncov/cn_province_today", response_model=ProvinceTodayModel)
async def get_china_province_data_today():
    data = get_cn_province_today()
    return data


@app.get("/ncov/cn_data_stream", response_model=CountryDataStreamModel)
async def get_china_data_stream(
        start_date: str = Query(..., description='start Date', example='2019-12-01'),
        end_date: str = Query(..., description='end date', example='2021-02-03')
):
    data = get_cn_data_stream(start_date, end_date)
    return data


@app.get("/ncov/us_data_stream", response_model=CountryDataStreamModel)
async def get_usa_data_stream(
        start_date: str = Query(..., description='start Date', example='2019-12-01'),
        end_date: str = Query(..., description='end date', example='2021-02-03')):
    data = get_us_data_stream(start_date, end_date)
    return data


@app.get("/ncov/us_state_today", response_model=ProvinceTodayModel)
async def get_usa_state_data_today():
    data = get_us_state_today()
    return data


@app.get("/ncov/us_city_today")
async def get_usa_city_data_today():
    data = get_us_city_today()
    return data
