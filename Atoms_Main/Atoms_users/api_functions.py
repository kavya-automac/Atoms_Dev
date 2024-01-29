
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from .Nested_Queries import *
from .conversions import *

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

