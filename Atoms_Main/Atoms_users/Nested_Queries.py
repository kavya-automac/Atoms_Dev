from django.db.models import Q

from .models import *
from asgiref.sync import sync_to_async



def get_node_LR(node,pro):#user
    # print('..........',node)
    node_left_right=Nested_Table.objects.get(Node_Id=node,Property=pro)
    left_v=node_left_right.Node_Left
    right_v=node_left_right.Node_Right
    data={'left':left_v,"right":right_v}
    return data

def get_immediate_parent(left_value, right_value):

    immediate_parent = Nested_Table.objects.filter(
        Node_Left__lt=left_value,
        Node_Right__gt=right_value
    ).order_by('Node_Id').last()

    return {"immediate_parent":{"immediate_left":immediate_parent.Node_Left,"immediate_right":immediate_parent.Node_Right}}


def get_grandparent(left_value, right_value):
    im_par=get_immediate_parent(left_value, right_value)
    left=im_par["immediate_parent"]["immediate_left"]
    right=im_par["immediate_parent"]["immediate_right"]
    grandparent = Nested_Table.objects.filter(
        Node_Left__lt=left,
        Node_Right__gt=right
    ).order_by('Node_Id').last()



    grandparent_l=grandparent.Node_Left
    grandparent_r=grandparent.Node_Right


    return {"grandparent":{"grandparent_l":grandparent_l,"grandparent_r":grandparent_r}}


def get_descendent(parent_left,parent_right,property,type):
    descendants = Nested_Table.objects.filter(
        Node_Left__range=(parent_left, parent_right),Property=property

    ).order_by('Node_Left')
    if type =="node_lr":

        descendant_names = [{"node_id":descendant.Node_Id,"node_left":descendant.Node_Left,"node_right":descendant.Node_Right} for descendant in descendants]

        return {"descendents":descendant_names,"property":property}
    elif type == "node":
        descendant_names = [descendant.Node_Id for descendant in descendants]

        return {"descendents": descendant_names, "property": property}
    else:
        pass





def Parent_nodes(left_value,right_value,root_left_value,root_right_value):
    # left_value , right_value  child[1,2] layers
    #root_left_value, root_right_value   grandparent of user
    ascendants = Nested_Table.objects.filter(
        Q(Node_Left__lte=left_value,Node_Left__gte=root_left_value) & Q(Node_Right__gte=right_value,
        Node_Right__lte=root_right_value)

    ).order_by('Node_Left')


    ascendants_names = [ascendants.Node_Id for ascendants in ascendants]
    ascendants_left = [[ascendants.Node_Left,ascendants.Node_Right] for ascendants in ascendants]
    # print('ascendants_left/////////',ascendants_left)
    # ascendants_right = [ascendants.Node_Right for ascendants in ascendants]


    return ascendants_names


@sync_to_async
def user_department(user_id):
    user_lr = get_node_LR(user_id, "User")
    department = get_immediate_parent(user_lr['left'], user_lr['right'])
    get_department_node =Nested_Table.objects.get(Node_Left=department['immediate_parent']['immediate_left'],
    Node_Right=department['immediate_parent']['immediate_right'])

    # print('get_department_node',get_department_node)

    layerdata=Layers.objects.get(id=get_department_node.Node_Id)
    dept_name = layerdata.Layer_Name
    return dept_name
