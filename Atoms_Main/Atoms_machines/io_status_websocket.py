import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()


def io_websocket(connected_machine_data):

    machine_data = json.loads(connected_machine_data)
    machine_id=machine_data['Machine_Id']
    from Atoms_users.models import MachineDetails
    from Atoms_users.conversions import io_list_data, key_value_merge

    node_id = MachineDetails.objects.get(Machine_id=machine_id)
    print('node_id',node_id)
    keys = io_list_data(node_id.id)
    digital_input = machine_data['Digital_Input']
    digital_output = machine_data['Digital_Output']
    analog_input = machine_data['Analog_Input']
    analog_output = machine_data['Analog_Output']
    other = machine_data['Other']
    io_value_result ={
        "Digital_Input":digital_input,
        "Digital_Output":digital_output,
        "Analog_Input":analog_input,
        "Analog_Output":analog_output,
        "Other":other
    }
    result =key_value_merge(node_id,keys,io_value_result)


    data ={
        "node_id": node_id.id,
        "machine_id": machine_id,
        "machine_name": node_id.Machine_Name,
        "time_stamp": machine_data['Timestamp']
    }

    result.update(data)
    print('result websocket', result)
    iostatus_output={
        "iostatus": result
    }

    io_websocket_result = json.dumps(iostatus_output)

    try:
        async_to_sync(channel_layer.group_send)(str(machine_id)+'_io', {"type": "chat.message", "text": io_websocket_result})
    except Exception as e:
        print("io error - ", e)


def control_websocket(connected_machine_data):

    machine_data = json.loads(connected_machine_data)
    machine_id=machine_data['Machine_Id']
    from Atoms_users.models import MachineDetails
    from Atoms_users.conversions import io_list_data, key_value_merge

    node_id = MachineDetails.objects.get(Machine_id=machine_id)
    print('node_id',node_id)
    keys = io_list_data(node_id.id)
    digital_input = machine_data['Digital_Input']
    digital_output = machine_data['Digital_Output']
    analog_input = machine_data['Analog_Input']
    analog_output = machine_data['Analog_Output']
    other = machine_data['Other']
    control_value_result ={
        "Digital_Input":digital_input,
        "Digital_Output":digital_output,
        "Analog_Input":analog_input,
        "Analog_Output":analog_output,
        "Other":other
    }
    result =key_value_merge(node_id,keys,control_value_result)


    data ={
        "node_id": node_id.id,
        "machine_id": machine_id,
        "machine_name": node_id.Machine_Name,
        "time_stamp": machine_data['Timestamp']
    }

    result.update(data)
    print('result websocket', result)
    control_output={
        "control": result
    }

    control_websocket_result = json.dumps(control_output)

    try:
        async_to_sync(channel_layer.group_send)(str(machine_id)+'_control', {"type": "control.message", "text": control_websocket_result })
    except Exception as e:
        print("control error - ", e)
