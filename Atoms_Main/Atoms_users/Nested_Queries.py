
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *



def get_node_LR(node,pro):#user
    print('..........',node)
    node_lr=Nested_Table.objects.get(Node_Id=node,Property=pro)

    # node_lr_values=Nested_Table.objects.filter(Node_Id=node).values("Node_Left","Node_Right")
    # print('node_lr_values',node_lr_values)
    print("........",node_lr)
    left_v=node_lr.Node_Left
    right_v=node_lr.Node_Right
    data={'l':left_v,"r":right_v}
    p_l_r=get_two_levels_of_parents(left_v,right_v)
    print('parent_left_right',p_l_r)

    pages=get_descendent(p_l_r["immediate_parent"]["immediate_parent_l"],p_l_r["immediate_parent"]["immediate_parent_r"],"Page")
    machines=get_descendent(p_l_r["grandparent"]["grandparent_l"],p_l_r["grandparent"]["grandparent_r"],"Machine")
    return data,p_l_r,pages,machines

def get_two_levels_of_parents(left_value, right_value):
    immediate_parent = Nested_Table.objects.filter(
        Node_Left__lt=left_value,
        Node_Right__gt=right_value
    ).order_by('Node_Id').last()
    print('immediate_parent',immediate_parent)

    if immediate_parent:
        grandparent = Nested_Table.objects.filter(
            Node_Left__lt=immediate_parent.Node_Left,
            Node_Right__gt=immediate_parent.Node_Right
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

    descendant_names = [descendant.Node_Id for descendant in descendants]
    print('descendant_names ', property,descendant_names)
    return {property:descendant_names}



@api_view(['GET'])
def get_node_LR_api(request):
    node_id=request.GET.get("node_id")
    pro=request.GET.get("pro")

    res=get_node_LR(node_id,pro)
    return Response(res)

