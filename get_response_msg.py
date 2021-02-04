import json
import pymysql
import time


def get_present_date():
    return time.strftime('%Y-%m-%d')


# 数据量较大，暂未确定是否实现该功能,留个模板
def get_world_data_stream(start_date: str, end_date: str):
    result = {
        'success': True, 'message': None, 'startDate': start_date, 'endDate': end_date,
        'data': []
    }
    db = pymysql.connect(host='10.10.10.10', port=3306, user='readonly', password='readonly', database='ncov')
    cursor = db.cursor()
    sql = f"SELECT country,countrycode,date,active,comfirmed,deaths,recovered FROM pandemic_cn_country " \
          f" WHERE date BETWEEN {start_date} AND {end_date} ORDER BY date ASC"
    cursor.execute(sql)
    temp_data = cursor.fetchall()
    db.close()
    for line in temp_data:
        one_data = {'name': 'China', 'date': line[2].strftime('%Y-%m-%d'), 'active': line[3], 'confirmed': line[4], 'deaths': line[5],
                    'recovered': line[6]}
        result['data'].append(one_data)
    return result


def get_world_today():
    result = {
        'success': True, 'message': '', 'date': get_present_date(),
        'data': []
    }
    db = pymysql.connect(host='10.10.10.10', port=3306, user='readonly', password='readonly', database='ncov')
    cursor = db.cursor()
    sql = f"SELECT country,countrycode,date,active,comfirmed,deaths,recovered FROM pandemic_world " \
          f"WHERE date='{get_present_date()}%' GROUP BY country"
    cursor.execute(sql)
    temp_data = cursor.fetchall()
    db.close()
    for line in temp_data:
        one_data = {'name': line[0], 'active': line[3], 'confirmed': line[4], 'deaths': line[5], 'recovered': line[6]}
        result['data'].append(one_data)
    return result


def get_cn_data_stream(start_date: str, end_date: str):
    result = {
        'success': True, 'message': '', 'country': 'China', 'startDate': start_date, 'endDate': end_date,
        'data': []
    }
    db = pymysql.connect(host='10.10.10.10', port=3306, user='readonly', password='readonly', database='ncov')
    cursor = db.cursor()
    sql = f"SELECT country,countrycode,date,active,comfirmed,deaths,recovered FROM pandemic_cn_country " \
          f" WHERE date BETWEEN \'{start_date}\' AND \'{end_date}\' ORDER BY date ASC"
    cursor.execute(sql)
    temp_data = cursor.fetchall()
    db.close()
    for line in temp_data:
        one_data = {'date': line[2].strftime('%Y-%m-%d'), 'active': line[3], 'confirmed': line[4], 'deaths': line[5],
                    'recovered': line[6]}
        result['data'].append(one_data)
    return result


def get_cn_province_today():
    result = {
        'success': True, 'message': '', 'date': get_present_date(), 'country': 'China',
        'data': []
    }
    db = pymysql.connect(host='10.10.10.10', port=3306, user='readonly', password='readonly', database='ncov')
    cursor = db.cursor()
    sql = f"SELECT country,countrycode,province,date,active,comfirmed,deaths,recovered FROM pandemic_cn_province WHERE date='{get_present_date()}%'"
    cursor.execute(sql)
    temp_data = cursor.fetchall()
    db.close()
    for line in temp_data:
        one_data = {'name': line[2], 'active': line[4], 'confirmed': line[5], 'deaths': line[6], 'recovered': line[7]}
        result['data'].append(one_data)
    return result


def get_us_data_stream(start_date: str, end_date: str):
    result = {
        'success': True, 'message': '', 'country': 'United States of America',
        'startDate': start_date, 'endDate': end_date,
        'data': []
    }
    db = pymysql.connect(host='10.10.10.10', port=3306, user='readonly', password='readonly', database='ncov')
    cursor = db.cursor()
    sql = f"SELECT country,countrycode,date,active,comfirmed,deaths,recovered FROM pandemic_us_country " \
          f" WHERE date BETWEEN \'{start_date}\' AND \'{end_date}\' ORDER BY date ASC"
    cursor.execute(sql)
    temp_data = cursor.fetchall()
    db.close()
    for line in temp_data:
        one_data = {'date': line[2].strftime('%Y-%m-%d'), 'active': line[3], 'confirmed': line[4], 'deaths': line[5],
                    'recovered': line[6]}
        result['data'].append(one_data)
    return result


def get_us_state_today():
    result = {
        'success': True, 'message': '', 'date': get_present_date(), 'country': 'United States of America',
        'data': []
    }
    db = pymysql.connect(host='10.10.10.10', port=3306, user='readonly', password='readonly', database='ncov')
    cursor = db.cursor()
    sql = f"SELECT country,countrycode,province,date,active,comfirmed,deaths,recovered FROM pandemic_us_state " \
          f"WHERE date='{get_present_date()}%'"
    cursor.execute(sql)
    temp_data = cursor.fetchall()
    db.close()
    for line in temp_data:
        one_data = {'name': line[2], 'active': line[4], 'confirmed': line[5], 'deaths': line[6], 'recovered': line[7]}
        result['data'].append(one_data)
    return result


def get_us_city_today():
    result = {
        'success': True, 'message': '', 'date': get_present_date(), 'country': 'United States of America',
        'data': []
    }
    db = pymysql.connect(host='10.10.10.10', port=3306, user='readonly', password='readonly', database='ncov')
    cursor = db.cursor()
    sql = f"SELECT country,countrycode,province,city,date,active,comfirmed,deaths,recovered FROM pandemic_us_city " \
          f"WHERE date='{get_present_date()}%'"
    cursor.execute(sql)
    temp_data = cursor.fetchall()
    db.close()
    for line in temp_data:
        one_data = {'province': line[2], 'city': line[3], 'active': line[5], 'confirmed': line[6],
                    'deaths': line[7], 'recovered': line[8]}
        result['data'].append(one_data)
    return result


if __name__ == '__main__':
    print(json.dumps(get_cn_data_stream('2019-12-01', '2021-02-03'), indent=4))
