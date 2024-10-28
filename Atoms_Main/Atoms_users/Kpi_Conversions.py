import ast

from Atoms_users.models import MachineCardsList
from .Calculation_fun import *

def get_kpi_conversion_fun1(instance):
    machine_id = instance.Machine_Id
    time_stamp = instance.Timestamp
    # print('machine_id',machine_id)
    get_data = MachineCardsList.objects.filter(Machine_Id__Machine_id=machine_id)
    # print('get_data',get_data)
    if get_data.exists():
        for data in get_data:
            # print('dataaaaaaaaaaa',data)
            # print('dataaaaaaaaaaa',data.Machine_Id)

            get_convserion_fun = data.Conversion_Fun
            datapoint = data.DataPoints
            get_name = data.Kpi_Name
            get_title = data.Title
            get_mode = data.mode
            # print('???????????',data.DataPoints[0])
            # print('datapoint', datapoint)
            data_dict = {
                "time_stamp": time_stamp,
                "machine_id": machine_id,
                "get_name": get_name,
                "get_value": None,
                "get_title": get_title,
                "get_mode": get_mode

            }

            datapoint_value = []
            value_list = []

            for i in range(len(datapoint)):
                # print('except')
                d_i_o = eval(f'instance.{datapoint[i]}')



                if str(d_i_o).lower() == "true":
                    d_i_o = "On"
                elif str(d_i_o).lower() == "false":
                    d_i_o = "Off"
                elif str(d_i_o).lower() == "on":
                    d_i_o = "On"
                elif str(d_i_o).lower() == "off":
                    d_i_o = "Off"
                # print('d_i_o', d_i_o)
                datapoint_value.append(d_i_o)
                try:
                    conversion_fun = get_convserion_fun[i]
                except:
                    conversion_fun = get_convserion_fun[0]

                data_dict['get_value']=d_i_o
                # data_dict['get_value']=datapoint_value
                # print('datapoint_value',datapoint_value)

                switch_dict = {
                    "Live": lambda: value_list.append(Live(data_dict)),
                    "Average": lambda: value_list.append(Average(data_dict,datapoint[i])),
                    "High_Low": lambda: value_list.append(High_Low(data_dict)),
                    "History": lambda: value_list.append(History(data_dict,datapoint[i])),
                    "RunTime": lambda: value_list.extend(RunTime(data_dict,datapoint[i])),#machine on off count
                    "alarm1": lambda: value_list.append(alarm1(data_dict,datapoint[i])),# if i==0 or i==1 etc
                    "Mode_": lambda: value_list.append(Mode_(data_dict,datapoint[i])),# if i==0 or i==1 etc

                    "RunTime_HMS": lambda: value_list.extend(RunTime_HMS(data_dict,datapoint[i])),# if i==0 or i==1 etc

                    'default': lambda: {"status": 'please give correct module'},
                }
                result = switch_dict.get(conversion_fun, switch_dict['default'])()
            data_dict['get_value'] = value_list
            # print('data_dict////////////////////////',data_dict)
            for mode_data in get_mode:
                # print('data',data)
                # print('mode_data',mode_data.mode)
                # get_mode = mode_data
                data_dict['get_mode'] = mode_data

                switch_dict = {
                    "New_Record": lambda: New_Record(data_dict),
                    "Day": lambda: Day(data_dict),
                    "Month": lambda: Month(data_dict),
                    "History_result": lambda: History_result(data_dict),
                    # "Alarm_fun": lambda: Alarm_fun(data_dict),
                    'default': lambda: {"status": 'please give correct module'},
                }
                store_rawkpi_data = switch_dict.get(mode_data, switch_dict['default'])()



