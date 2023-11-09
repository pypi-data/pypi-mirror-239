提示[tips]  
仅适用于2018-01-01以后的中国节假日查询, 包含法定节假日及周末  

安装[install]  
pip install holiday-chn  

使用[use]  
import holiday_chn  

判断传入日期是否为节假日[Determine whether the incoming date is a holiday]  
holiday_chn.is_holiday('2024-01-01') // return True  

获取指定年份的节假日日期[Obtain holiday dates for the specified year]  
holiday_chn.holidays(2024) // return date list of holidays  

获取指定年份的工作日日期[Obtain the working day date of the specified year]  
holiday_chn.workdays(2024) // return date list of workdays