from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *

def get_node_LR(node,pro):#user
    print('..........',node)
    node_left_right=Nested_Table.objects.get(Node_Id=node,Property=pro)
    left_v=node_left_right.Node_Left
    right_v=node_left_right.Node_Right
    data={'left':left_v,"right":right_v}
    return data






def immediate_node(left_value,right_value):
    immediate_parent = Nested_Table.objects.filter(
        Node_Left__lt=left_value,
        Node_Right__gt=right_value
    ).order_by('Node_Id').last()
    print('immediate_parent', immediate_parent)
    im_lr={'im_left':immediate_parent.Node_Left,'im_right':immediate_parent.Node_Right}
    return im_lr


def grand_parent(left_value, right_value):
    im_parent=immediate_node(left_value,left_value)
    print('immediate_parent',im_parent)

   #???????????
    if im_parent:
        grandparent = Nested_Table.objects.filter(
            Node_Left__lt=im_parent.Node_Left,
            Node_Right__gt=im_parent.Node_Right
        ).order_by('Node_Id').last()

        print('grandparent',grandparent)

        grandparent_l=grandparent.Node_Left
        grandparent_r=grandparent.Node_Right


        return {"immediate_parent":{"immediate_parent_l":immediate_parent.Node_Left,"immediate_parent_r":immediate_parent.Node_Right}, "grandparent":{"grandparent_l":grandparent_l,"grandparent_r":grandparent_r}}

    else:
        return None, None

def get_descendent(parent_left,parent_right,property):
    descendants = Nested_Table.objects.filter(
        Node_Left__range=(parent_left, parent_right),Property=property

    ).order_by('Node_Id')

    descendant_names = [{"node":descendant.Node_Id ,"left":descendant.Node_Left,"right":descendant.Node_Right} for descendant in descendants]
    print('descendant_names ', property,descendant_names)
    return {"descendents":descendant_names,'property':property}



def Parent_nodes(left_value,right_value,root_left_value,root_right_value):
    root_left_value =22 #user grandparent left
    root_right_value = 127

    # tree_id = request.GET.get('tree_id')

    descendants = Nested_Table.objects.filter(
        Q(Node_Left__lte=left_value,Node_Left__gte=root_left_value) & Q(Node_Right__gte=right_value,
        Node_Right__lte=root_right_value)

    ).order_by('Node_Left')

    # descendants = Nested_Table.objects.filter(
    #     Node_Left__range=(root_left_value,left_value), Node_Right__range=(root_right_value,right_value)
    #
    # ).order_by('Node_Left')
    print('lllllllllparent fun',descendants)
    descendant_names = [descendant.Node_Id for descendant in descendants]
    print('descendant_names',descendant_names)

    return descendant_names
#
# def get_node_and_depth(request):
#     # parent_name = request.GET.get('parent_name')
#     parent_name = request.GET.get('parent_name')
#     node = Node.objects.get(name=parent_name)
#     # node_data=NodeSerialiser(node,many=True)
#     print('node',node)
#     ancestors = Node.objects.filter(left__gt=node.left, right__gt=node.right)
#     print('ancestors', ancestors)




    # return Response(ancestors)


