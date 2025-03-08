import re
from datetime import datetime
from decimal import Decimal

from Atoms_machines.models import CardsRawData,MachineRawData
from datetime import datetime, date

from django.db.models import Avg,F,Count

from .all_types_of_alarm import demo_alarm
import logging
# from Atoms_Main.settings import DATABASES
# import psycopg2
from django.db import connection
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models import Q
from django.core.cache import cache



logger = logging.getLogger("django")

#
# try:
#     # Establish the connection
#     connection = psycopg2.connect(
#         host=DATABASES["default"]["HOST"],
#         port=DATABASES["default"]["PORT"],
#         database=DATABASES["default"]["NAME"],
#         user=DATABASES["default"]["USER"],
#         password=DATABASES["default"]["PASSWORD"]
#     )
#
#     # Create a cursor object
#     cursor = connection.cursor()
#
#
# except Exception as error:
#     print("Error while connecting to PostgreSQL:", error)
# finally:
#     # Close the connection when done
#     if connection:
#         cursor.close()
#         connection.close()
#         print("PostgreSQL connection is closed")
#




# {'time_stamp': '2025-03-04T13:37:01', 'machine_id': 'MAPL100024090060',
    #  'get_name': ['Water Generated', 'Energy Consumed', 'Machine Run Ti
    #               me', 'Machine Idle Time', 'Water Level', 'Average Temperature', 'Average Humidity', 'Average DP'], '
    #               get_value': 11.76, 'get_title': 'Summary', 'get_mode': ['Day']}
    # datapoint
    # Analog_Input[2]

def Live_new_record(data_dict):
    value = data_dict['get_value']

    return value

def Live(data_dict):
    value = data_dict['get_value']

    return value


def Average1(data_dict,datapoint):
    print("in average")
    # today = date.today()

    machine_timestamp = data_dict['time_stamp']
    # print("machine_timestamp mode", machine_timestamp)
    timestamp_tostring = datetime.strptime(machine_timestamp, "%Y-%m-%dT%H:%M:%S")
    machine_date_tp = timestamp_tostring.date()

    first_record_today = MachineRawData.objects.filter(Timestamp__date=machine_date_tp,Machine_Id=data_dict["machine_id"]).latest('-Timestamp')
    start_of_day = first_record_today.Timestamp
    # print('start_of_day',start_of_day)
    latest_record_today = MachineRawData.objects.filter(Timestamp__date=machine_date_tp,Machine_Id=data_dict["machine_id"]).latest('Timestamp')
    # print('latest_record_today',latest_record_today)

    end_of_day = latest_record_today.Timestamp
    records_today = MachineRawData.objects.filter(Timestamp__date=machine_date_tp,Machine_Id=data_dict["machine_id"])
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
    print("average done")


    return rounded_avg_res


from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models import Q
from decimal import Decimal


def Maithri_at_nine(data_dict, datapoint):
    """Fetches the first available 9-10 AM record for today and yesterday,
    then calculates the difference. Returns 0 if no data is found."""

    def get_first_record(date):
        """Fetches the first record in the 9-10 AM range for the given date."""
        start_time = make_aware(datetime.combine(date, datetime.min.time()).replace(hour=9, minute=0))
        end_time = make_aware(datetime.combine(date, datetime.min.time()).replace(hour=10, minute=0))

        return MachineRawData.objects.filter(
            Timestamp__gte=start_time, Timestamp__lt=end_time,
            Machine_Id=data_dict['machine_id']
        ).order_by('Timestamp').first()

    # Extract column and index from datapoint (e.g., "Analog_Input[2]" → col="Analog_Input", index=2)
    try:
        col, index = datapoint.split('[')
        print("col",col)
        index = int(index[:-1])  # Remove closing bracket and convert to int
        print("index",index)
    except Exception as e:
        print("Invalid datapoint format:", datapoint, "Error:", e)
        return 0

    # Fetch today's first record (9-10 AM)
    first_record_today = get_first_record(datetime.today().date())
    print("first_record_today",first_record_today)

    if not first_record_today:
        return 0  # No data for today

    # Extract today's value
    try:
        today_value = getattr(first_record_today, col)[index]
        print("today_value",today_value)
    except Exception as e:
        print("Error fetching today's value:", e)
        return 0

    # Fetch yesterday's first record (9-10 AM)
    first_record_yesterday = get_first_record(datetime.today().date() - timedelta(days=1))
    print("first_record_yesterday",first_record_yesterday)
    if not first_record_yesterday:
        return 0  # No data for yesterday

    # Extract yesterday's value and compute the difference
    try:
        yesterday_value = getattr(first_record_yesterday, col)[index]
        print("yesterday_value",yesterday_value)
        print(today_value - Decimal(yesterday_value))
        return today_value - Decimal(yesterday_value)
    except Exception as e:
        print("Error fetching yesterday's value:", e)
        return 0


#
# def Maithri_at_nine(data_dict,datapoint):
#     # #Get current datetime and today's date
#     now = datetime.now()
#     today = now.date()
#     todays_date = datetime.today().date()
#     print('data_dict Maithri_at_nine',data_dict)
#     print('today',today)
#
#     # Define the 9-10 AM time range for today
#     start_time = make_aware(datetime.combine(today, datetime.min.time()).replace(hour=9, minute=0))
#     end_time = make_aware(datetime.combine(today, datetime.min.time()).replace(hour=10, minute=0))
#     print(start_time,"and",end_time)
#
#     # Get today's first record within 9-10 AM
#     first_record_today = MachineRawData.objects.filter(
#         Q(Timestamp__gte=start_time) & Q(Timestamp__lt=end_time),
#         Machine_Id=data_dict['machine_id'],  # Replace with the actual machine ID
#     ).order_by('Timestamp').first()  # Get earliest record
#
#     print("datapoint",datapoint)
#     print("first_record_today",first_record_today)
#     # print("first_record_analog today",first_record_today.Analog_Output[0])
#
#     if first_record_today:
#         datapoints_split = datapoint.split('[')
#         col = datapoints_split[0]
#         index = int(datapoints_split[1][:-1])
#         print('.........', 'col', col, '\\\\', 'index', index)
#         data = getattr(first_record_today, f"{col}")[index]
#         print('datadata', data)
#         print('typee  datadata', type(data))
#         print("if first_record_today")
#         today_value = data  # Fetching Analog_Input[2] value
#     else:
#         return 0  # No record for today in the given time range
#
#     print("data_dict",data_dict)
#     print("todays_date",todays_date)
#
#
#
#     # Get yesterday's date
#     yesterday = datetime.today().date() - timedelta(days=1)
#
#     # Define start and end time for 9 AM - 10 AM yesterday
#     start_time = make_aware(datetime.combine(yesterday, datetime.min.time()).replace(hour=9, minute=0))
#     end_time = make_aware(datetime.combine(yesterday, datetime.min.time()).replace(hour=10, minute=0))
#
#     print(start_time, "and", end_time)
#
#     # Get yesterday's first record within 9-10 AM
#     first_record_yesterday = MachineRawData.objects.filter(
#         Q(Timestamp__gte=start_time) & Q(Timestamp__lt=end_time),
#         Machine_Id=data_dict['machine_id'],  # Replace with the actual machine ID
#     ).order_by('Timestamp').first()
#
#     print("first_record_yesterday:", first_record_yesterday)
#
#     # If data is found, calculate difference; otherwise, return 0
#     if first_record_yesterday:
#         try:
#             datapoints_split = datapoint.split('[')
#             col = datapoints_split[0]
#             index = int(datapoints_split[1][:-1])
#             print('.........', 'col', col, '\\\\', 'index', index)
#
#             yesterday_value = getattr(first_record_yesterday, f"{col}")[index]
#             return today_value - Decimal(yesterday_value)
#
#         except Exception as e:
#             print("Error:", e)
#             return 0  # If any error occurs, return 0
#     else:
#         return 0  # If no data found for yesterday, return 0



# def Maithri_at_nine(data_dict, datapoint):
#     now = datetime.now()
#     today = now.date()
#
#     # Define the cache key
#     cache_key = f"first_record_{data_dict['machine_id']}_{today}"
#     print('cache_key',cache_key)
#     # Check cache before querying DB
#     first_record_today = cache.get(cache_key)
#     print('first_record_today cache',first_record_today)
#
#     if not first_record_today:
#         # Define 9-10 AM time range
#         start_time = make_aware(datetime.combine(today, datetime.min.time()).replace(hour=9, minute=0))
#         end_time = make_aware(datetime.combine(today, datetime.min.time()).replace(hour=10, minute=0))
#
#         # Query first record of today between 9-10 AM
#         first_record_today = MachineRawData.objects.filter(
#             Q(Timestamp__gte=start_time) & Q(Timestamp__lt=end_time),
#             Machine_Id=data_dict['machine_id']
#         ).order_by('Timestamp').first()
#
#         if first_record_today:
#             # Store result in cache to prevent redundant queries
#             cache.set(cache_key, first_record_today, timeout=3600 * 24)  # Cache for 24 hours
#
#     if not first_record_today:
#         return 0  # No data found for today
#
#     # Extract datapoint value
#     datapoints_split = datapoint.split('[')
#     col = datapoints_split[0]
#     index = int(datapoints_split[1][:-1])
#     today_value = getattr(first_record_today, col)[index]
#
#     # Fetch previous day's record
#     first_record_previous = CardsRawData.objects.filter(
#         Machine_Id__contains=[data_dict['machine_id']],
#         Title=data_dict['get_title'],
#         Timestamp__date__lt=str(today),
#         Mode=data_dict['get_mode'][0]
#     ).order_by('-Timestamp').first()
#     print("today_value",today_value)
#     if first_record_previous:
#         try:
#             yesterday_value = first_record_previous.Value[8]
#             print("yesterday_value",yesterday_value)
#             print(today_value - Decimal(yesterday_value))
#             return today_value - Decimal(yesterday_value)
#         except Exception as e:
#             print("Error:", e)
#
#     return today_value  # No previous record, return today's value as is







def Average(data_dict,datapoint):

    print("datapoint",datapoint)
    machine_timestamp = data_dict['time_stamp']
    # print("machine_timestamp mode", machine_timestamp)
    timestamp_tostring = datetime.strptime(machine_timestamp, "%Y-%m-%dT%H:%M:%S")
    machine_date_tp = timestamp_tostring.date()
    # datapoints_split = datapoint.split('[')
    # datapoints_split1 = datapoints_split[1].split(']')

    # converted_text = re.sub(r'(\w+)(\[\d+\])', r'"\1"\2', datapoint)
    # output_str = re.sub(r'\[(\d+)\]', lambda x: f"[{int(x.group(1)) + 1}]", datapoint)

    match = re.match(r"([a-zA-Z_]+)\[(\d+)\]", datapoint)
    print("..........", match)

    if match:
        text_part = match.group(1)  # "Analog_input"
        index_part = int(match.group(2)) + 1  # Increment the index
        output_str = f'"{text_part}"[{index_part}]'
        print(output_str)  # Outputs: "Analog_input"[3]
    else:
        print("Invalid format")

    print("converted_text", output_str)  # Now using output_str as the converted text

    # Use output_str in the query
    query = f"""
            SELECT AVG(field) AS avg_dp
            FROM (
                SELECT DISTINCT 
                    "Timestamp",
                    {output_str} AS field,
                    "Machine_Id"
                FROM 
                   postgres."Machines_Schema"."MachineRawData" 
                WHERE 
                    "Machine_Id" = %s 
                    AND DATE("Timestamp") = %s
            ) AS distinct_records;
        """

    # match = re.match(r"([a-zA-Z_]+)\[(\d+)\]", datapoint)
    # print("..........",match)
    #
    # if match:
    #     text_part = match.group(1)  # "Analog_input"
    #     index_part = int(match.group(2)) + 1  # Increment the index
    #     output_str = f'"{text_part}"[{index_part}]'
    #     print(output_str)  # Outputs: "Analog_input"[3]
    # else:
    #     print("Invalid format")
    #
    #
    # print("converted_text",match)
    #
    # query = """
    #         SELECT AVG(field) AS avg_dp
    #         FROM (
    #             SELECT DISTINCT
    #                 "Timestamp",
    #                 """+ match+""" AS field,
    #                 "Machine_Id"
    #             FROM
    #                postgres."Machines_Schema"."MachineRawData"
    #             WHERE
    #                 "Machine_Id" = %s
    #                 AND DATE("Timestamp") = %s
    #         ) AS distinct_records;
    #     """

    # Execute the raw SQL query
    with connection.cursor() as cursor:
        cursor.execute(query, [data_dict["machine_id"], machine_date_tp])
        avg_dp = cursor.fetchone()[0]  # Fetch the result of the AVG calculation
    avg_res = round(avg_dp, 2)
    print("avg_res.........",avg_res)

    return avg_res

#
# # Example usage
# machine_id = 'MAPL100024090060'
# date = '2024-10-27'
# average_dp = get_avg_dp(machine_id, date)
# print("Average DP:", average_dp)








def High_Low(data_dict):
    pass




def RunTime(data_dict,datapoint):
    machine_timestamp = data_dict['time_stamp']
    # print("machine_timestamp mode", machine_timestamp)
    timestamp_tostring = datetime.strptime(machine_timestamp, "%Y-%m-%dT%H:%M:%S")
    machine_date_tp = timestamp_tostring.date()
    print("runtime machine_date_tp",machine_date_tp)


    match = re.match(r"([a-zA-Z_]+)\[(\d+)\]", datapoint)
    print("....runtime.", match)

    if match:
        text_part = match.group(1)  # "Analog_input"
        index_part = int(match.group(2)) + 1  # Increment the index
        output_str = f'"{text_part}"[{index_part}]'
        print(output_str)  # Outputs: "Analog_input"[3]
    else:
        print("Invalid format")

    print("converted_text   runtime ", output_str)  # Now using output_str as the converted text

    query1 = f"""
        SELECT 
        COUNT(CASE WHEN status = true THEN 1 END) AS on_count,
        COUNT(CASE WHEN status = false THEN 1 END) AS off_count
    FROM 
        ( 
        SELECT DISTINCT 
            "Timestamp", 
            {output_str} as status,
            "Machine_Id"
        FROM 
            postgres."Machines_Schema"."MachineRawData" 
        WHERE 
            "Machine_Id" = %s
            AND DATE("Timestamp") = %s
        ) AS distinct_records;
            """

    with connection.cursor() as cursor:
        cursor.execute(query1, [data_dict["machine_id"], machine_date_tp])
        on_off_count = cursor.fetchone()
    print("on_off_count",on_off_count)

    on_count_res = on_off_count[0] * 60
    off_count_res = on_off_count[1] * 60

    result = [on_count_res,off_count_res]

    return result







def RunTime1(data_dict,datapoint):
    print(" in RunTime")
    # print('runtime datapoint',datapoint)
    # print('data_dict datapoint',data_dict)
    # print('data_dict machine',data_dict["machine_id"])

    machine_timestamp = data_dict['time_stamp']
    # print("machine_timestamp mode", machine_timestamp)
    timestamp_tostring = datetime.strptime(machine_timestamp, "%Y-%m-%dT%H:%M:%S")
    machine_date_tp = timestamp_tostring.date()

    # today = date.today()
    # print('today.......',today)
    todays_records = MachineRawData.objects.filter(Timestamp__date=machine_date_tp,Machine_Id=data_dict["machine_id"])  #add distinct timestamp if we add distinct aggregate will not work
    print('count runtime query',todays_records.count())
    # print('todays_records runtime', todays_records[0])
    datapoints_split = datapoint.split('[')
    datapoints_split1 = datapoints_split[1].split(']')
    field = str(datapoints_split[0] + "__" + datapoints_split1[0])
    # print('//////////////',datapoints_split[0]+"__"+datapoints_split1[0])
    # Calculate average of analog_input[0] for today's records
    count_datapoint= todays_records.aggregate(count_data=Count(F(field)))
    # print('')
    # print('counttttt',count_datapoint['count_data'])
    on_count = (todays_records.filter(**{field: True}).count())*60
    # on_count = (todays_records.filter(**{field: True}).count())
    off_count = (todays_records.filter(**{field: False}).count())*60
    # off_count = (todays_records.filter(**{field: False}).count())
    # print(f"Count of 'on' for {field}: {on_count}")
    # print(f"Count of 'off' for {field}: {off_count}")
    count_result=[on_count, off_count]
    print('count_result',count_result)
    print("RunTime dome")

    return count_result


def Mode_(data_dict,datapoint):
    print("in mode_")
    # today = date.today()
    machine_timestamp_mode = data_dict['time_stamp']
    # print("machine_timestamp mode", machine_timestamp_mode)
    timestamp_tostring = datetime.strptime(machine_timestamp_mode, "%Y-%m-%dT%H:%M:%S")
    machine_date_tp = timestamp_tostring.date()
    # print('macine_id in mode_',data_dict["machine_id"])


    todays_records = MachineRawData.objects.filter(Timestamp__date=machine_date_tp,Machine_Id=data_dict["machine_id"])  # add distinct timestamp
    # print('todays_records runtime', todays_records[0])
    datapoints_split = datapoint.split('[')
    datapoints_split1 = datapoints_split[1].split(']')
    field = str(datapoints_split[0] + "__" + datapoints_split1[0])#other__0

    query_data = (MachineRawData.objects.values(field).annotate(count=Count(field)).order_by('-count').first())

    # print('field',field)
    # print('query_data',query_data)
    mode_data = query_data[field] if query_data else None
    # print("mode_data",mode_data)
    print("mode_ done")
    return mode_data




def RunTime_HMS(data_dict,datapoint):
    print(" in RunTime_HMS")
    total_sec = RunTime(data_dict,datapoint)

    hours = total_sec[0] // 3600
    minutes = (total_sec[0] % 3600) // 60
    seconds = total_sec[0] % 60

    hours1 = total_sec[1] // 3600
    minutes1 = (total_sec[1] % 3600) // 60
    seconds1 = total_sec[1] % 60

    total_res =[f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}",f"{int(hours1):02}:{int(minutes1):02}:{int(seconds1):02}"]
    print("total_res",total_res)
    print("RunTime_HMS done")
    return total_res
    # return total_res[0],total_res[1]




def History(data_dict,datapoint):

    pass

def alarm1(data_dict,datapoint):
    # print('alarm1............',data_dict)
    # print('alarm1........222....',datapoint)
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
    # print('alarm funnnn............')

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
    # today = datetime.now().date()
    machine_timestamp = data_dict['time_stamp']
    print("machine_timestamp day", machine_timestamp)
    timestamp_tostring = datetime.strptime(machine_timestamp,"%Y-%m-%dT%H:%M:%S")
    machine_date = timestamp_tostring.date()
    print("machine_date day",machine_date)

    kpi_data_queryset = CardsRawData.objects.filter(Machine_Id__contains=[data_dict['machine_id']], Title=data_dict['get_title'],
                                                        Timestamp__date=machine_date,Mode=data_dict['get_mode'])

    # logger.info('day exception after query t: %s', e)
    # result_get_values=str_list_rawvalue(data_dict)
    # print('data_dict',data_dict['get_value'])

    # if kpi_data_queryset:
    if kpi_data_queryset.exists():


        kpi_data_queryset.update(Value=data_dict['get_value'], Timestamp=data_dict["time_stamp"])
        print('update query exception after')

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
