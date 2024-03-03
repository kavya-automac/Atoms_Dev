import time

from django.http import JsonResponse
from .serializers import *
from . models import *
from Atoms_machines.models import MachineRawData
from Atoms_machines.serializers import machineValues_serializer


# from ..Atoms_machines.models import *


def io_keys(node_id):
    try:
        node_group = MachineDetails.objects.get(id=node_id)
    except MachineDetails.DoesNotExist:
        error_message = "Please enter a valid machine_id."
        return JsonResponse({"status": error_message}, status=400)  # Return an error response

    # print('node_group', node_group)
    group_data = node_group.IO_Group_Id
    machine_id=node_id.Machine_id
    # print('group_data', group_data)
    input_output_data = IOList.objects.filter(IO_Group=group_data).order_by('id')

    input_output_data_serializer = IO_list_serializer(input_output_data, many=True)
    input_output_data_serializer_data = input_output_data_serializer.data
    digital_input_keys = []
    digital_output_keys = []
    analog_input_keys = []
    analog_output_keys = []
    other_keys = []

    for i in range(len(input_output_data)):
        # print('iiiiiiiiiii',i)
        if input_output_data_serializer_data[i]['IO_type'] == "analog_output":
            analog_output_keys.append(input_output_data_serializer_data[i]['IO_name'])

        if input_output_data_serializer_data[i]['IO_type'] == "analog_input":
            analog_input_keys.append(input_output_data_serializer_data[i]['IO_name'])
        if input_output_data_serializer_data[i]['IO_type'] == "digital_output":
            digital_output_keys.append(input_output_data_serializer_data[i]['IO_name'])

        if input_output_data_serializer_data[i]['IO_type'] == "digital_input":
            # print('iiiiiiiiiiiiiiiiiiiii',i ,input_output_data_serializer_data[i]['IO_name'])
            digital_input_keys.append(input_output_data_serializer_data[i]['IO_name'])
        if input_output_data_serializer_data[i]['IO_type'] == "other":
            # print('iiiiiiiiiiiiiiiiiiiii',i ,input_output_data_serializer_data[i]['IO_name'])
            other_keys.append(input_output_data_serializer_data[i]['IO_name'])
    return {"machine_id":machine_id,"digital_input_keys":digital_input_keys,"digital_output_keys":digital_output_keys,
            "analog_input_keys":analog_input_keys,"analog_output_keys":analog_output_keys,
            "other_keys":other_keys}


def io_list_data(node_id):#machine_id 1 ,2....
    try:
        node_group = MachineDetails.objects.get(id=node_id)

    except MachineDetails.DoesNotExist:
        error_message = "Please enter a valid machine_id."
        return JsonResponse({"status": error_message}, status=400)  # Return an error response

    # print('node_group', node_group)
    group_data = node_group.IO_Group_Id
    machine_id=node_group.Machine_id
    # print('group_data', group_data)
    input_output_data = IOList.objects.filter(IO_Group=group_data).order_by('id')

    input_output_data_serializer = IO_list_serializer(input_output_data, many=True)
    input_output_data_serializer_data = input_output_data_serializer.data
    # print('input_output_data_serializer_data',input_output_data_serializer_data)
    # result={
    #     "input_output_data_serializer_data":input_output_data_serializer_data,
    #     "machine_id":machine_id
    # }

    digital_input_keys=[]
    digital_output_keys=[]
    analog_input_keys=[]
    analog_output_keys=[]
    others_keys=[]

    # others_keys=[{"name":p['IO_name'],"unit":p['IO_Unit'],"control":p['Control'],"color":p['IO_color']} and result["input_output_data_serializer_data"].remove(p) for p in result["input_output_data_serializer_data"]  if "other" == p['IO_type']]
    # print(
    #     'before loop', input_output_data_serializer_data
    # )

    modified_list = input_output_data_serializer_data[:]
    """ removing data from original list(input_output_data_serializer_data)
     and looping with updated data list
      example code here :
      original_list = [1, 2, 3, 4, 5]

        # Create a copy of the original list
        modified_list = original_list[:]
        
        # Iterate over the copy and remove elements from the original list
        for element in modified_list:
            original_list.remove(element)
        
        # Now original_list is empty, and modified_list contains the original elements
        print("original_list:", original_list)
        print("modified_list:", modified_list)
        
        
      """

    for di in modified_list:
        # print('di>>>>>>>>>>>>>>>>>>>>>>>',di)
        # time.sleep(1)
        if di['IO_type'] == "digital_input":
            digital_input_keys.append({
                "name": di['IO_name'],
                "unit": di['IO_Unit'],
                "control": di['Control'],
                "color": di['IO_color'],
                "iovalue": di['IO_value'],
                "type": di['IO_type']
            })
            input_output_data_serializer_data.remove(di)
    # print(
    #     'after d i',input_output_data_serializer_data
    # )
    # modified_list = input_output_data_serializer_data[:]

    for do in modified_list:
        if do['IO_type'] == "digital_output":
            digital_output_keys.append({
                "name": do['IO_name'],
                "unit": do['IO_Unit'],
                "control": do['Control'],
                "color": do['IO_color'],
                "iovalue": do['IO_value'],
                "type": do['IO_type']
            })
            input_output_data_serializer_data.remove(do)

    # print(
    #     'after d o', input_output_data_serializer_data
    # )
    # modified_list = input_output_data_serializer_data[:]


    for ai in modified_list:
        if ai['IO_type'] == "analog_input":
            analog_input_keys.append({
                "name": ai['IO_name'],
                "unit": ai['IO_Unit'],
                "control": ai['Control'],
                "color": ai['IO_color'],
                "iovalue": ai['IO_value'],
                "type": ai['IO_type']
            })
            # input_output_data_serializer_data.remove(ai)

    # modified_list = input_output_data_serializer_data[:]


    for ao in modified_list:
        if ao['IO_type'] == "analog_output":
            analog_output_keys.append({
                "name": ao['IO_name'],
                "unit": ao['IO_Unit'],
                "control": ao['Control'],
                "color": ao['IO_color'],
                "iovalue": ao['IO_value'],
                "type": ao['IO_type']
            })
            input_output_data_serializer_data.remove(ao)
    # print(
    #     'after a i', input_output_data_serializer_data
    # )
    # modified_list = input_output_data_serializer_data[:]


    for p in modified_list:
        if p['IO_type'] == "other":
            others_keys.append({
                "name": p['IO_name'],
                "unit": p['IO_Unit'],
                "control": p['Control'],
                "color": p['IO_color'],
                "iovalue": p['IO_value'],
                "type": p['IO_type']
            })
            input_output_data_serializer_data.remove(p)

    return {
        "digital_input_keys": digital_input_keys,
        "digital_output_keys": digital_output_keys,
        "analog_input_keys": analog_input_keys,
        "analog_output_keys": analog_output_keys,
        "others_keys": others_keys,
        "machine_id": machine_id
    }


def io_values(node_id,type,date=None):#machine_id="MAC_06"
    if type == "iostatus" or type == "control":
        machine_values_data = MachineRawData.objects.filter(Machine_Id=node_id).order_by('-Timestamp').first()
        last_valies_data_1 = machineValues_serializer(machine_values_data)
    elif type == "Trails":
        machine_values_data = MachineRawData.objects.filter(Machine_Id=node_id, Timestamp__date=date). \
        values('Timestamp','Machine_Id', 'Machine_Location', 'Digital_Input', 'Digital_Output',
        'Analog_Input', 'Analog_Output', 'Other').distinct('Timestamp').order_by('-Timestamp')

        last_valies_data_1 = machineValues_serializer(machine_values_data,many=True)

    # print('machine_values_data', machine_values_data)

    last_valies_data = last_valies_data_1.data
    # print("last_valies_data",last_valies_data)
    return last_valies_data


#
# {
#     "iostatus": {
#         "machine_id": "CSD2",
#         "machine_name": "Chamber 2",
#         "digital_input": [
#             {
#                 "name": "Compressor Status",
#                 "value": "Off",
#                 "color": "#FF0000"
#             }
#         ],
#         "digital_output": [],
#         "analog_input": [
#             {
#                 "name": "Temperature",
#                 "value": "23.00",
#                 "color": "#808080",
#                 "unit": "°C"
#             }
#         ],


def key_value_merge(node_id,keys,io_value_data):
    # io_key_data=io_list_data(node_id)#should call this  2 functions in key_value_merge
    # io_value_data=io_values(node_id)
    # keys=io_list_data(node_id)
    # print('keys',keys)
    # print('io_value_data',io_value_data)
    digital_input_result = []
    digital_output_result = []
    analog_input_result = []
    analog_output_result = []
    other_result = []

    # digital_input_keys=[ di['IO_name'] for di in io_key_data["input_output_data_serializer_data"]  if "digital_input" == di['IO_type']]
    # analog_input_keys=list(filter(lambda ai : "analog_input" in ai ,io_key_data["input_output_data_serializer_data"]))
    # print('digital_input_keys listtt',digital_input_keys)
    # print('analog_input_keys listtt',analog_input_keys)
    for di in range(len(io_value_data['Digital_Input'])):
        # print("????????????????",io_value_data['Digital_Input'][di])
        # print("????????????????",type(io_value_data['Digital_Input'][di]))
        if isinstance(io_value_data['Digital_Input'][di], str):
            io_value= "On" if io_value_data['Digital_Input'][di].lower() == "on" else "Off"
        else:
            # Handle the case when it's not a string, for example, by assigning a default value
            io_value = "On" if io_value_data['Digital_Input'][di] else "Off"
        # print("io_value",io_value)


        io_name= keys['digital_input_keys'][di]['name']
        io_unit = keys['digital_input_keys'][di]['unit']
        io_control = str(keys['digital_input_keys'][di]['control'])

        io_value_range= keys['digital_input_keys'][di]['iovalue']
        # print("----------------------",io_value_range.index(io_value))
        io_color= keys['digital_input_keys'][di]['color'][io_value_range.index(io_value)]
        io_type = keys['digital_input_keys'][di]['type']
        data={
            "name":io_name,
            "value":io_value,
            "color":io_color,
            "unit":io_unit,
            "control": io_control,
            "type": io_type
        }
        digital_input_result.append(data)
    # print('digital_input_keys',digital_input_result)

    for do in range(len(io_value_data['Digital_Output'])):
        if isinstance(io_value_data['Digital_Input'][do], str):
            io_value = "On" if io_value_data['Digital_Input'][do].lower() == "on" else "Off"
        else:
            # Handle the case when it's not a string, for example, by assigning a default value
            io_value = "On" if io_value_data['Digital_Input'][do] else "Off"

        # io_value = "On" if io_value_data['Digital_Output'][do].lower() == "on" else "Off"
        io_name = keys['digital_output_keys'][do]['name']
        io_unit =  keys['digital_output_keys'][do]['unit']
        io_control =  str(keys['digital_output_keys'][do]['control'])
        io_type = keys['digital_output_keys'][do]['type']



        io_value_range = keys['digital_input_keys'][do]['iovalue']
        # print("----------------------",io_value_range.index(io_value))
        io_color = keys['digital_output_keys'][do]['color'][io_value_range.index(io_value)]
        data = {
            "name": io_name,
            "value": io_value,
            "color": io_color,
            "unit":io_unit,
            "control": io_control,
            "other":io_type
        }
        digital_output_result.append(data)
    # print('digital_input_keys', digital_output_result)

    for ai in range(len(io_value_data['Analog_Input'])):
        io_value = str(io_value_data['Analog_Input'][ai])


        io_name = keys['analog_input_keys'][ai]['name']
        # print('iooooooooooooooonameeeeee',io_name)
        io_unit = keys['analog_input_keys'][ai]['unit']
        io_control = str(keys['analog_input_keys'][ai]['control'])
        io_type = keys['analog_input_keys'][ai]['type']


    # io_value_range = io_key_data["input_output_data_serializer_data"][ai]['IO_value']
        io_color = keys['analog_input_keys'][ai]['color'][0]
        data = {
            "name": io_name,
            "value": io_value,
            "color": io_color,
            "unit":io_unit,
            "control": io_control,
            "type": io_type
        }
        analog_input_result.append(data)
    # print('analog_input_result', analog_input_result)

    for ao in range(len(io_value_data['Analog_Output'])):
        io_value = str(io_value_data['Analog_Output'][ao])
        io_name = keys['analog_output_keys'][ao]['name']
        io_unit =  keys['analog_output_keys'][ao]['unit']
        io_control =  str(keys['analog_output_keys'][ao]['control'])
        io_type = keys['analog_output_keys'][ao]['type']



        # io_value_range = io_key_data["input_output_data_serializer_data"][ai]['IO_value']
        io_color = keys['analog_output_keys'][ao]['color'][0]
        data = {
            "name": io_name,
            "value": io_value,
            "color": io_color,
            "unit":io_unit,
            "control": io_control,
            "type": io_type
        }
        analog_output_result.append(data)
    # print('analog_output_result', analog_output_result)

    for param in range(len(io_value_data['Other'])):
        io_value = str(io_value_data['Other'][param])
        io_name = keys['others_keys'][param]['name']
        io_unit = keys['others_keys'][param]['unit']
        io_control = str(keys['others_keys'][param]['control'])
        # io_value_range = io_key_data["input_output_data_serializer_data"][ai]['IO_value']
        io_color = keys['others_keys'][param]['color'][0]
        io_type = keys['others_keys'][param]['type']

        data = {
            "name": io_name,
            "value": io_value,
            "color": io_color,
            "unit":io_unit,
            "control":io_control,
            "type": io_type
        }
        other_result.append(data)
    # print('other_result', other_result)


    return {
        "digital_input": digital_input_result,
        "digital_output": digital_output_result,
        "analog_input": analog_input_result,
        "analog_output": analog_output_result,
        "others": other_result,

    }

