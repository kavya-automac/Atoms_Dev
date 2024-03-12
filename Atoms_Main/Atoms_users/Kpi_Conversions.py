
from Atoms_users.models import MachineCardsList
from .Calculation_fun import *


def get_kpi_conversion_fun(instance):
    machine_id=instance.Machine_Id
    time_stamp=instance.Timestamp
    # print('machine_id',machine_id)
    get_data = MachineCardsList.objects.filter(Machine_Id__Machine_id=machine_id)
    # print('get_data',get_data)
    for data in get_data:
        # print('???????????',data.DataPoints[0])

        get_convserion_fun = data.Conversion_Fun[0]
        datapoint=data.DataPoints
        # print('datapoint',datapoint)

        datapoint_value=[]
        for i in range(len(datapoint)):
            d_i_o = eval(f'instance.{datapoint[i]}')
            if str(d_i_o).lower() == "true":
                d_i_o = "On"
            elif str(d_i_o).lower() == "false":
                d_i_o = "Off"
            # print('d_i_o',d_i_o)
            datapoint_value.append(d_i_o)
        # print('d',datapoint_value)

        # print('datapoint_value1',datapoint_value1)
        # datapoint_value = eval(f'instance.{datapoint}')
        # print('datapoint_value',datapoint_value)
        # print(']]]]]]]]]',data.Kpi_Name)
        get_name=data.Kpi_Name
        # print('get_name',get_name)
        get_title=data.Title
        get_mode=data.mode
        data_dict={
            "time_stamp":time_stamp,
            "machine_id": machine_id,
            "get_name": get_name,
            "get_value": datapoint_value,
            "get_title": get_title,
            "get_mode": get_mode



        }

        # print('datapoint',data_dict)
        switch_dict = {
            "Live_new_record": lambda: Live_new_record(data_dict),
            "Live": lambda: Live(data_dict),
            "Average": lambda: Average(),
            "High_Low": lambda: High_Low(),

            'default': lambda: {"status": 'please give correct module'},
        }

        # Execute the corresponding function from the switch_dict or the default function
        result = switch_dict.get(get_convserion_fun, switch_dict['default'])()

        # print('get_convserion_fun',get_convserion_fun)


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
                    'default': lambda: {"status": 'please give correct module'},
                }
                store_rawkpi_data = switch_dict.get(mode_data, switch_dict['default'])()






            # elif len(get_convserion_fun) > 1:
            #
            #     print('tryyyy')
            #     d_i_o = eval(f'instance.{datapoint[i]}')
            #     convserion_fun =get_convserion_fun[i]
            #     if str(d_i_o).lower() == "true":
            #         d_i_o = "On"
            #     elif str(d_i_o).lower() == "false":
            #         d_i_o = "Off"
            #     print('d_i_o', d_i_o)
            #     datapoint_value.append(d_i_o)
            #
            #     print('convserion_fun',convserion_fun)
            #     data_dict['get_value'] = datapoint_value
            #     print('///////////////////')
            #     switch_dict = {
            #         "Live_new_record": lambda: value_list.append(Live_new_record(data_dict,"dashboard")),
            #         "Live": lambda: value_list.append(Live(data_dict,"dashboard")),
            #         "Average": lambda: Average(),
            #         "High_Low": lambda: High_Low(),
            #         "Cummulative": lambda: Cummulative(),
            #
            #         'default': lambda: {"status": 'please give correct module'},
            #     }
            #
            #     result = switch_dict.get(convserion_fun, switch_dict['default'])()
            #     print('value_list',value_list)
        # data_dict['get_value'] = value_list

        # conversions_list(data_dict,"kpi")


        # print('d', datapoint_value)
#
#
# def test(instance):
#     machine_id = instance.Machine_Id
#     time_stamp = instance.Timestamp
#     # print('machine_id',machine_id)
#     get_data = MachineCardsList.objects.filter(Machine_Id__Machine_id=machine_id)
#     print('get_data',get_data)
#     value_data=[]
#     for data in get_data:
#         # print('???????????',data.DataPoints[0])
#
#         get_convserion_fun = data.Conversion_Fun
#         switch_dict = {
#             "Live": lambda: live_values.append(call_live_function(data_dict)),
#             "Average": lambda: average_values.append(Average()),  # Assuming 'Average' function returns a value
#             # Add other conversion functions as needed
#             'default': lambda: {"status": 'please give correct module'},
#         }



