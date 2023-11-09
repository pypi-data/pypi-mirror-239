from setuptools import find_packages
from setuptools import setup

version = '1.2024.1'

setup(
    name='holiday-chn',
    version=version,
    license='ZPL 2.1',
    description='This package provides judgment on Chinese holidays and outputs the dates of all holidays.By using it, one can determine whether a certain date is a holiday and obtain the working days or holidays of a certain year.\n'
                '该库提供了2018年以后的中国节假日查询，主要有is_holiday()方法判断日期是否为节假日，holidays()方法获取指定年的节假日日期，workdays()方法获取指定年的工作日日期。\n'
                'e.g: \n'
                'is_holiday("2024-01-01") 判断2024-01-01是否为节假日，返回True\n'
                'holidays(2024) 获取2024年的所有节假日日期，返回日期list\n'
                'workdays(2024) 获取2024年的所有工作日日期，返回日期list.',
    author='lytcreate',
    author_email='lytcreate@163.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    readme=''
)
