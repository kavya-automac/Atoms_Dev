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
from Atoms_machines.mqtt_code import client
import json
import datetime
import logging

logger = logging.getLogger("django")

# import logging
# from Atoms_Main.settings import logger

# logger.debug('machine_list...!')
# logger = logging.getLogger("django")


@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    # print('serializer:', serializer)
    # print('serializer_type:', type(serializer))
    if serializer.is_valid():
        # print('serializer:', serializer)
        username = serializer.data.get('username')
        # print('serializer_username:', username)
        # print('type_serializer_username:', type(username))
        password = serializer.data.get('password')
        # print('serializer_password:', password)
        # user = User.objects.get(username=username)
        # print(user)
        user  = authenticate(username=username, password=password)
        # print('authenticate_user:', type(user))

        if  user is not None:
            # print("not none")

            login(request, user)
            # print("logged in:", request.user.username)
            # print('request_user',request.user)
            # print('request_user_username',request.user.id)
            uid=User.objects.get(username=request.user)
            print('uid.......',uid.pk)

            user_id=User_details.objects.get(user_id=uid.pk)
            user_id_serializer=user_details_serializer_all(user_id)
            user_id_serializer_data=user_id_serializer.data
            print('user_id_serializer_data',user_id_serializer.data)
            # print(user_id,user_id.Company_id,user_id.Company_id.Company_Logo)
            node_lr=get_node_LR(user_id_serializer_data['user_id'],"User")
            # print("node_lr",node_lr)
            immediate_prt=get_immediate_parent(node_lr['left'],node_lr['right'])
            # print('immediate_prt',immediate_prt)
            pages=get_descendent(immediate_prt['immediate_parent']['immediate_left'], immediate_prt['immediate_parent']['immediate_right'], "Page","node")
            print('Pagess',pages)
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

    try:
        logger.info('machine_list: %s',request.user)
        current_user=request.user
        if current_user.is_authenticated:
            logger.info('machine_list...!')

            # user_id = User_details.objects.get(user_id__username="user1")
            # user_id_serializer = user_details_serializer_all(user_id)
            # user_id_serializer_data = user_id_serializer.data
            # print('user_id_serializer_data', user_id_serializer.data)
            node_id=request.query_params.get('node_id')
            node_lr = get_node_LR(node_id, "Layer")
            # print("node_lr", node_lr)
            # grandparent_lr=get_grandparent(node_lr['left'],node_lr['right'])
            # print('grandparent_lr',grandparent_lr)
            get_machines=get_descendent(node_lr['left'],node_lr['right'],"Machine","node")
            # print('get_machines',get_machines)
            # machines = [node['node_id'] for node in get_machines['descendents']]
            machines = get_machines['descendents']
            # print(machines)
            # Querying MachineDetails model to get machine details
            machine_names_query = MachineDetails.objects.filter(id__in=machines)
            # print('machines_query',machine_names_query)
            machine_details_serializer_data=machine_details_serializer_machine_id_machine_name(machine_names_query,many=True).data
            # print('machine_details_serializer_all_data',machine_details_serializer_data)
            # Creating a list of dictionaries with 'Machine_id' and 'Machine_Name'
            machines_list = [{'Machine_id': machine.id, 'Machine_Name': machine.Machine_Name} for machine in
                             machine_names_query]

            # print(machines_list)

            return JsonResponse({"machines":machine_details_serializer_data})
        else:
            return JsonResponse({"status": "login_required"})

    except Exception as e:

        return JsonResponse({"status": "error", "message": str(e)})


@api_view(['GET'])

def Machine_module(request):#dropdown
    try:
        logger.info('machine_module: %s', request.user)
        current_user = request.user
        if current_user.is_authenticated:
            # user_id=10#from frontend
            # print('request.headers',request.headers)
            # print('request.headers',request.headers['user-id'])
            user_id=request.headers['user-id']
            # print("user_id||||||||||||||||",user_id)
            drop_down=dropdown(user_id)


            user_left_right=get_node_LR(user_id,"User")
            im_lr=get_immediate_parent(user_left_right['left'], user_left_right['right'])

            sub_pages=get_descendent(im_lr['immediate_parent']['immediate_left'],im_lr['immediate_parent']['immediate_right'],"Subpage","node")
            # print('sub_pages',sub_pages)

            return JsonResponse({"drop_down":drop_down,"sub_pages":sub_pages["descendents"]})
        else:
            return JsonResponse({"status": "login_required"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@api_view(['GET'])

def Trail_module(request):#dropdown
    try:
        logger.info('trail module: %s', request.user)
        current_user=request.user
        if current_user.is_authenticated:

            # user_id=10#from frontend
            # print('request.headers',request.headers)
            # print('request.headers',request.headers['user-id'])
            user_id=request.headers['user-id']
            # print("user_id||||||||||||||||",user_id)
            drop_down=dropdown(user_id)


            user_left_right=get_node_LR(user_id,"User")
            # im_lr=get_immediate_parent(user_left_right['left'], user_left_right['right'])

            # sub_pages=get_descendent(im_lr['immediate_parent']['immediate_left'],im_lr['immediate_parent']['immediate_right'],"Subpage","node")
            # print('sub_pages',sub_pages)

            return JsonResponse({"drop_down":drop_down})
        else:
            return JsonResponse({"status": "login_required"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@api_view(['GET'])

def Report_module(request):#dropdown
    try:
        logger.info('report module: %s', request.user)
        current_user = request.user
        if current_user.is_authenticated:

            # user_id=10#from frontend
            # print('request.headers',request.headers)
            # print('request.headers',request.headers['user-id'])
            user_id=request.headers['user-id']
            # print("user_id||||||||||||||||",user_id)
            drop_down=dropdown(user_id)


            user_left_right=get_node_LR(user_id,"User")
            im_lr=get_immediate_parent(user_left_right['left'], user_left_right['right'])

            Reports_Type=get_descendent(im_lr['immediate_parent']['immediate_left'],im_lr['immediate_parent']['immediate_right'],"Report","node")
            # print('sub_pages',Reports_Type)
            report_des = Reports_Type['descendents']
            # report_title_names = MachineCardsList.objects.filter(id__in=report_des)
            report=[]
            report_title_names = MachineCardsList.objects.filter(id__in=report_des).values('Title')
            # print('report_title_names',report_title_names)
            for i in report_title_names:
                # print('i',i)
                report.append(i['Title'])


            return JsonResponse({"drop_down":drop_down,"report_titles":report})
        else:
            return JsonResponse({"status": "login_required"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})






@api_view(['GET'])

def Machines_sub_details(request):#node_id= machine_id
    try:
        logger.info('Machines_sub_details: %s', request.user)
        current_user = request.user
        if current_user.is_authenticated:

            if "node_id" in request.GET and "module" in request.GET:
                module = request.GET.get('module')
                node_id = request.GET.get('node_id')

                switch_dict = {
                    "5": lambda: JsonResponse(Details(node_id)),
                    "6": lambda: JsonResponse(machine_kpis(node_id)),
                    "7": lambda: JsonResponse({"iostatus": Machine_Iostatus(node_id)}),
                    "8": lambda: JsonResponse({"control": Machine_Control(node_id)}),
                    "9": lambda: JsonResponse({"status": 'Settings under development'}),
                    'default': lambda: JsonResponse({"status": 'please give correct module'}),
                }

                # Execute the corresponding function from the switch_dict or the default function
                result = switch_dict.get(module, switch_dict['default'])()

                return result
            else:
                resultant = {"status": 'enter_correct__node_id_and_module'}
                return JsonResponse(resultant)
        else:
            return JsonResponse({"status": "login_required"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})



@api_view(['GET'])

def Trail_details(request):#node_id,date
    try:
        logger.info('Trail_details: %s', request.user)
        current_user = request.user
        if current_user.is_authenticated:

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
                    # digital_input
                    # digital_output
                    # analog_input
                    # analog_output
                    # others

                    trail_result_output={
                        "data":Trails_data['digital_input']+Trails_data['digital_output']+Trails_data['analog_input']+
                        Trails_data['analog_output']+Trails_data['others'],
                        "timestamp":trail["Timestamp"]

                    }
                    trail_result.append(trail_result_output)
                # print('length...................',len(trail_result))

                return JsonResponse({"machine_details": {
                        "node_id":node_id,
                        "machine_name": machine_name,
                        "machine_id":machine_id

                    },"Trail_Details":trail_result})

            else:
                return {"status": "please enter valid node_id"}
        else:
            return JsonResponse({"status": "login_required"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})



# @api_view(['POST'])
@api_view(['POST'])
def Reports_details(request):
    try:
        logger.info('Reports_details: %s', request.user)
        current_user = request.user
        if current_user.is_authenticated:

            report_type = request.data.get('report_type')
            machine_id = request.data.get('machine_id')
            user_id = request.data.get('user_id')
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

            except :
                return JsonResponse({"error": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS' format."},
                                    status=status.HTTP_400_BAD_REQUEST)

            # try:
            #     node = MachineDetails.objects.get(pk=node_id)
            #     print('node',node)
            # except MachineDetails.DoesNotExist:
            #     error_message = "Please enter a valid node_machine_id."
            #     return JsonResponse({"status": error_message}, status=400)

            report_frontend_data=Reports_data(user_id,machine_id,start_datetime,end_datetime,report_type)

            return JsonResponse({"report_details":report_frontend_data})
        else:
            return JsonResponse({"status": "login_required"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})








@api_view(['PUT'])
def machine_control(request):
    try:
        logger.info('machine_control: %s', request.user)
        current_user = request.user
        if current_user.is_authenticated:

            # print('******',request.data)

            machine_id=request.data.get('machine_id')
            name=request.data.get('name')
            value=request.data.get('value')
            Type=request.data.get('type')
            machine = MachineDetails.objects.get(pk=machine_id)
            # print('pk',machine.Machine_id)
            input_output_data = IOList.objects.filter(IO_Group=machine.IO_Group_Id,IO_type=Type).order_by('id').values_list('IO_name',flat=True)
            output = list(input_output_data).index(name)
            # print('index***********',list(input_output_data).index(name))
            # print('input_output_data----------',input_output_data)
            # print('output----------',output)
            # print('machine_id,name,value', machine_id,name,value)

            control_json = {"mid":machine.Machine_id,"parameter_type":Type, "data":{"output":output, "value":value}}
            # client.publish("websocket_data", json.dumps(control_json))
            client.publish("controls", json.dumps(control_json))
            # return JsonResponse({"status":list(input_output_data).index(name)})
            return JsonResponse({"status":"data has been sent"})
        else:
            return JsonResponse({"status": "login_required"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@api_view(['GET'])

def dashboard(request):
    try:
        logger.info('dashboard: %s', request.user)
        current_user = request.user
        if current_user.is_authenticated:

            # user_id = 10
            user_id = request.headers['user-id']

            user_lr = get_node_LR(user_id, "User")
            layer = get_grandparent(user_lr['left'], user_lr['right'])
            department = get_immediate_parent(user_lr['left'], user_lr['right'])
            get_dashboard = get_descendent(department['immediate_parent']['immediate_left'],
                                           department['immediate_parent']['immediate_right'],'Dashboard','node')
            get_machines = get_descendent(layer['grandparent']['grandparent_l'],layer['grandparent']['grandparent_r'],
                                          'Machine','node')
            machines = get_machines['descendents']
            dash = get_dashboard['descendents']
            # print(machines)
            # print('dash',dash)
            # Querying MachineDetails model to get machine details
            total_count_result=count_machines(machines)
            dashboard_cards = dashboard_data(dash)
            # print('total_count_result',total_count_result)
            statuss=total_count_result[1]


            return JsonResponse({'total_count_result':total_count_result[0],"machine_status":statuss,
                                 'dashboard_cards':dashboard_cards})
        else:
            return JsonResponse({"status": "login_required"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})



# new data added to nested sets using api's starts from here ..............................

@api_view(['GET'])


def add_new_node(request):  # add child node
    parent_id = request.query_params.get('parent_id')
    node_name = request.query_params.get('node_name')
    pro_name = request.query_params.get('property')

    parent = Nested_Table.objects.get(id=parent_id)

    parent_left = parent.Node_Left

    Nested_Table.objects.filter(Node_Right__gt=parent_left).update(Node_Right=models.F('Node_Right') + 2)
    Nested_Table.objects.filter(Node_Left__gt=parent_left).update(Node_Left=models.F('Node_Left') + 2)

    Nested_Table.objects.create(Node_Id=node_name, Node_Left=parent_left + 1,
                                Node_Right=parent_left + 2, Property=pro_name)

    return Response({"message": "new Child node added successfully"})

@api_view(['GET'])

def delete_node_and_uplift_the_descendants(request):
    node_id = request.query_params.get('node_id')  # pk of node_id

    node = Nested_Table.objects.get(id=node_id)
    node_left = node.Node_Left
    node_right = node.Node_Right
    # pro_name = node.Property

    Nested_Table.objects.filter(id=node_id).delete()
    Nested_Table.objects.filter(Node_Left__range=(node_left, node_right)).update(
        Node_Left=models.F('Node_Left') - 1,
        Node_Right=models.F('Node_Right') - 1
    )
    Nested_Table.objects.filter(Node_Right__gt=node_right).update(Node_Right=models.F('Node_Right') - 2)
    Nested_Table.objects.filter(Node_Left__gt=node_right).update(Node_Left=models.F('Node_Left') - 2)

    return Response({"message": "Node deleted and descendants uplifted successfully"})

@api_view(['GET'])

def get_primary_key(request):
    node_id = request.query_params.get('node_id')
    pro_name=request.query_params.get('property')
    node = Nested_Table.objects.get(Node_Id=node_id,Property=pro_name)
    # print('node',node.id)

    return Response({"primary_key_id":node.id })


