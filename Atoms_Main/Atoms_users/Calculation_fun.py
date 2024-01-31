from datetime import datetime
from Atoms_machines.models import CardsRawData


def Live_new_record(data_dict):

    print('data_dict......................',data_dict)
    CardsRawData.objects.create(
        Timestamp=data_dict['time_stamp'],
        Machine_Id=[data_dict["machine_id"]],#list many to many
        Name = data_dict['get_name'],#list machinecard names in list
        Value= data_dict['get_value'], #datapoint in list
        Title = data_dict['get_title'],
        Mode=data_dict['get_mode']
    )


def Live(data_dict):
    today = datetime.now().date()
    kpi_data_queryset = CardsRawData.objects.filter(Machine_Id__contains=[data_dict['machine_id']], Title=data_dict['get_title'],
                                                        Timestamp__date=today)
    # print('kpi_data_queryset', kpi_data_queryset)
    # result_get_values=str_list_rawvalue(data_dict)
    print('data_dict',data_dict['get_value'])
    if kpi_data_queryset.exists():
        # Update the existing record(s) for cumulative data
        kpi_data_queryset.update(Value=data_dict['get_value'], Timestamp=data_dict["time_stamp"])
    else:
        # Create a new record for cumulative data if it doesn't exist

        CardsRawData.objects.create(
            Timestamp=data_dict['time_stamp'],
            Machine_Id=[data_dict["machine_id"]],  # list many to many
            Name=data_dict['get_name'],  # list machinecard names in list
            Value=data_dict['get_value'],  # datapoint in list
            Title=data_dict['get_title'],
            Mode=data_dict['get_mode']
        )


def Average():
    pass

def High_Low():
    pass
def Cummulative():
    pass

def Energy_card(data_dict):
    today = datetime.now().date()

    kpi_data_queryset = CardsRawData.objects.filter(Machine_Id=data_dict["machine_id"], Name=data_dict['get_name'],
                                                        Timestamp__date=today)
    # print('kpi_data_queryset',kpi_data_queryset)
    if kpi_data_queryset.exists():

        kpi_data_queryset.update(Value=data_dict['get_value'], Timestamp=data_dict['time_stamp'])
    else:
        CardsRawData.objects.create(
            Timestamp=data_dict['time_stamp'],
            Machine_Id=[data_dict["machine_id"]],  # list many to many
            Name=data_dict['get_name'],  # list machinecard names in list
            Value=data_dict['get_value'],  # datapoint in list
            Title=data_dict['get_title'],
            Mode=data_dict['get_mode']
        )

