import calendar
import datetime

from .config import SUPPORT_YEAR, YEAR_MAPPINGS, DAY_LIST


def is_holiday(date_str: str):
    """
    :param date_str: '2024-01-01'
    :return: True
    """
    if '-' not in date_str or len(date_str) != 10:
        raise TypeError('parameter error,the right is like 2024-01-01.')
    if date_str[:4] in SUPPORT_YEAR:
        year_data = YEAR_MAPPINGS.get(date_str[:4])
        holiday = year_data.get('holidays')
        workday = year_data.get('workdays')
        year = int(date_str.split('-')[0])
        month = int(date_str.split('-')[1])
        day = int(date_str.split('-')[2])
        if date_str in holiday:
            return True
        elif (datetime.date(year, month, day).weekday() == 5 or datetime.date(year, month, day).weekday() == 6) and \
                date_str not in workday:
            return True
        else:
            return False
    else:
        raise KeyError('no enough datas, it just support after 2018-01-01.')


def holidays(year: int):
    """
    :param year: 2024
    :return: holiday_list = []
    """
    if str(year) in SUPPORT_YEAR:
        year_data = YEAR_MAPPINGS.get(str(year))
        holiday = year_data.get('holidays')
        workday = year_data.get('workdays')
        holiday_list = []
        for i in range(1, 13):
            days = DAY_LIST.get(str(i))
            if i == 2 and calendar.isleap(year):
                days = 29
            for j in range(1, days + 1):
                date_str = f'{str(year)}-{str(i).zfill(2)}-{str(j).zfill(2)}'
                if date_str in holiday:
                    holiday_list.append(date_str)
                else:
                    if (datetime.date(year, i, j).weekday() == 5 or datetime.date(year, i, j).weekday() == 6) and \
                            date_str not in workday:
                        holiday_list.append(date_str)
        return holiday_list
    else:
        raise ValueError('parameter error,integer meed, the right is like 2024. or no enough datas, it just support '
                         'after 2018-01-01.')


def workdays(year: int):
    """
    :param year: 2024
    :return: work_list = []
    """
    if str(year) in SUPPORT_YEAR:
        year_data = YEAR_MAPPINGS.get(str(year))
        holiday = year_data.get('holidays')
        workday = year_data.get('workdays')
        work_list = []
        for i in range(1, 13):
            days = DAY_LIST.get(str(i))
            if i == 2 and calendar.isleap(year):
                days = 29
            for j in range(1, days + 1):
                date_str = f'{str(year)}-{str(i).zfill(2)}-{str(j).zfill(2)}'
                if date_str in workday:
                    work_list.append(date_str)
                else:
                    if (datetime.date(year, i, j).weekday() != 5 and datetime.date(year, i, j).weekday() != 6) and \
                            date_str not in holiday:
                        work_list.append(date_str)
        return work_list
    else:
        raise ValueError('parameter error,integer meed, the right is like 2024. or no enough datas, it just support '
                         'after 2018-01-01.')
