"""
疫情数据更新代码
数据源：约翰霍普金斯大学官方网站
"""
import json
import mysql.connector
import requests
import time
from datetime import datetime,timedelta

# connect database
mydb = mysql.connector.connect(
  host="10.10.10.10",
  user="groupleader",
  passwd="onlyleaders",
  database="ncov"
)
mycursor = mydb.cursor()

def pandemic_cn_country():
    url = "https://api.covid19api.com/total/country/China?from=2021-01-30T00:00:00Z&to=2021-02-02T23:00:00Z"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.text
    data = json.loads(data)
    i = 0
    while i < len(data):
        sql = "INSERT INTO pandemic_cn_country (country,countrycode,city,citycode,lat,lon,date,active,comfirmed,deaths,recovered)\
                                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (data[i]['Country'], 'CN', data[i]['City'], data[i]['CityCode'],
               '31.2', '121.45', \
               datetime.strptime(data[i]['Date'], "%Y-%m-%dT%H:%M:%SZ"), data[i]['Active'], data[i]['Confirmed'],
               data[i]['Deaths'], data[i]['Recovered'])
        i += 1
        mycursor.execute(sql, val)
        mydb.commit()
        print("%d\n"%i)
        # print(datetime.strptime(data[i]['Date'], "%Y-%m-%dT%H:%M:%SZ"))
    print("pandemic_us_country update successfully\n")

def pandemic_cn_province():
    url = "https://api.covid19api.com/country/China?from=2021-01-30T00:00:00Z&to=2021-02-02T23:00:00Z"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.text
    data = json.loads(data)

    i=0
    while i < len(data):
        sql = "INSERT INTO pandemic_cn_province (country,countrycode,province,city,citycode,lat,lon,date,active,comfirmed,deaths,recovered)\
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (data[i]['Country'],data[i]['CountryCode'],data[i]['Province'],data[i]['City'],data[i]['CityCode'],data[i]['Lat'],data[i]['Lon'],\
               datetime.strptime(data[i]['Date'], "%Y-%m-%dT%H:%M:%SZ"), data[i]['Active'],data[i]['Confirmed'],data[i]['Deaths'],data[i]['Recovered'])
        i += 1
        mycursor.execute(sql, val)
        mydb.commit()
        print("%d\n" % i)
        # print(datetime.strptime(data[i]['Date'], "%Y-%m-%dT%H:%M:%SZ"))
    print("pandemic_cn_province update successfully\n")

def pandemic_us_country():
    url = "https://api.covid19api.com/total/country/United States of America?from=2021-01-30T00:00:00Z&to=2021-02-02T23:00:00Z"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.text
    data = json.loads(data)
    i = 0
    while i < len(data):
        sql = "INSERT INTO pandemic_us_country (country,countrycode,city,citycode,lat,lon,date,active,comfirmed,deaths,recovered)\
                                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (data[i]['Country'], 'US', data[i]['City'], data[i]['CityCode'],
               '40.59', '-102.36', \
               datetime.strptime(data[i]['Date'], "%Y-%m-%dT%H:%M:%SZ"), data[i]['Active'], data[i]['Confirmed'],
               data[i]['Deaths'], data[i]['Recovered'])
        i += 1
        mycursor.execute(sql, val)
        mydb.commit()
        print("%d\n"%i)
        # print(datetime.strptime(data[i]['Date'], "%Y-%m-%dT%H:%M:%SZ"))
    print("pandemic_us_country update successfully\n")


'''
update data by changing url's time everyday 
'''
def pandemic_us_cityandstate():
    url = "https://api.covid19api.com/country/United States of America?from=2021-01-30T00:00:00Z&to=2021-02-02T23:00:00Z"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.text
    data = json.loads(data)

    #create temporary table to achieve results of state in US
    sql = "CREATE TEMPORARY TABLE TempState (\
  `country` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,\
  `countrycode` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,\
  `province` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,\
  `city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,\
  `citycode` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,\
  `lat` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,\
  `lon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,\
  `date` datetime(6) DEFAULT NULL,\
  `active` int DEFAULT NULL,\
  `comfirmed` int DEFAULT NULL,\
  `deaths` int DEFAULT NULL,\
  `recovered` int DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;"
    mycursor.execute(sql)
    mydb.commit()

    i = 0
    while i < len(data):
        # print(datetime.strptime(data[i]['Date'], "%Y-%m-%dT%H:%M:%SZ"))
        sql = "INSERT INTO pandemic_us_city (country,countrycode,province,city,citycode,lat,lon,date,active,comfirmed,deaths,recovered)\
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (data[i]['Country'], data[i]['CountryCode'], data[i]['Province'], data[i]['City'], data[i]['CityCode'],
               data[i]['Lat'], data[i]['Lon'], \
               datetime.strptime(data[i]['Date'], "%Y-%m-%dT%H:%M:%SZ"), data[i]['Active'], data[i]['Confirmed'],
               data[i]['Deaths'], data[i]['Recovered'])

        mycursor.execute(sql, val)
        mydb.commit()

        sql = "INSERT INTO TempState (country,countrycode,province,city,citycode,lat,lon,date,active,comfirmed,deaths,recovered)\
                                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (data[i]['Country'], data[i]['CountryCode'], data[i]['Province'], data[i]['City'], data[i]['CityCode'],
               data[i]['Lat'], data[i]['Lon'], \
               datetime.strptime(data[i]['Date'], "%Y-%m-%dT%H:%M:%SZ"), data[i]['Active'], data[i]['Confirmed'],
               data[i]['Deaths'], data[i]['Recovered'])
        mycursor.execute(sql, val)
        mydb.commit()
        i += 1
        print(i)
    print("pandemic_us_city updates successfully\n")

    #update pandemic_us_state
    sql = "INSERT INTO pandemic_us_state(country,countrycode,province,date,active,comfirmed,deaths,recovered) \
        SELECT country,countrycode,province,date,SUM(active),SUM(comfirmed),SUM(deaths),SUM(recovered) \
        FROM `TempState` GROUP BY province,date"
    mycursor.execute(sql)
    mydb.commit()

    #change null into ""
    sql = "UPDATE pandemic_us_state SET city= ifnull(city,''), citycode=ifnull(city,''),lat=ifnull(lat,''),lon=ifnull(lon,'')"
    mycursor.execute(sql)
    mydb.commit()

    #delete temporary table TempState
    sql = "DROP TABLE TempState"
    mycursor.execute(sql)
    mydb.commit()
    print("pandemic_us_state updates successfully\n")

def pandemic_uk_country():
    url = "https://api.covid19api.com/total/country/United Kingdom?from=2021-01-30T00:00:00Z&to=2021-02-02T23:00:00Z"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.text
    data = json.loads(data)
    i = 0
    while i < len(data):
        sql = "INSERT INTO pandemic_uk_country (country,countrycode,city,citycode,lat,lon,date,active,comfirmed,deaths,recovered)\
                                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (data[i]['Country'], 'UK', data[i]['City'], data[i]['CityCode'],
               '51.30', '0.7', \
               datetime.strptime(data[i]['Date'], "%Y-%m-%dT%H:%M:%SZ"), data[i]['Active'], data[i]['Confirmed'],
               data[i]['Deaths'], data[i]['Recovered'])
        i += 1
        mycursor.execute(sql, val)
        mydb.commit()
        print("%d\n"%i)
        # print(datetime.strptime(data[i]['Date'], "%Y-%m-%dT%H:%M:%SZ"))
    print("pandemic_us_country update successfully\n")

def pandemic_world_today():
    url = "https://api.covid19api.com/summary"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.text
    data = json.loads(data)
    countries = data['Countries']
    #print(type(countries[0]['TotalConfirmed']))

    i = 0
    while i < len(countries):
        sql = "INSERT INTO pandemic_world (country,countrycode,province,city,citycode,lat,lon,date,active,comfirmed,deaths,recovered)\
                                                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (countries[i]['Country'], countries[i]['CountryCode'], "", "", "", \
               "", "", \
               datetime.strptime(countries[i]['Date'], "%Y-%m-%dT%H:%M:%SZ"), \
               countries[i]['TotalConfirmed']-countries[i]['TotalDeaths']-countries[i]['TotalRecovered'],
               countries[i]['TotalConfirmed'], countries[i]['TotalDeaths'], countries[i]['TotalRecovered'])
        i += 1
        mycursor.execute(sql, val)
        mydb.commit()
    print("pandemic_world updates successfully\n")

def pandemic_world():
    url = "https://api.covid19api.com/countries"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    country_data = response.text
    country_data = json.loads(country_data)

    i = 0
    while i < len(country_data):
        country = country_data[i]['Country']
        countrycode = country_data[i]['ISO2']
        url = "https://api.covid19api.com/total/country/%s?from=2021-01-30T00:00:00Z&to=2021-02-02T23:00:00Z" %(country)
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.text
        data = json.loads(data)
        # f = open("1.txt", "ab")
        # for chunk in response.iter_content(chunk_size=512):
        #     if chunk:
        #         f.write(chunk)
        # f.close()
        #some countries are not existing,returning dict type
        if type(data) is list:
            j = 0
            while j < len(data):
                sql = "INSERT INTO pandemic_world (country,countrycode,province,city,citycode,lat,lon,date,active,comfirmed,deaths,recovered)\
                                                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (country, countrycode, data[j]['Province'], data[j]['City'], data[j]['CityCode'],
                       data[j]['Lat'], data[j]['Lon'], \
                       datetime.strptime(data[j]['Date'], "%Y-%m-%dT%H:%M:%SZ"), data[j]['Active'], data[j]['Confirmed'],
                       data[j]['Deaths'], data[j]['Recovered'])
                j += 1
                mycursor.execute(sql, val)
                mydb.commit()
            print("%s success\n" % (country))
        else:
            time.sleep(1)
        i += 1
    print("pandemic_world updates successfully \n")

if __name__ == '__main__':
    pandemic_cn_country()
    pandemic_cn_province()
    pandemic_us_country()
    pandemic_us_cityandstate()
    pandemic_uk_country()
    pandemic_world()
