import datetime

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from .Nested_Queries import *
from .conversions import *
from Atoms_machines.models import CardsRawData
from django.db.models import F, CharField, Value
from django.db.models.functions import Cast


def dropdown(user_id):

    # user_id=6
    user_lr=get_node_LR(user_id, "User")
    print('user_lr',user_lr)
    # data = {'left': left_v, "right": right_v}

    data = get_grandparent(user_lr['left'], user_lr['right'])
    grand_left=data['grandparent']['grandparent_l']
    grand_right=data['grandparent']['grandparent_r']
    print('left',data['grandparent']['grandparent_l'])
    print('right',data['grandparent']['grandparent_r'])

    des = get_descendent(grand_left, grand_right, "Layer","node_lr")
    print('des',des)
    result=[]
    for i in des['descendents']:
        layer_parents= Parent_nodes(i["node_left"],i["node_right"],grand_left,grand_right)
        print('p...........',layer_parents)
        # get_layer_details=Layers.objects.filter(id__in=layer_parents).values_list('Layer_Name',flat=True)
        get_layer_details=Layers.objects.filter(id__in=layer_parents).values('Layer_Name','Layer_Type').order_by('id')
        print('get_layer_details',get_layer_details)
        serializer=layerSerializer(get_layer_details,many=True)
        print('.............',serializer.data)
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
        print('detail_serializer',dict(detail_serializer.data))
        # print('detail_serializer manuals',detail_serializer.data['Manuals'])
        manuals_data=[dict(item) for item in detail_serializer.data['Manuals']]
        techincal_data=[dict(item) for item in detail_serializer.data['Technical_Details']]
        details=only_details_serailizers(get_machine_details)
        print('details',details.data)

        general_data = {"general_details":details.data ,"Manuals_and_Docs":manuals_data,
                             "Techincal_Details_data":techincal_data}
        print('dataaaa',general_data)

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
        iostatus_data["time_stamp"] = io_value_data['Timestamp']


        print('iostatus_data', iostatus_data)
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
        control_data["machine_id"] = node_id
        control_data["machine_name"] = machine_name
        control_data["time_stamp"] = io_value_data['Timestamp']
        print('control_data',control_data)
        return control_data
    else:
        return {"status": "please enter valid node_id"}


def machine_kpis(node_id):
    todays_date = datetime.datetime.now().date()
    lrvalues=get_node_LR(node_id,"Machine")
    left=lrvalues['left']
    right=lrvalues['right']
    child_kpi=get_descendent(left,right,"Kpi","node")
    print('child_kpi',child_kpi["descendents"])
    kpinode_data=MachineCardsList.objects.filter(id__in=child_kpi["descendents"]).values('Machine_Id__Machine_id',
                                    'Title','X_Label','Y_Label','Ledger','Title','Card_type__Card_Type','Unit')
    print('kpinode_data',kpinode_data)


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
            "Pie": lambda: "under dev",

            'default': lambda: {"status": ""},
        }

        # Execute the corresponding function from the switch_dict or the default function
        result = switch_dict.get(i['Card_type__Card_Type'], switch_dict['default'])()

    return result


def Reports_data(user_id,machine_id,start_datetime,end_datetime1,report_type):
    print('node_id in reports_data',user_id)
    todays_date = datetime.datetime.now().date()
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
    print('child_kpi',child_kpi["descendents"])
    kpinode_data=MachineCardsList.objects.filter(id__in=child_kpi["descendents"],Title=report_type).values('Machine_Id__Machine_id',
                                    'Title','X_Label','Y_Label','Ledger','Title','Card_type__Card_Type','Unit')
    print('kpinode_data',kpinode_data)
    entire_result_data=[]
    # x_axis=[]
    # y_axis=[]
    if kpinode_data:
        for i in kpinode_data:
            kpi_result = {}
            print('i',i)
            print('i..........',i['Card_type__Card_Type'])
            switch_dict = {
                "Line": lambda: Line_bar_graph(i,entire_result_data,kpi_result,"reports",user_id,machine_id,start_datetime,end_datetime1,report_type),
                "Bar": lambda: Line_bar_graph(i,entire_result_data,kpi_result,"reports",user_id,machine_id,start_datetime,end_datetime1,report_type),
                "Text": lambda: text_card(i,entire_result_data,kpi_result,"reports",user_id,machine_id,start_datetime,end_datetime1,report_type),
                "Pie": lambda: "under dev",

                'default': lambda: {"status": ""},
            }

            # Execute the corresponding function from the switch_dict or the default function
            result = switch_dict.get(i['Card_type__Card_Type'], switch_dict['default'])()


        return result
    else:
        return "no data available"



















def Line_bar_graph(data,entire_result_data,kpi_result,method,user_id=None,machine_id=None,start_datetime=None,end_datetime=None,report_type=None):
    formatted_datetime = datetime.datetime.now().date()
    todays_date = formatted_datetime.strftime("%Y-%m-%d")
    if method == "kpis":

        kpirawdata = CardsRawData.objects.filter(
            Machine_Id__contains=[data['Machine_Id__Machine_id']],
            Title=data['Title'],
            Timestamp__date=todays_date
        ).order_by('-Timestamp')[:10]
    elif method == "kpiweb":
        kpirawdata = CardsRawData.objects.filter(
            Machine_Id__contains=[data['Machine_Id__Machine_id']],
            Title=data['Title'],
            Timestamp__date=todays_date
        ).order_by('-Timestamp')[::12]

    elif method =="reports":

        kpirawdata = CardsRawData.objects.filter(
            Machine_Id=[machine_id],
            Title=report_type,  # Assuming there's a field for KPI ID in the Machine_KPI_Data model
            Timestamp__range=[start_datetime, end_datetime],
        ).order_by('Timestamp')
        print('kpirawdata',kpirawdata)


    # print('kpirawdata', kpirawdata[0].Value)
    card_data = []
    for j in kpirawdata:
        print('jjjj', j)
        timestamp_str = str(j.Timestamp)
        kpi_result_data = {"x_axis_data": timestamp_str, "y_axis_data": j.Value}
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

        'data': entire_result_data,
    }
    print('kpi_entry', kpi_entry)

    return kpi_entry


def text_card(data, entire_result_data, kpi_result, method, start_datetime=None, end_datetime=None, report_type=None):
    formatted_datetime = datetime.datetime.now().date()
    todays_date = formatted_datetime.strftime("%Y-%m-%d")

    kpi_result_data = []

    if method == "kpis":

        kpirawdata = CardsRawData.objects.filter(
            Machine_Id__contains=[data['Machine_Id__Machine_id']],
            Title=data['Title'],
            Timestamp__date=todays_date
        ).order_by('-Timestamp').first()
    elif method == "kpiweb":
        kpirawdata = CardsRawData.objects.filter(
            Machine_Id__contains=[data['Machine_Id__Machine_id']],
            Title=data['Title'],
            Timestamp__date=todays_date
        ).order_by('-Timestamp')[::12]
    elif method == "reports":
        kpirawdata = CardsRawData.objects.filter(
            Machine_Id=[data['Machine_Id__Machine_id']],
            Title=report_type,
            Timestamp__range=[start_datetime, end_datetime],
        ).order_by('Timestamp')

        # kpi_result_data = []
        for record in kpirawdata:
            # Process each record and create a dictionary
            record_data = {"name": record.Name, "value": record.Value, "unit": data['Unit'],"timestamp":record.Timestamp}
            kpi_result_data.append(record_data)

        # print('kpirawdata', kpirawdata)

    else:
        # Handle other cases if needed
        pass

    # Process kpirawdata only if it's not None
    if kpirawdata:
        kpi_result['card'] = data['Card_type__Card_Type']
        kpi_result['title'] = data['Title']
        kpi_result['ledger'] = data['Ledger']
        labels = {
            # "unit": data['Unit'],
            # "y_label": data['Y_Label']
        }
        kpi_result["labels"] = labels
        kpi_result['data'] = kpi_result_data
        entire_result_data.append(kpi_result)

        kpi_entry = {'kpidata': entire_result_data}
        print('kpi_entry', kpi_entry)
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


