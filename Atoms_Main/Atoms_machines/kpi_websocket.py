import json
from Atoms_users .models import User_details
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()
from Atoms_users.Nested_Queries import  get_node_LR,get_grandparent,get_descendent
from Atoms_users.api_functions import Line_bar_graph,text_card
from django.apps import apps

# @sync_to_async
def kpi_socket(machine_id):
    # from Atoms_users .models import MachineDetails
    MachineDetails = apps.get_model('Atoms_users','MachineDetails')
    machine=MachineDetails.objects.get(Machine_id=machine_id)
    print('machine',machine)



    # user_id=User_details.objects.get(user_id__username=username)
    # print("IIIIIIII",user_id.pk)
    # data=get_node_LR(user_id.pk, "User")
    # u_left=data['left']
    # u_right=data['right']
    # gp=get_grandparent(u_left,u_right)
    # gp_l=gp['grandparent']['grandparent_l']
    # gp_r=gp['grandparent']['grandparent_r']
    # machines=get_descendent(gp_l, gp_r, "Machine", "node")
    # print('machines',machines['descendents'])
    # from Atoms_machines.models import MachineCardsList
    MachineCardsList = apps.get_model('Atoms_users','MachineCardsList')
    print('MachineCardsList',MachineCardsList)


    kpinode_data = MachineCardsList.objects.filter(Machine_Id__in=[machine.pk]).\
        values('Machine_Id__Machine_id','Title', 'X_Label', 'Y_Label', 'Ledger', 'Title',
               'Card_type__Card_Type', 'Unit')
    print('kpinode_data', kpinode_data)

    entire_result_data = []
    # x_axis=[]
    # y_axis=[]
    abc=[]
    for i in kpinode_data:
        kpi_result = {}
        print('i', i)
        switch_dict = {
            "Line": lambda: Line_bar_graph(i, entire_result_data, kpi_result, "kpiweb"),
            "Bar": lambda: Line_bar_graph(i, entire_result_data, kpi_result, "kpiweb"),
            "Text": lambda: text_card(i, entire_result_data, kpi_result, "kpiweb"),
            "Pie": lambda: "under dev",

            'default': lambda: {"status": ""},
        }

        # Execute the corresponding function from the switch_dict or the default function
        resultkpi = switch_dict.get(i['Card_type__Card_Type'], switch_dict['default'])()
        print('result_inside',resultkpi)
        # abc.append(resultkpi)
    # output = json.dumps(abc)
    # print('output',output)
        kpiresultdata = json.dumps(resultkpi)
        async_to_sync(channel_layer.group_send)(str(machine_id)+'_kpi',
                                                {"type": "kpiweb", "text": kpiresultdata})

        # output = json.dumps(result)
        # print('outputkpi',output)
        # try:
        # except Exception as e:
        #     print("io error - ", e)











