from .Nested_Queries import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Nested_Table  # Import your actual model


@api_view(['GET'])
def list(request):
    left_value = 100
    right_value = 103

    # tree_id = request.GET.get('tree_id')

    descendants = Nested_Table.objects.filter(
        Node_Left__lt=left_value, Node_Right__gt=right_value,Property='Layer'

    ).order_by('Node_Left')

    descendant_names = [descendant.Node_Id for descendant in descendants]
    gp=dropdown()
    print('gp',gp)

    return Response(descendant_names)


def dropdown():


    data = get_two_levels_of_parents(34, 35)
    print('left',data['grandparent']['grandparent_l'])
    print('right',data['grandparent']['grandparent_r'])

    des = get_descendent(data['grandparent']['grandparent_l'], data['grandparent']['grandparent_r'], "Layer")
    print('des',des)
    l=[]
    for i in des['descendents']:
        p= Parent_nodes(i[1],i[2])
        print('p...........',p)
        n=i[0]
        parent=p
        d={"n":n,"parent":parent}
        l.append(d)
    print('///////////////////',l)







