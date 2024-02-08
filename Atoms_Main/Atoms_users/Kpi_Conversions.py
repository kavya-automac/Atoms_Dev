
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
        print('datapoint',datapoint)

        datapoint_value=[]
        for i in range(len(datapoint)):
            d_i_o = eval(f'instance.{datapoint[i]}')
            if str(d_i_o).lower() == "true":
                d_i_o = "On"
            elif str(d_i_o).lower() == "false":
                d_i_o = "Off"
            print('d_i_o',d_i_o)
            datapoint_value.append(d_i_o)
        print('d',datapoint_value)

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
            "Cummulative": lambda: Cummulative(),
            "Energy_card": lambda: Energy_card(data_dict),

            'default': lambda: {"status": 'please give correct module'},
        }

        # Execute the corresponding function from the switch_dict or the default function
        result = switch_dict.get(get_convserion_fun, switch_dict['default'])()

        # print('get_convserion_fun',get_convserion_fun)





