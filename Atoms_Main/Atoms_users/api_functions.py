# import datetime
from datetime import datetime, timezone, timedelta

import pytz
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from .Nested_Queries import *
from .conversions import *
from Atoms_machines.models import CardsRawData,MachineRawData
from django.db.models import F, CharField, Value
from django.db.models.functions import Cast
from asgiref.sync import sync_to_async



def dropdown(user_id):

    # user_id=6
    user_lr=get_node_LR(user_id, "User")
    # print('user_lr',user_lr)
    # data = {'left': left_v, "right": right_v}

    data = get_grandparent(user_lr['left'], user_lr['right'])
    grand_left=data['grandparent']['grandparent_l']
    grand_right=data['grandparent']['grandparent_r']
    # print('left',data['grandparent']['grandparent_l'])
    # print('right',data['grandparent']['grandparent_r'])

    des = get_descendent(grand_left, grand_right, "Layer","node_lr")
    # print('des',des)
    result=[]
    for i in des['descendents']:
        layer_parents= Parent_nodes(i["node_left"],i["node_right"],grand_left,grand_right)
        # print('p...........',layer_parents)
        # get_layer_details=Layers.objects.filter(id__in=layer_parents).values_list('Layer_Name',flat=True)
        get_layer_details=Layers.objects.filter(id__in=layer_parents).values('Layer_Name','Layer_Type').order_by('id')
        # print('get_layer_details',get_layer_details)
        serializer=layerSerializer(get_layer_details,many=True)
        # print('.............',serializer.data)
        node_name=serializer.data[-1]["Layer_Name"]
        # todo: "change node_id and layer(type) from using serializer instead of [-1]"
        # node_name=i["node_id"]
        parent= [name["Layer_Name"] for name in serializer.data]
        Type=serializer.data[-1]["Layer_Type"]
        result_data={"node":node_name,"node_id":i["node_id"],"type":Type,"parent":parent}
        result.append(result_data)
    return result



def Details(node_id):

    # node_id=6
    # print('type of nodeid in params',type(node_id))
    if node_id:
        get_machine_details=MachineDetails.objects.get(pk=node_id)
        detail_serializer=Details_serializer(get_machine_details)
        # print('detail_serializer',dict(detail_serializer.data))
        # print('detail_serializer manuals',detail_serializer.data['Manuals'])
        manuals_data=[dict(item) for item in detail_serializer.data['Manuals']]
        techincal_data=[dict(item) for item in detail_serializer.data['Technical_Details']]
        details=only_details_serailizers(get_machine_details)
        # print('details',details.data)

        general_data = {"general_details":details.data ,"Manuals_and_Docs":manuals_data,
                             "Techincal_Details_data":techincal_data}
        # print('dataaaa',general_data)

        return general_data
    else:
        return {"status":"please enter valid node_id"}


def Machine_Iostatus(node_id):#machine_id
    node=MachineDetails.objects.get(pk=node_id)
    machine_name=node.Machine_Name
    machine_id=node.Machine_id
    # print('machine_name iostatus',machine_name)


    if node_id:
        io_key_data=io_list_data(node_id)
        io_value_data=io_values(machine_id,"iostatus")
        iostatus_data = key_value_merge(machine_id, io_key_data, io_value_data)
        iostatus_data["node_id"] = node_id
        iostatus_data["machine_id"] = machine_id
        iostatus_data["machine_name"] = machine_name
        iostatus_data["Time"] = io_value_data['Timestamp']


        # print('iostatus_data', iostatus_data)
        return iostatus_data

    else:
        return {"status": "please enter valid node_id"}


@sync_to_async
def Machine_Iostatus_web2(node_id):#machine_id
    node=MachineDetails.objects.get(pk=node_id)
    machine_name=node.Machine_Name
    machine_id=node.Machine_id
    # print('machine_name iostatus',machine_name)


    if node_id:
        io_key_data=io_list_data(node_id)
        io_value_data=io_values(machine_id,"iostatus")
        iostatus_data = key_value_merge(machine_id, io_key_data, io_value_data)
        iostatus_data["node_id"] = node_id
        iostatus_data["machine_id"] = machine_id
        iostatus_data["machine_name"] = machine_name
        iostatus_data["Timestamp"] = io_value_data['Timestamp']


        # print('iostatus_data', iostatus_data)
        return iostatus_data

    else:
        return {"status": "please enter valid node_id"}



def Machine_Control(node_id):
    node = MachineDetails.objects.get(pk=node_id)
    machine_name = node.Machine_Name
    machine_id = node.Machine_id

    if node_id:
        io_key_data=io_list_data(node_id)
        io_value_data=io_values(machine_id,"control")
        control_data = key_value_merge(node_id, io_key_data, io_value_data)
        control_data["node_id"] = node_id
        control_data["machine_id"] = machine_id
        control_data["machine_name"] = machine_name
        control_data["Timestamp"] = io_value_data['Timestamp']
        # print('control_data',control_data)
        return control_data
    else:
        return {"status": "please enter valid node_id"}


@sync_to_async

def Machine_Control_web2(node_id):
    node = MachineDetails.objects.get(pk=node_id)
    machine_name = node.Machine_Name
    machine_id = node.Machine_id

    if node_id:
        io_key_data=io_list_data(node_id)
        io_value_data=io_values(machine_id,"control")
        control_data = key_value_merge(node_id, io_key_data, io_value_data)
        control_data["node_id"] = node_id
        control_data["machine_id"] = machine_id
        control_data["machine_name"] = machine_name
        control_data["Timestamp"] = io_value_data['Timestamp']
        # print('control_data',control_data)
        return control_data
    else:
        return {"status": "please enter valid node_id"}



def machine_kpis(node_id):
    # # todays_date = datetime.now().date()
    # todays_date = "2024-02-08"
    lrvalues=get_node_LR(node_id,"Machine")
    left=lrvalues['left']
    right=lrvalues['right']
    child_kpi=get_descendent(left,right,"Kpi","node")
    # print('child_kpi',child_kpi["descendents"])
    kpinode_data=MachineCardsList.objects.filter(id__in=child_kpi["descendents"]).values('Machine_Id__Machine_id',
                                    'Title','X_Label','Y_Label','Ledger','Title','Card_type__Card_Type','Unit','mode')
    # print('kpinode_data',kpinode_data)

    result = {"resultant_data": []}  # Initialize result outside the loop

    entire_result_data=[]
    # x_axis=[]
    # y_axis=[]

    for i in kpinode_data:
        kpi_result = {}
        # print('i',i)
        switch_dict = {
            "Line": lambda: Line_bar_graph(i,entire_result_data,kpi_result,"kpis"),
            "Bar": lambda: Line_bar_graph(i,entire_result_data,kpi_result,"kpis"),
            "Text": lambda: text_card(i,entire_result_data,kpi_result,"kpis"),
            "Pie": lambda: text_card(i,entire_result_data,kpi_result,"kpis"),
            "RunTime": lambda: text_card(i,entire_result_data,kpi_result,"kpis"),
            "Status": lambda: status(i,entire_result_data,kpi_result,"kpis"),
            "Alarm": lambda: alarm(i,entire_result_data,kpi_result,"kpis"),
            'default': lambda: {"resultant_data": []},
        }

        # Execute the corresponding function from the switch_dict or the default function
        result = switch_dict.get(i['Card_type__Card_Type'], switch_dict['default'])()

    return result

@sync_to_async

def machine_kpis_web2(node_id):
    # print('llll')
    # # todays_date = datetime.now().date()
    # todays_date = "2024-02-08"
    lrvalues=get_node_LR(node_id,"Machine")
    # print('....')
    left=lrvalues['left']
    right=lrvalues['right']
    child_kpi=get_descendent(left,right,"Kpi","node")
    # print('child_kpi',child_kpi["descendents"])
    kpinode_data=MachineCardsList.objects.filter(id__in=child_kpi["descendents"]).values('Machine_Id__Machine_id',
                                    'Title','X_Label','Y_Label','Ledger','Title','Card_type__Card_Type','Unit','mode')
    # print('kpinode_data',kpinode_data)


    entire_result_data=[]
    # x_axis=[]
    # y_axis=[]

    for i in kpinode_data:
        kpi_result = {}
        print('i',i)
        switch_dict = {
            "Line": lambda: Line_bar_graph(i,entire_result_data,kpi_result,"kpis"),
            "Bar": lambda: Line_bar_graph(i,entire_result_data,kpi_result,"kpis"),
            "Text": lambda: text_card(i,entire_result_data,kpi_result,"kpis"),
            "Pie": lambda: text_card(i,entire_result_data,kpi_result,"kpis"),
            "RunTime": lambda: text_card(i,entire_result_data,kpi_result,"kpis"),
            "Status": lambda: status(i, entire_result_data, kpi_result, "kpis"),
            "Alarm": lambda: alarm(i, entire_result_data, kpi_result, "kpis"),

            'default': lambda: {"resultant_data": []},
        }

        # Execute the corresponding function from the switch_dict or the default function
        result = switch_dict.get(i['Card_type__Card_Type'], switch_dict['default'])()

    return result

def Reports_data(user_id,machine_id,start_datetime,end_datetime1,report_type):
    # print('node_id in reports_data',user_id)
    # todays_date = datetime.now().date()
    m_l_r = get_node_LR(user_id, "User")
    p_l_r = get_immediate_parent(m_l_r['left'], m_l_r['right'])

    child_kpi = get_descendent(p_l_r['immediate_parent']['immediate_left'],
                                     p_l_r['immediate_parent']['immediate_right'],
                                     "Report", "node")
    # lrvalues=get_node_LR(node_id,"Machine")
    # left=lrvalues['left']
    # right=lrvalues['right']
    # get_immediate_parent(left, right)
    # child_kpi=get_descendent(left,right,"Report","node")
    # print('child_kpi',child_kpi["descendents"])
    kpinode_data=MachineCardsList.objects.filter(id__in=child_kpi["descendents"],Title=report_type).values('Machine_Id__Machine_id',
                                    'Title','X_Label','Y_Label','Ledger','Title','Card_type__Card_Type','Unit')
    # print('kpinode_data',kpinode_data)
    entire_result_data=[]
    # x_axis=[]
    # y_axis=[]
    if kpinode_data:
        for i in kpinode_data:
            kpi_result = {}
            print('i',i)
            # print('i..........',i['Card_type__Card_Type'])
            switch_dict = {
                "Line": lambda: Line_bar_graph(i,entire_result_data,kpi_result,"reports",user_id,machine_id,start_datetime,end_datetime1,report_type),
                "Bar": lambda: Line_bar_graph(i,entire_result_data,kpi_result,"reports",user_id,machine_id,start_datetime,end_datetime1,report_type),
                "Text": lambda: text_card(i,entire_result_data,kpi_result,"reports",start_datetime,end_datetime1,report_type),
                "Pie": lambda:text_card(i,entire_result_data,kpi_result,"reports",start_datetime,end_datetime1,report_type),
                "History": lambda:Trail_Report(i,entire_result_data, kpi_result,"reports",start_datetime,end_datetime1,report_type),
                "RunTime": lambda: text_card(i, entire_result_data, kpi_result, "reports",start_datetime,end_datetime1,report_type),
                'default': lambda: {"resultant_data": []},
            }

            # Execute the corresponding function from the switch_dict or the default function
            result = switch_dict.get(i['Card_type__Card_Type'], switch_dict['default'])()


        return result
    else:
        return "no data available"

#  graphs ,text card and any calculation functions from here


def Line_bar_graph(data,entire_result_data,kpi_result,method,user_id=None,machine_id=None,start_datetime=None,end_datetime=None,report_type=None):
    # print('linee')
    formatted_datetime = datetime.now().date()
    todays_date = formatted_datetime.strftime("%Y-%m-%d")
    # print('todays_date',todays_date)

    yesterday_date=formatted_datetime - timedelta(days=2)
    # print('yesterday_date',yesterday_date)
    if method == "kpis":

        kpirawdata = CardsRawData.objects.filter(
            Machine_Id__contains=[data['Machine_Id__Machine_id']],
            Title=data['Title'],
            Timestamp__date=todays_date
        ).order_by('-Timestamp').distinct('Timestamp')
        # print('lennnnnnnnnnn',kpirawdata)
        # if kpirawdata is None: #newly added from here
        #
        #     yesterday_records = CardsRawData.objects.filter(
        #         Machine_Id__contains=[data['Machine_Id__Machine_id']],
        #         Title=data['Title'],
        #         Timestamp__date=yesterday_date
        #     ).order_by('-Timestamp')
        #
        #     # Get every 600th record from yesterday's data
        #     selected_records = yesterday_records
        #
        #     # If there are selected records, assign them to kpirawdata
        #     if selected_records:
        #         kpirawdata = selected_records
        # print('lennnnnnnnnnn', kpirawdata)# up to here
        #

    elif method == "kpiweb":
        kpirawdata = [CardsRawData.objects.filter(
            Machine_Id__contains=[data['Machine_Id__Machine_id']],
            Title=data['Title'],
            Timestamp__date=todays_date
        ).order_by('-Timestamp').latest('Timestamp')]# we will get only one record here due to for loop below kept query in list
        # if kpirawdata is None: #newly added lines
        #     yesterday_records = CardsRawData.objects.filter(
        #         Machine_Id__contains=[data['Machine_Id__Machine_id']],
        #         Title=data['Title'],
        #         Timestamp__date=yesterday_date
        #     ).order_by('-Timestamp')
        #
        #     # Get every 600th record from yesterday's data
        #     selected_records = yesterday_records[::600]
        #
        #     # If there are selected records, assign them to kpirawdata
        #     if selected_records:
        #         kpirawdata = selected_records #up to here

    elif method =="reports":

        kpirawdata = CardsRawData.objects.filter(
            Machine_Id=[machine_id],
            Title=report_type,  # Assuming there's a field for KPI ID in the Machine_KPI_Data model
            Timestamp__range=[start_datetime, end_datetime],
        ).order_by('-Timestamp').distinct('Timestamp')
        # print('kpirawdata',kpirawdata)
    elif method == "dashboard":
        dashrawdata = CardsRawData.objects.filter(
            Machine_Id__contains=[data['Machine_Id__Machine_id']],
            Title=data['Title'],
            Timestamp__date=todays_date,
            Mode=data['mode'][0]
        ).distinct('Timestamp','Mode')

        for d in dashrawdata:
            machine_id = d.Machine_Id  # Get the machine ID
            # Check if the card already exists in entire_result_data
            card_exists = False
            for card_data in entire_result_data:
                if card_data['title'] == data['Title'] and card_data['ledger'] == data['Ledger']:
                    card_exists = True
                    # Append data to existing card
                    card_data['data'].append({
                        "x_axis_data": d.Machine_Id,
                        "y_axis_data": d.Value
                    })
                    break

            if not card_exists:
                # Create a new card entry
                new_card = {
                    "card": data['Card_type__Card_Type'],
                    "title": data['Title'],
                    "ledger": data['Ledger'],
                    "labels": {
                        "x_label": data['X_Label'],
                        "y_label": data['Unit']
                    },
                    "data": [{
                        "x_axis_data": d.Machine_Id,
                        "y_axis_data": d.Value
                    }]
                }
                entire_result_data.append(new_card)

        kpi_entry = {
            'resultant_data': entire_result_data,
        }
        # print('kpi_entry', kpi_entry)

        return kpi_entry


    card_data = []
    for j in kpirawdata:
        timestamp = j.Timestamp
        # timestamp_str = timestamp.strftime('%Y-%m-%d')  # Convert datetime object to string if needed

        # print('timestamp typeeee',type(timestamp_str))
        # print('try  start_datetime',start_datetime)

        # print('jjjj', j)
        # timestamp_str = str(j.Timestamp)
        timestamp_str = j.Timestamp
        formatted_timestamp = timestamp_str.strftime("%d-%m-%Y %H:%M:%S")
        # print('Formatted time:', formatted_timestamp)




        # kpi_result_data = {"x_axis_data": timestamp_str, "y_axis_data": j.Value}
        kpi_result_data = {"x_axis_data": formatted_timestamp, "y_axis_data": j.Value}
        # print('kpi_result_data',kpi_result_data)
        card_data.append(kpi_result_data)
        # x_axis.append(j.Timestamp)
        # y_axis.append(j.Value)
    # kpi_result['x_axis']=x_axis

    kpi_result['card'] = data['Card_type__Card_Type']
    kpi_result['title'] = data['Title']
    kpi_result['ledger'] = data['Ledger']
    labels = {
        "x_label": data['X_Label'],
        "y_label": data['Y_Label']
    }
    kpi_result["labels"] = labels
    kpi_result['data'] = card_data


    entire_result_data.append(kpi_result)

    kpi_entry = {

        'resultant_data': entire_result_data,
    }
    # print('kpi_entry', kpi_entry)

    return kpi_entry

def Trail_Report(data,entire_result_data, kpi_result,method,start_datetime,end_datetime1,report_type):
    # print('start_datetime tr', start_datetime)
    # print('end_datetime tr', end_datetime1)
    if method == "reports":
       if report_type == 'History Report':

            try:
                node = MachineDetails.objects.get(Machine_id=data['Machine_Id__Machine_id'])
                node_id=node.pk
            except MachineDetails.DoesNotExist:
                error_message = "Please enter a valid node_machine_id."
                return JsonResponse({"status": error_message}, status=400)


            # print('trail report node',node)
            # print('trail report node_id',node_id)
            machine_id = node.Machine_id
            machine_name = node.Machine_Name
            # print('trail report machine_id', machine_id)
            if node_id:
                io_key_data = io_list_data(node_id)
                # print('io_key_data report ',io_key_data)
                io_value_data = io_values(machine_id,"Reports",'',start_datetime,end_datetime1)
                # print('io_value_data report ',io_value_data)

                # print('kpirawdata',kpirawdata)
                kpi_result['card'] = data['Card_type__Card_Type']
                kpi_result['title'] = data['Title']
                kpi_result['ledger'] = data['Ledger']
                labels = {
                    "x_label": data['X_Label'],
                    "y_label": data['Y_Label']
                    # "units": data['Unit'],
                    # "y_label": data['Y_Label']

                }
                kpi_result["labels"] = labels

                trail_result=[]
                for trail in io_value_data:
                    Trails_data = key_value_merge(node_id, io_key_data, trail)

                    # trail_result_output={
                    #     "data":Trails_data['digital_input']+Trails_data['digital_output']+Trails_data['analog_input']+
                    #     Trails_data['analog_output']+Trails_data['others'],
                    #     "timestamp":trail["Timestamp"]
                    #
                    # }
                    trail_result_output = {
                        "data": Trails_data['digital_input'] + Trails_data['digital_output'] + Trails_data[
                            'analog_input'] +
                                Trails_data['analog_output'] + Trails_data['others'],
                        # "timestamp": trail["Timestamp"]

                    }
                    trail_data_values = []  # List to store 'value' from each item in Trails_data
                    for item in trail_result_output['data']:
                        trail_data_values.append(item['value'])
                    print('trail_data_values',trail_data_values)

                    original_timestamp = trail["Timestamp"]
                    print('original time', original_timestamp)
                    dt = datetime.datetime.strptime(original_timestamp, "%Y-%m-%dT%H:%M:%SZ")
                    formatted_timestamp = dt.strftime("%d-%m-%YT%H:%M:%SZ")  # "2024-07-08T17:20:25Z
                    print('formatted_timestamp', formatted_timestamp)

                    trail_result_output = {
                        "x_axis_data":formatted_timestamp,
                         "y_axis_data":trail_data_values
                    }


                    trail_result.append(trail_result_output)

                kpi_result['data'] = trail_result
                entire_result_data.append(kpi_result)
                # print('length...................',len(entire_result_data))
                # print('length...................',entire_result_data)

                return {"resultant_data":entire_result_data}

            else:
                return {"status": "please enter valid node_id"}



def text_card(data, entire_result_data, kpi_result, method, start_datetime=None, end_datetime=None, report_type=None):
    formatted_datetime = datetime.now().date()
    todays_date = formatted_datetime.strftime("%Y-%m-%d")
    yesterday_date = formatted_datetime - timedelta(days=2)
    # print('text')
    kpi_result_data = []

    if method == "kpis":

        kpirawdata = CardsRawData.objects.filter(
            Machine_Id__contains=[data['Machine_Id__Machine_id']],
            Title=data['Title'],
            Timestamp__date=todays_date
        ).distinct('Timestamp').order_by('-Timestamp')
        print('textttt kpi')
    elif method == "kpiweb":
        kpirawdata =[CardsRawData.objects.filter(
            Machine_Id__contains=[data['Machine_Id__Machine_id']],
            Title=data['Title'],
            Timestamp__date=todays_date
        ).distinct('Timestamp').order_by('-Timestamp').latest('Timestamp')]
    elif method == "reports":
        kpirawdata = CardsRawData.objects.filter(
            Machine_Id=[data['Machine_Id__Machine_id']],
            Title=report_type,
            Timestamp__range=[start_datetime, end_datetime],
        ).distinct('Timestamp').order_by('Timestamp')

        # kpi_result_data = []
        # for record in kpirawdata1:
        #     # Process each record and create a dictionary
        #     record_data = {"name": record.Name, "value": record.Value, "unit": data['Unit'],"Timestamp":record.Timestamp}
        #     kpi_result_data.append(record_data)

        # print('kpirawdata', kpirawdata)
    elif method == "dashboard":
        dashrawdata = CardsRawData.objects.filter(
            Machine_Id__contains=[data['Machine_Id__Machine_id']],
            Title=data['Title'],
            Timestamp__date=todays_date,
            Mode=data['mode'][0]
        ).distinct('Timestamp', 'Mode')

        for d in dashrawdata:
            machine_id = d.Machine_Id  # Get the machine ID
            # Check if the card already exists in entire_result_data
            card_exists = False
            for card_data in entire_result_data:
                if card_data['title'] == data['Title'] and card_data['ledger'] == data['Ledger']:
                    card_exists = True
                    # Append data to existing card
                    card_data['data'].append({
                        "x_axis_data": d.Machine_Id,
                        "y_axis_data": d.Value
                    })
                    break

            if not card_exists:
                # Create a new card entry
                new_card = {
                    "card": data['Card_type__Card_Type'],
                    "title": data['Title'],
                    "ledger": data['Ledger'],
                    "labels": {
                        "x_label": data['X_Label'],
                        "y_label": data['Y_Label']
                    },
                    "data": [{
                        "x_axis_data": d.Machine_Id,
                        "y_axis_data": d.Value
                    }]
                }
                entire_result_data.append(new_card)

        kpi_entry = {
            'resultant_data': entire_result_data,
        }
        # print('kpi_entry', kpi_entry)

        return kpi_entry

    # Process kpirawdata only if it's not None
    if kpirawdata:

        # print('kpirawdata',kpirawdata)
        kpi_result['card'] = data['Card_type__Card_Type']
        kpi_result['title'] = data['Title']
        kpi_result['ledger'] = data['Ledger']
        labels = {
            "units": data['Unit'],
            # "y_label": data['Y_Label']
        }
        kpi_result["labels"] = labels
        for res in kpirawdata:
            print('res', res.Timestamp)
            print('res type', type(res.Timestamp))
            timestamp_dt = res.Timestamp

            # Format the datetime object
            # formatted_timestamp_str = timestamp_dt.strftime('Y%-%m-%d %H:%M:%S')
            # formatted_timestamp_str = timestamp_dt.strftime('d%-%m-%Y %H:%M:%S')
            formatted_timestamp_str = timestamp_dt.strftime("%d-%m-%Y %H:%M:%S")

            print('formatted_timestamp_str',formatted_timestamp_str)
            text_res_data = {"Timestamp": formatted_timestamp_str, "value": res.Value}

            kpi_result_data.append(text_res_data)


        kpi_result['data'] = kpi_result_data
        entire_result_data.append(kpi_result)
        # print('entire_result_data',entire_result_data)
        # print('kpi_result_data',kpi_result_data)

        kpi_entry = {'resultant_data': entire_result_data}
        # print('kpi_entry', kpi_entry)
        return kpi_entry
    else:
        # Handle the case when kpirawdata is None (no records found)
        return None


def status(data, entire_result_data, kpi_result, method, start_datetime=None, end_datetime=None, report_type=None):
    formatted_datetime = datetime.now().date()
    todays_date = formatted_datetime.strftime("%Y-%m-%d")

    kpi_result_data = []

    if method == "kpis":

        kpirawdata = CardsRawData.objects.filter(
            Machine_Id__contains=[data['Machine_Id__Machine_id']],
            Title=data['Title'],
            Timestamp__date=todays_date
        ).order_by('-Timestamp').distinct('Timestamp')
    elif method == "kpiweb":
        kpirawdata =[CardsRawData.objects.filter(
            Machine_Id__contains=[data['Machine_Id__Machine_id']],
            Title=data['Title'],
            Timestamp__date=todays_date
        ).distinct('Timestamp').order_by('-Timestamp').latest('Timestamp')]

    if kpirawdata:

        # print('kpirawdata',kpirawdata)
        kpi_result['card'] = data['Card_type__Card_Type']
        kpi_result['title'] = data['Title']
        kpi_result['ledger'] = data['Ledger']
        labels = {
            "units": data['Unit'],
        }
        kpi_result["labels"] = labels
        for res in kpirawdata:
            # print('res in status', res.Timestamp)
            timestamp_dt = res.Timestamp


            formatted_timestamp_str = timestamp_dt.strftime("%d-%m-%Y %H:%M:%S")



            # timestamp_dt = datetime.fromisoformat(str(res.Timestamp))

            # Format the datetime object
            # formatted_timestamp_str = timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')
            # print('.............',res.Value)
            value=res.Value
            if value[0] == "Off":
                value[0] = "Idle"

            text_res_data = {"Machine": value}

            kpi_result_data.append(text_res_data)


        kpi_result['data'] = kpi_result_data
        entire_result_data.append(kpi_result)
        # print('entire_result_data',entire_result_data)
        # print('kpi_result_data',kpi_result_data)

        kpi_entry = {'resultant_data': entire_result_data}
        # print('kpi_entry', kpi_entry)
        return kpi_entry
    else:
        # Handle the case when kpirawdata is None (no records found)
        return None


# def text_card(data,entire_result_data,kpi_result,method,start_datetime=None,end_datetime=None,report_type=None):
#     todays_date = datetime.datetime.now().date()
#     if method ==  "kpis":
#         kpirawdata = CardsRawData.objects.filter(
#             Machine_Id__contains=[data['Machine_Id__Machine_id']],
#             Title=data['Title'],
#             Timestamp__date=todays_date
#         ).order_by('-Timestamp').first()
#     elif method == "reports":
#         kpirawdata = CardsRawData.objects.filter(
#             Machine_Id=[data['Machine_Id__Machine_id']],
#             Title=data['Title'],  # Assuming there's a field for KPI ID in the Machine_KPI_Data model
#             Timestamp__range=[start_datetime, end_datetime],
#         ).order_by('Timestamp')
#         print('kpirawdata', kpirawdata)
#
#         pass
#
#     print('kpirawdatavaluessssssssssss', kpirawdata.Value)
#     # card_data = []
#     kpi_result_data = [{key: value for key, value in zip(['name', 'value', 'unit'], values)} for values in
#                      zip(kpirawdata.Name, kpirawdata.Value, data['Unit'])]
#
#     print('<<<<<<<<<<<<<<<<<',kpi_result_data)
#
#
#     # if kpirawdata:
#     #     kpi_result_data = {"Name":kpirawdata.Name,"Value": kpirawdata.Value}
#     #     card_data.append(kpi_result_data)
#
#     # for j in kpirawdata:
#     #     print('jjjj', j)
#     #     kpi_result_data = {"Value": j. Value}
#     #     card_data.append(kpi_result_data)
#
#     kpi_result['card'] = data['Card_type__Card_Type']
#     kpi_result['title'] = data['Title']
#     kpi_result['ledger'] = data['Ledger']
#     labels = {
#         # "unit": data['Unit'],
#         # "y_label": data['Y_Label']
#     }
#     kpi_result["labels"] = labels
#     kpi_result['data'] = kpi_result_data
#     # kpi_result['data']['unit']=data['Unit']
#     # card_data[0]["unit"] = data['Unit']
#     entire_result_data.append(kpi_result)
#
#     kpi_entry = {
#
#         'kpidata': entire_result_data,
#     }
#     print('kpi_entry', kpi_entry)
#
#     return kpi_entry


def count_machines(machines):
    current_time_Ist = datetime.now()
    current_time = current_time_Ist.astimezone(timezone.utc)


    machine_names_query = MachineDetails.objects.filter(id__in=machines).values('id','Machine_id','Machine_Name')
    # print('machines_query', machine_names_query)
    # result = []
    machine_count = 0
    inactive_count = 0
    active_count = 0
    all_machines_status=[]
    for machine_data in machine_names_query:
        # print('machine_data', machine_data)

        machines = machine_data['Machine_id']
        # print('machines dashboard', machines)
        machine_count += 1

        if MachineRawData.objects.filter(Machine_Id=machines).exists():

            # to_fetch_lastrecord_data = MachineDetails.objects.filter(machine_id=machines).values('machine_id','timestamp').latest('timestamp')
            to_fetch_lastrecord_data = MachineRawData.objects.filter(Machine_Id=machines).values('Machine_Id',
                                                                                                 'Db_Timestamp')


            # print('fetch_latest sliceee', fetch_latest)

            fetch_latest = to_fetch_lastrecord_data.latest('Db_Timestamp')

            # print('fetch_latest', fetch_latest)
            # print('fetch_latest', fetch_latest)
            last_record_time1 = fetch_latest['Db_Timestamp']
            # print('last_record_time1', last_record_time1)
            # five_30_hours = timedelta(hours=5, minutes=30)
            # print('five_30_hours',five_30_hours)
            adjusted_datetime = last_record_time1
            # adjusted_datetime = last_record_time1 - five_30_hours
            # print('adjusted_datetime',adjusted_datetime)

            # last_record_time2 = last_record_time1.strftime("%Y-%m-%d %H:%M:%S.%f %Z").split('.')[0]
            # print("last_record_time2 string",last_record_time2)
            # print("last_record_time2 type ss",type(last_record_time2))
            # last_record_time = datetime.strptime(last_record_time2, "%Y-%m-%d %H:%M:%S")
            # utc_timestamp_latest=last_record_time.astimezone(timezone.utc)
            # print('last_record_time s to d', last_record_time)
            # print('utc_timestamp_latest', utc_timestamp_latest)
            # print('current_time', current_time)


            time_difference = abs((current_time - adjusted_datetime).total_seconds())
            # time_difference = current_time - last_record_time
            print('time_difference', time_difference)
            # print(' time_difference > timedelta(seconds=30)', time_difference > 60)

            if time_difference > 600:
                # print("in if------------")
                machine_status = "Inactive"
                inactive_count += 1 # uncomment later now inactive_count = 0
                # inactive_count = 0 # uncomment later now inactive_count = 0
                # print('inactive if', inactive_count)
            else:
                # print("in else------------")
                machine_status = "Active"
                # active_count = machine_count
                active_count += 1
                # print('active else', active_count)
        else:
            inactive_count += 1
            # inactive_count = 0
            machine_status = "Inactive"
            # print('inactive else', inactive_count)
        count_card_data = {
            # "title": "count_card",
            "Total Machines": str(machine_count),
            # "Active Machines": str(active_count),
            "Active Machines": str(active_count),
            "Inactive Machines": str(inactive_count)

        }
        Machines_and_status={
            "Machine_name":machine_data['Machine_Name'],
            "machine_id":machine_data['Machine_id'],
            "Machines_status":machine_status,
            # "Machines_status":'Active',
            "node_id":machine_data['id'],
            #"module":5

            # "Machines_status":machine_status
        }
        all_machines_status.append(Machines_and_status)

    return count_card_data,all_machines_status


def dashboard_data(dash):
    dash_node = MachineCardsList.objects.filter(id__in=dash).values(
        'Machine_Id__Machine_id',
        'Title',
        'X_Label',
        'Y_Label',
        'Ledger',
        'Title',
        'Card_type__Card_Type',
        'Unit',
        'mode'
    )

    entire_result_data = []
    result = {"resultant_data": []} # Initialize the result

    for k in dash_node:
        dash_result = {}

        switch_dict = {
            "Line": lambda: Line_bar_graph(k, entire_result_data, dash_result, "dashboard"),
            "Bar": lambda: Line_bar_graph(k, entire_result_data, dash_result, "dashboard"),
            "Text": lambda: text_card(k, entire_result_data, dash_result, "dashboard"),
            "Pie": lambda: text_card(k, entire_result_data, dash_result, "dashboard"),
            'default': lambda: {"resultant_data": []},
        }

        # Execute the corresponding function from the switch_dict
        result_data = switch_dict.get(k['Card_type__Card_Type'], switch_dict['default'])()

        # Append result_data to resultant_data if it has any content
        if 'resultant_data' in result_data:
            result["resultant_data"].extend(result_data["resultant_data"])

    return result








# def dashboard_data(dash):
#     dash_node = MachineCardsList.objects.filter(id__in=dash).values('Machine_Id__Machine_id',
#                                     'Title','X_Label','Y_Label','Ledger','Title','Card_type__Card_Type','Unit','mode')
#
#     entire_result_data = []
#     for k in dash_node:
#
#         dash_result = {}
#         # print('k', k['Card_type__Card_Type'])
#         switch_dict = {
#             "Line": lambda: Line_bar_graph(k, entire_result_data, dash_result, "dashboard"),
#             "Bar": lambda: Line_bar_graph(k, entire_result_data, dash_result, "dashboard"),
#             "Text": lambda: text_card(k, entire_result_data, dash_result, "dashboard"),
#             "Pie": lambda: text_card(k, entire_result_data, dash_result, "dashboard"),
#
#             'default': lambda: {"resultant_data": []},
#         }
#
#         # Execute the corresponding function from the switch_dict or the default function
#         result = switch_dict.get(k['Card_type__Card_Type'], switch_dict['default'])()
#     return result


def alarm(i,entire_result_data,kpi_result,method):
    # print('machineid alaram...........',i['Machine_Id__Machine_id'])
    # print('machineid alaram...........',i)
    machine_id = i['Machine_Id__Machine_id']
    kpi_result_data_alarm = []
    date_today = datetime.now().date()
    todays_date = date_today.strftime("%Y-%m-%d")
    value = MachineCardsList.objects.get(Machine_Id__Machine_id=machine_id,
                                         Card_type__Card_Type='Alarm')  # later filter alaramgrp

    if method == "kpis":
        alarm_table_date=Alarm_data.objects.filter(machine_id=machine_id,TimeStamp__date=todays_date).order_by('TimeStamp').\
            distinct('TimeStamp')
        alarm_table_date_serializer=alarm_serializer(alarm_table_date,many=True)
        alarm_serializer_data=alarm_table_date_serializer.data
        # print('alarm_serializer_data kpis',alarm_serializer_data)
        kpi_result_data_alarm=alarm_serializer_data
        # print('kpi_result_data_alarm',kpi_result_data_alarm)


    if method == "kpiweb":

        # machine_grp=MachineDetails.objects.get(Machine_id=machine_id)
        # print('machine_grp',machine_grp)

        machine_latest_data=Alarm_data.objects.filter(machine_id=machine_id, TimeStamp__date=todays_date)\
            .order_by('-TimeStamp').latest('TimeStamp')


        # latest_entry = machine_latest_data.latest('TimeStamp')
        alarm_single_data = alarm_serializer(machine_latest_data)
        alarm_serializer_data = alarm_single_data.data
        kpi_result_data_alarm.append({
            "Message": alarm_serializer_data.get("Message", ""),
            "TimeStamp": alarm_serializer_data.get("TimeStamp", "")
        })

        # # print('machine_latest_data',machine_latest_data)
        # # print('countttttttttt',machine_latest_data.count())
        # alarm_single_data = alarm_serializer(machine_latest_data)
        # # print()
        # alarm_serializer_data = alarm_single_data.data
        # print('alarm_serializer_data kpiweb',alarm_serializer_data)
        # kpi_result_data_alarm=alarm_serializer_data
        # print('kpi_result_data_alarm kpiweb',kpi_result_data_alarm)



        # print('reee',kpi_result_data_alarm)
    kpi_result['card'] = value.Card_type.Card_Type
    kpi_result['title'] = value.Title
    kpi_result['ledger'] = value.Ledger
    labels = {
        "units": value.Unit,
        # "y_label": data['Y_Label']
    }
    kpi_result["labels"] = labels


    kpi_result['data'] = kpi_result_data_alarm
    entire_result_data.append(kpi_result)
    kpi_entry = {'resultant_data': entire_result_data}
    return kpi_entry


    # "on" index and particular "on" index keys zip and send








