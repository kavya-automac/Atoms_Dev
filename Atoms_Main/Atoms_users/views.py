from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import response, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from .Nested_Queries import *
from .conversions import *
from .api_functions import *

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
        print('authenticate_user:', type(user))

        if  user is not None:
            # print("not none")

            login(request, user)
            print("logged in:", request.user.username)
            print('request_user',request.user)
            print('request_user_username',request.user.id)
            user_id=User_details.objects.get(user_id__username=request.user)
            user_id_serializer=user_details_serializer_all(user_id)
            user_id_serializer_data=user_id_serializer.data
            print('user_id_serializer_data',user_id_serializer.data)
            print(user_id,user_id.Company_id,user_id.Company_id.Company_Logo)
            node_lr=get_node_LR(user_id.pk,"User")
            print("node_lr",node_lr)
            immediate_prt=get_immediate_parent(node_lr['left'],node_lr['right'])
            print('immediate_prt',immediate_prt)
            pages=get_descendent(immediate_prt['immediate_parent']['immediate_left'], immediate_prt['immediate_parent']['immediate_right'], "Page","node")
            # page_ids=[node['node_id'] for node in pages['descendents']]
            # print('page_ids',page_ids)
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
                             "user_id":user_id_serializer_data['user_id'],"Company_logo":user_id.Company_id.Company_Logo,"pages":pages['descendents'],"status_code":200})

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

    # user_id = User_details.objects.get(user_id__username="user1")
    # user_id_serializer = user_details_serializer_all(user_id)
    # user_id_serializer_data = user_id_serializer.data
    # print('user_id_serializer_data', user_id_serializer.data)
    node_id=request.query_params.get('node_id')
    node_lr = get_node_LR(node_id, "Layer")
    print("node_lr", node_lr)
    # grandparent_lr=get_grandparent(node_lr['left'],node_lr['right'])
    # print('grandparent_lr',grandparent_lr)
    get_machines=get_descendent(node_lr['left'],node_lr['right'],"Machine","node")
    print('get_machines',get_machines)
    # machines = [node['node_id'] for node in get_machines['descendents']]
    machines = get_machines['descendents']
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


@api_view(['GET'])

def Machine_module(request):#dropdown
    # user_id=10#from frontend
    print('request.headers',request.headers)
    print('request.headers',request.headers['user-id'])
    user_id=request.headers['user-id']
    print("user_id||||||||||||||||",user_id)
    drop_down=dropdown(user_id)


    user_left_right=get_node_LR(user_id,"User")
    im_lr=get_immediate_parent(user_left_right['left'], user_left_right['right'])

    sub_pages=get_descendent(im_lr['immediate_parent']['immediate_left'],im_lr['immediate_parent']['immediate_right'],"Subpage","node")
    print('sub_pages',sub_pages)

    return JsonResponse({"drop_down":drop_down,"sub_pages":sub_pages["descendents"]})


@api_view(['GET'])

def Machines_sub_details(request):#node_id= machine_id
    if "node_id" in request.GET and "module" in request.GET:
        module = request.GET.get('module')
        node_id = request.GET.get('node_id')

        switch_dict = {
            "5": lambda: JsonResponse(Details(node_id)),
            "6": lambda: JsonResponse(machine_kpis(node_id)),
            "7": lambda: JsonResponse({"iostatus":Machine_Iostatus(node_id)}),
            "8": lambda: JsonResponse({"control":Machine_Control(node_id)}),
            "9": lambda: JsonResponse({"status": 'Settings under development'}),
            'default': lambda: JsonResponse({"status": 'please give correct module'}),
        }

        # Execute the corresponding function from the switch_dict or the default function
        result = switch_dict.get(module, switch_dict['default'])()

        return result
    else:
        resultant = {"status": 'enter_correct__node_id_and_module'}
        return JsonResponse(resultant)

@api_view(['GET'])

def Trail_details(request):#node_id,date


    selected_date= request.GET.get('date')
    node_id=request.GET.get('node_id')#node_id = 1,2 seleted machine_id

    try:
        node = MachineDetails.objects.get(pk=node_id)
    except MachineDetails.DoesNotExist:
        error_message = "Please enter a valid node_machine_id."
        return JsonResponse({"status": error_message}, status=400)
    machine_id = node.Machine_id
    machine_name = node.Machine_Name
    if node_id:
        io_key_data = io_list_data(node_id)
        io_value_data = io_values(machine_id, "Trails",selected_date)
        trail_result=[]
        for trail in io_value_data:
            Trails_data = key_value_merge(node_id, io_key_data, trail)

            trail_result_output={
                "data":Trails_data,
                "timestamp":trail["Timestamp"]

            }
            trail_result.append(trail_result_output)
        print('length...................',len(trail_result))

        return JsonResponse({"machine_details": {
                "node_id":node_id,
                "machine_name": machine_name,
                "machine_id":machine_id

            },"Trail_Details":trail_result})

    else:
        return {"status": "please enter valid node_id"}


# @api_view(['POST'])
@api_view(['POST'])
def Reports_details(request):
    report_type = request.data.get('report_type')
    # machine_id = request.data.get('machine_id')
    node_id = request.data.get('node_id')#machine_id
    start_datetime = request.data.get('start_datetime')
    end_datetime1 = request.data.get('end_datetime')
    try:
        # Convert the start_datetime and end_datetime strings to datetime objects
        start_datetime = datetime.datetime.strptime(start_datetime, '%Y-%m-%d')
        # print('try  start_datetime',start_datetime)

        # end_datetime = datetime.datetime.strptime(end_datetime, '%Y-%m-%d %H:%M:%S')
        end_datetime2 = datetime.datetime.strptime(end_datetime1, '%Y-%m-%d')
        end_datetime = end_datetime2 + datetime.timedelta(days=1)
        # print('after increment end_datetime',end_datetime)

    except ValueError:
        return JsonResponse({"error": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS' format."},
                            status=status.HTTP_400_BAD_REQUEST)

    # try:
    #     node = MachineDetails.objects.get(pk=node_id)
    #     print('node',node)
    # except MachineDetails.DoesNotExist:
    #     error_message = "Please enter a valid node_machine_id."
    #     return JsonResponse({"status": error_message}, status=400)

    report_frontend_data=Reports_data(node_id,start_datetime,end_datetime,report_type)

    return JsonResponse({"report_details":report_frontend_data})





    # m_l_r = get_node_LR(node_id, "Machine")
    # p_l_r = get_immediate_parent(m_l_r['left'], m_l_r['right'])
    #
    # get_report_list = get_descendent(p_l_r['immediate_parent']['immediate_left'],
    #                                  p_l_r['immediate_parent']['immediate_right'],
    #                                  "Report", "node")
    # print('get_report_list',get_report_list['descendents'])
    pass







