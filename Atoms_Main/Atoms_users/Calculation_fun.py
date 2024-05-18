from datetime import datetime
from Atoms_machines.models import CardsRawData,MachineRawData
from datetime import datetime, date

from django.db.models import Avg,F,Count

from .all_types_of_alarm import demo_alarm


def Live_new_record(data_dict):
    value = data_dict['get_value']

    return value

def Live(data_dict):
    value = data_dict['get_value']

    return value


def Average(data_dict,datapoint):
    today = date.today()
    first_record_today = MachineRawData.objects.filter(Timestamp__date=today).latest('-Timestamp')
    start_of_day = first_record_today.Timestamp
    # print('start_of_day',start_of_day)
    latest_record_today = MachineRawData.objects.filter(Timestamp__date=today).latest('Timestamp')
    # print('latest_record_today',latest_record_today)

    end_of_day = latest_record_today.Timestamp
    records_today = MachineRawData.objects.filter(Timestamp__date=today)
    # print('records_today',len(records_today))
    result=[]

    # for d in datapoint:
    # print('datapoint',datapoint)



    datapoints_split = datapoint.split('[')
    datapoints_split1 = datapoints_split[1].split(']')
    # print('datapoints_split',datapoints_split)
    # print('datapoints_split1',datapoints_split1)
    field = str(datapoints_split[0] + "__" + datapoints_split1[0])
    # print('//////////////',datapoints_split[0]+"__"+datapoints_split1[0])
    # Calculate average of analog_input[0] for today's records
    average_analog_input = records_today.aggregate(avg_analog_input=Avg(F(field)))
    result.append(average_analog_input['avg_analog_input'])

        # The result will be in average_analog_input['avg_analog_input']
    # print("Average :", average_analog_input)
    # print("Average analog_input[0] for today:", average_analog_input['avg_analog_input'])
    # print("Averag res:", result)
    avg_res=float(result[0])
    # avg_data = [float(val) for val in result if val is not None]
    rounded_avg_res = round(avg_res, 2)
    # print("avg_data res:", avg_data)
    # print("Averag res:", rounded_avg_res)


    return rounded_avg_res


def High_Low(data_dict):
    pass

def RunTime(datapoint):
    # print('runtime')
   today = date.today()

   todays_records = MachineRawData.objects.filter(Timestamp__date=today)
   # print('todays_records runtime', todays_records[0])
   datapoints_split = datapoint.split('[')
   datapoints_split1 = datapoints_split[1].split(']')
   field = str(datapoints_split[0] + "__" + datapoints_split1[0])
   # print('//////////////',datapoints_split[0]+"__"+datapoints_split1[0])
   # Calculate average of analog_input[0] for today's records
   count_datapoint= todays_records.aggregate(count_data=Count(F(field)))
   # print('')
   # print('counttttt',count_datapoint['count_data'])
   on_count = (todays_records.filter(**{field: True}).count())*5
   off_count = (todays_records.filter(**{field: False}).count())*5

   # print(f"Count of 'on' for {field}: {on_count}")
   # print(f"Count of 'off' for {field}: {off_count}")
   count_result=[on_count, off_count]
   return count_result


def History(data_dict,datapoint):

    pass

def alarm1(data_dict,datapoint):
    # print('alarm1............',data_dict)
    print('alarm1........222....',datapoint)
    # {'time_stamp': '2024-05-18T12:38:42', 'machine_id': 'AA_001', 'get_name': ['Alarm'], 'get_value': 'Off', 'get_title': 'Alarm', 'get_mode': ['Alarm_
    # fun']}

    machine_id='AA_001'
    grp="demo"
    if grp == "demo":

        latest_record = MachineRawData.objects.filter(Machine_Id=machine_id).order_by('-id').first()

        previous_record = MachineRawData.objects.filter(Machine_Id=machine_id,
                                                            id__lt=latest_record.id).order_by('-id').first()
        demo_alarm(data_dict, datapoint, latest_record, previous_record)
    else:
        pass







def History_result(data_dict):
    pass

def Alarm_fun(data_dict):
    print('alarm funnnn............')

    pass



def New_Record(data_dict):

    # print('data_dict......................',data_dict)
    # print('time_stamp......................',data_dict['time_stamp'])
    kp_raw_data_storing = CardsRawData.objects.create(
        Timestamp=data_dict['time_stamp'],
        # Timestamp=datetime.now().isoformat().split('.')[0],
        Machine_Id=[data_dict["machine_id"]],#list many to many
        Name = data_dict['get_name'],#list machinecard names in list
        Value= data_dict['get_value'], #datapoint in list
        Title = data_dict['get_title'],
        Mode=data_dict['get_mode']
    )
    kp_raw_data_storing.save()


def Day(data_dict):
    # print('day datadict.................',data_dict)
    today = datetime.now().date()
    kpi_data_queryset = CardsRawData.objects.filter(Machine_Id__contains=[data_dict['machine_id']], Title=data_dict['get_title'],
                                                        Timestamp__date=today,Mode=data_dict['get_mode'])
    # print('kpi_data_queryset', kpi_data_queryset)
    # result_get_values=str_list_rawvalue(data_dict)
    # print('data_dict',data_dict['get_value'])

    if kpi_data_queryset.exists():
        # Update the existing record(s) for cumulative data
        kpi_data_queryset.update(Value=data_dict['get_value'], Timestamp=data_dict["time_stamp"])

    else:
        # Create a new record for cumulative data if it doesn't exist
        # card_raw_data = CardsRawData.objects.create(
        #     Timestamp=data_dict['time_stamp'],
        #     Title=data_dict['get_title'],
        #     Mode=data_dict['get_mode']
        # )
        # for machine_id in data_dict["machine_id"]:
        #     card_raw_data.Machine_Id.add(machine_id)
        #     card_raw_data.Name.add(data_dict['get_name'])
        #     card_raw_data.Value.add(data_dict['get_value'])

        new_record_today=CardsRawData.objects.create(
            Timestamp=data_dict['time_stamp'],
            Machine_Id=[data_dict["machine_id"]],  # list many to many
            Name=data_dict['get_name'],  # list machinecard names in list
            Value=data_dict['get_value'],  # datapoint in list
            Title=data_dict['get_title'],
            Mode=data_dict['get_mode']
        )
        new_record_today.save()


def Month(data_dict):
    today = datetime.now().date()
    kpi_data_queryset = CardsRawData.objects.filter(Machine_Id__contains=[data_dict['machine_id']],
                                                    Title=data_dict['get_title'],
                                                    Timestamp__date=today,Mode=data_dict['get_mode'])
    # print('kpi_data_queryset', kpi_data_queryset)
    # result_get_values=str_list_rawvalue(data_dict)
    # print('data_dict', data_dict['get_value'])

    if kpi_data_queryset.exists():
        # Update the existing record(s) for cumulative data
        kpi_data_queryset.update(Value=data_dict['get_value'], Timestamp=data_dict["time_stamp"])

    else:
        # Create a new record for cumulative data if it doesn't exist
        new_record_today1 = CardsRawData.objects.create(
            Timestamp=data_dict['time_stamp'],
            Machine_Id=[data_dict["machine_id"]],  # list many to many
            Name=data_dict['get_name'],  # list machinecard names in list
            Value=data_dict['get_value'],  # datapoint in list
            Title=data_dict['get_title'],
            Mode=data_dict['get_mode']
        )
        new_record_today1.save()
            # CardsRawData.objects.create(
            #     Timestamp=data_dict['time_stamp'],
            #     Machine_Id=[data_dict["machine_id"]],  # list many to many
            #     Name=data_dict['get_name'],  # list machinecard names in list
            #     Value=data_dict['get_value'],  # datapoint in list
            #     Title=data_dict['get_title'],
            #     Mode=data_dict['get_mode']
            # )

#
# def Average():
#     pass
#
# def High_Low(data_dict):
#     pass
#     # # datapoints = data_kpi.data_points[0]  # split coulumn_name and  value
#     # # # print('datapoints', datapoints)
#     # # kpiname = data_kpi.kpi_name
#     # # # print('kpiname',kpiname)
#     # # datapoints_split = datapoints.split('[')
#     # # col = datapoints_split[0]
#     # # index = int(datapoints_split[1][:-1])
#     # # # print('.........','col',col,'\\\\','index',index)
#     # #
#     # # # kpi_data = getattr(instance,datapoints)
#     # # # kpi_data = eval(f'instance.{datapoints}')
#     # # # print('kpidata',kpi_data)
#     # #
#     # # # print('..................................',datapoints,'??????????',kpiname,'///////',kpi_data)
#     # first_record = MachineDetails.objects.filter(machine_id=machine_id, timestamp__date=today).latest(
#     #     'timestamp')
#     #
#     # min_max_data_query = MachineDetails.objects.filter(machine_id=machine_id, timestamp__date=today)
#     # # print('min_max_data_query',min_max_data_query)
#     # lowest = getattr(first_record, f"{col}")[index]
#     # # print('lowest',lowest)
#     # highest = getattr(first_record, f"{col}")[index]
#     # # print('highest',highest)
#     # min_max_data_query = MachineDetails.objects.filter(machine_id=machine_id, timestamp__date=today)
#     #
#     # for m in range(len(min_max_data_query)):
#     #     # print('mmmmmmmmmmmmm',m)
#     #     # print('indexxx',index)
#     #     record_data = getattr(min_max_data_query[m], f"{col}")
#     #     record_data = record_data[index]
#     #     # record_data = getattr(min_max_data_query[m], f"{col}")[index]
#     #     # print('record_data',record_data)
#     #     if record_data > highest:
#     #         highest = record_data
#     #     elif record_data < lowest:
#     #         lowest = record_data
#     #
#     #     # print('min ',str(lowest), "max",str(highest))
#     #     high_low_result = [lowest, highest]
#     #     # print('high_low_result',high_low_result)
#     #
#     # kpi_data_queryset = Machine_KPI_Data.objects.filter(machine_id=machine_id, kpi_id__kpi_name=kpiname,
#     #                                                     timestamp__date=today)
#     # # print('kpi_data_queryset', kpi_data_queryset)
#     # # print('kpiname', kpiname)
#     #
#     # # print('counttt', kpi_data_queryset.count())#10517
#     #
#     # if kpi_data_queryset.exists():
#     #     # Update the existing record(s) for cumulative data
#     #     kpi_data_queryset.update(kpi_data=high_low_result, timestamp=time_stamp)
#     # else:
#     #     # Create a new record for cumulative data if it doesn't exist
#     #     Machine_KPI_Data.objects.create(
#     #         machine_id=machine_id,
#     #         kpi_id=data.kpi,
#     #         kpi_data=high_low_result,
#     #         timestamp=time_stamp
#     #     )
#
#
# def Cummulative():
#     pass
#
# def conversions_list(data_dict,method):
#     today = datetime.now().date()
#     kpi_data_queryset = CardsRawData.objects.filter(Machine_Id__contains=[data_dict['machine_id']],
#                                                     Title=data_dict['get_title'],
#                                                     Timestamp__date=today)
#     # print('kpi_data_queryset', kpi_data_queryset)
#     # result_get_values=str_list_rawvalue(data_dict)
#     print('data_dict', data_dict['get_value'])
#
#     if kpi_data_queryset.exists():
#         # Update the existing record(s) for cumulative data
#         if method == "kpi":
#             kpi_data_queryset.update(Value=data_dict['get_value'], Timestamp=data_dict["time_stamp"])
#         elif method == "dashboard":
#             return data_dict['get_value']
#     else:
#         # Create a new record for cumulative data if it doesn't exist
#         if method == "kpi":
#
#             CardsRawData.objects.create(
#                 Timestamp=data_dict['time_stamp'],
#                 Machine_Id=[data_dict["machine_id"]],  # list many to many
#                 Name=data_dict['get_name'],  # list machinecard names in list
#                 Value=data_dict['get_value'],  # datapoint in list
#                 Title=data_dict['get_title'],
#                 Mode=data_dict['get_mode']
#             )
#         elif method == "dashboard":
#             return data_dict['get_value']
#
#     pass
#
#
# def Energy_card(data_dict):
#     today = datetime.now().date()
#
#     kpi_data_queryset = CardsRawData.objects.filter(Machine_Id=data_dict["machine_id"], Name=data_dict['get_name'],
#                                                         Timestamp__date=today)
#     # print('kpi_data_queryset',kpi_data_queryset)
#     if kpi_data_queryset.exists():
#
#         kpi_data_queryset.update(Value=data_dict['get_value'], Timestamp=data_dict['time_stamp'])
#     else:
#         CardsRawData.objects.create(
#             Timestamp=data_dict['time_stamp'],
#             Machine_Id=[data_dict["machine_id"]],  # list many to many
#             Name=data_dict['get_name'],  # list machinecard names in list
#             Value=data_dict['get_value'],  # datapoint in list
#             Title=data_dict['get_title'],
#             Mode=data_dict['get_mode']
#         )
#
