import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async


channel_layer = get_channel_layer()


def io_websocket(connected_machine_data):

    machine_data = json.loads(connected_machine_data)
    machine_id=machine_data['machine_id']
    from Atoms_users.models import MachineDetails
    from Atoms_users.conversions import io_list_data, key_value_merge

    node_id = MachineDetails.objects.get(Machine_id=machine_id)
    # print('node_id',node_id)
    keys = io_list_data(node_id.id)
    digital_input = machine_data['digital_inputs']
    digital_output = machine_data['digital_outputs']
    analog_input = machine_data['analog_inputs']
    analog_output = machine_data['analog_outputs']
    other = machine_data['other']
    io_value_result ={
        "Digital_Input":digital_input,
        "Digital_Output":digital_output,
        "Analog_Input":analog_input,
        "Analog_Output":analog_output,
        "Other":other
    }
    result =key_value_merge(node_id,keys,io_value_result)


    data ={
        "node_id": str(node_id.id),
        "machine_id": machine_id,
        "machine_name": node_id.Machine_Name,
        "Time": machine_data['timestamp']
    }

    result.update(data)
    # print('result websocket', result)
    iostatus_output={
        "iostatus": result
    }

    io_websocket_result = json.dumps(iostatus_output)
    # print('io_websocket_result',io_websocket_result)

    try:
        async_to_sync(channel_layer.group_send)(str(machine_id)+'_io', {"type": "chat.message", "text": io_websocket_result})
    except Exception as e:
        print("io error - ", e)


def control_websocket(connected_machine_data):

    machine_data = json.loads(connected_machine_data)
    machine_id=machine_data['machine_id']
    from Atoms_users.models import MachineDetails
    from Atoms_users.conversions import io_list_data, key_value_merge

    node_id = MachineDetails.objects.get(Machine_id=machine_id)
    # print('node_id',node_id)
    keys = io_list_data(node_id.id)
    digital_input = machine_data['digital_inputs']
    digital_output = machine_data['digital_outputs']
    analog_input = machine_data['analog_inputs']
    analog_output = machine_data['analog_outputs']
    other = machine_data['other']
    control_value_result ={
        "Digital_Input":digital_input,
        "Digital_Output":digital_output,
        "Analog_Input":analog_input,
        "Analog_Output":analog_output,
        "Other":other
    }
    control_result =key_value_merge(node_id,keys,control_value_result)


    data ={
        "node_id": str(node_id.id),
        "machine_id": machine_id,
        "machine_name": node_id.Machine_Name,
        "Time": machine_data['timestamp']
    }

    control_result.update(data)
    # print('result websocket', control_result)
    control_output={
        "control": control_result
    }

    control_websocket_result = json.dumps(control_output)

    try:
        async_to_sync(channel_layer.group_send)(str(machine_id)+'_control', {"type": "control.message", "text": control_websocket_result })
    except Exception as e:
        print("control error - ", e)




@sync_to_async
def dashboard_web(user_id,dept):
    # user_id = 10
    # print('dashboard_web function')
    # user_id = request.headers['user-id']
    from Atoms_users.Nested_Queries import get_node_LR, get_grandparent, get_immediate_parent, get_descendent
    from Atoms_users.api_functions import count_machines,dashboard_data
    user_lr = get_node_LR(user_id, "User")
    layer = get_grandparent(user_lr['left'], user_lr['right'])
    department = get_immediate_parent(user_lr['left'], user_lr['right'])
    get_dashboard = get_descendent(department['immediate_parent']['immediate_left'],
                                   department['immediate_parent']['immediate_right'], 'Dashboard', 'node')
    get_machines = get_descendent(layer['grandparent']['grandparent_l'], layer['grandparent']['grandparent_r'],
                                  'Machine', 'node')
    machines = get_machines['descendents']
    dash = get_dashboard['descendents']
    # print(machines)
    # print('dash', dash)
    # Querying MachineDetails model to get machine details
    total_count_result = count_machines(machines)
    dashboard_cards = dashboard_data(dash)
    # print('dashboard_cards', dashboard_cards)
    statuss = total_count_result[1]
    dash_web_response ={'total_count_result':total_count_result[0],"machine_status":statuss,
                                 'dashboard_cards':dashboard_cards}

    dashboard_resut = json.dumps(dash_web_response)

    async_to_sync(channel_layer.group_send)(dept+'_dashboard',
                                            {"type": "dashboard.message", "text": dashboard_resut})










