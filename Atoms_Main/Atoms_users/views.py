from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from .Nested_Queries import *

@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    # print('serializer:', serializer)
    # print('serializer_type:', type(serializer))
    if serializer.is_valid():
        print('serializer:', serializer)
        username = serializer.data.get('username')
        # print('serializer_username:', username)
        # print('type_serializer_username:', type(username))
        password = serializer.data.get('password')
        # print('serializer_password:', password)
        # user = User.objects.get(username=username)
        # print(user)
        user  = authenticate(username=username, password=password)
        # print('authenticate_user:', user)

        if  user is not None:
            # print("not none")

            login(request, user)
            print("logged in:", request.user.username)
            print('request_user',request.user)
            print('request_user_username',request.user.id)
            user_id=User_details.objects.get(user_id__username="user1")
            user_id_serializer=user_details_serializer_all(user_id)
            user_id_serializer_data=user_id_serializer.data
            print('user_id_serializer_data',user_id_serializer.data)
            print(user_id,user_id.Company_id,user_id.Company_id.Company_Logo)
            node_lr=get_node_LR(user_id.pk,"User")
            print("node_lr",node_lr)
            immediate_prt=get_immediate_parent(node_lr['data']['left'],node_lr['data']['right'])
            print('immediate_prt',immediate_prt)
            pages=get_descendent(immediate_prt['immediate_parent']['immediate_left'], immediate_prt['immediate_parent']['immediate_right'], "Page")
            page_ids=[node['node_id'] for node in pages['descendents']]
            print('page_ids',page_ids)
            # access=[]
            # page_access = {}
            # for i in range(len(pages['Page'])):
            #
            #
            #     page_data=Modules.objects.get(pk=pages['Page'][i])
            #     print("(((",page_data)
            #     page_access[i]['page_id']=page_data.pk
            #     page_access[i]['page_name']=page_data.Module_Name
            #     page_access[i]['page_icon']=page_data.icons
            #     print(page_access)
            #     access.append(page_access)
            #
            # print(page_access)
            return JsonResponse({"status": "user_validated","first_name":request.user.first_name,
                             "user_id":user_id_serializer_data['user_id'],"Company_logo":user_id.Company_id.Company_Logo,"pages":page_ids,"status_code":200})

        else:
            # print("none")
            return JsonResponse({"status": "unauthorized_user"})
    return JsonResponse({'status':'Invalid Credentials'})

@api_view(['GET'])
def logout_view(request):
    # print("entering logout")


    # print("loggedout",request.user.username)

    logout(request)
    request.session.flush()
    return JsonResponse({"status": "Logged_out"})



@api_view(['GET'])
def Machines_List(request):

    user_id = User_details.objects.get(user_id__username="user1")
    # user_id_serializer = user_details_serializer_all(user_id)
    # user_id_serializer_data = user_id_serializer.data
    # print('user_id_serializer_data', user_id_serializer.data)
    node_lr = get_node_LR(user_id.pk, "User")
    print("node_lr", node_lr)
    grandparent_lr=get_grandparent(node_lr['data']['left'],node_lr['data']['right'])
    print('grandparent_lr',grandparent_lr)
    get_machines=get_descendent(grandparent_lr['grandparent']['grandparent_l'], grandparent_lr['grandparent']['grandparent_r'], "Machine")
    print('get_machines',get_machines)
    machines = [node['node_id'] for node in get_machines['descendents']]
    print(machines)
    # Querying MachineDetails model to get machine details
    machine_names_query = MachineDetails.objects.filter(id__in=machines)
    print('machines_query',machine_names_query)
    machine_details_serializer_data=machine_details_serializer_machine_id_machine_name(machine_names_query,many=True).data
    print('machine_details_serializer_all_data',machine_details_serializer_data)
    # Creating a list of dictionaries with 'Machine_id' and 'Machine_Name'
    machines_list = [{'Machine_id': machine.id, 'Machine_Name': machine.Machine_Name} for machine in
                     machine_names_query]

    print(machines_list)

    return JsonResponse({"machines":machine_details_serializer_data})
