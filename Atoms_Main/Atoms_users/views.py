from itertools import groupby

from django.db.models.functions import Concat
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.db.models import F, Value, CharField,OuterRef, Subquery
from django.db.models.functions import Concat
from django.db.models import F, Q
from .Nested_Queries import *
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat
from . serializers import *

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Nested_Table  # Import your actual model
#
# @api_view(['GET'])
# def list(request):
#     left_value = 100
#     right_value = 103
#
#     # tree_id = request.GET.get('tree_id')
#
#     descendants = Nested_Table.objects.filter(
#         Node_Left__lt=left_value, Node_Right__gt=right_value,Property='Layer'
#
#     ).order_by('Node_Left')
#
#     descendant_names = [descendant.Node_Id for descendant in descendants]
#     gp=dropdown()
#     print('gp',gp)
#
#     return Response(gp)


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
        get_layer_details=Layers.objects.filter(id__in=layer_parents).values('Layer_Name','Layer_Type')
        print('get_layer_details',get_layer_details)
        serializer=layerSerializer(get_layer_details,many=True)
        print('.............',serializer.data)
        node_name=serializer.data[-1]["Layer_Name"]
        # node_name=i["node_id"]
        parent= [name["Layer_Name"] for name in serializer.data]
        Type=serializer.data[-1]["Layer_Type"]
        result_data={"node":node_name,"type":Type,"parent":parent}
        result.append(result_data)
    return result


@api_view(['GET'])

def Machine_module(request):
    user_id=5#from frontend
    drop_down=dropdown(user_id)


    user_left_right=get_node_LR(user_id,"User")
    im_lr=get_immediate_parent(user_left_right['left'], user_left_right['right'])

    sub_pages=get_descendent(im_lr['immediate_parent']['immediate_left'],im_lr['immediate_parent']['immediate_right'],"Subpage","node")
    print('sub_pages',sub_pages)

    return JsonResponse({"drop_down":drop_down,"sub_pages":sub_pages["descendents"]})









