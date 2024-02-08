import json
# from .models import *
from django.apps import apps

def Machine_data_to_db(mqtt_machines_data):
    payload = json.loads(mqtt_machines_data)

    timestamp = payload['Timestamp'].split('.')[0]
    machine_id = payload['Machine_Id']
    machine_location = payload['Machine_Location']
    digital_input = payload.get('Digital_Input')
    digital_output = payload.get('Digital_Output')
    analog_input = payload.get('Analog_Input')
    analog_output = payload.get('Analog_Output')
    other=payload.get('Other')

    digital_input = [True if value.lower() == 'on' else False for value in digital_input]

    digital_output = [True if value.lower() == 'on' else False for value in digital_output]
    MachineRawData = apps.get_model('Atoms_machines', 'MachineRawData')
    existing_record = MachineRawData.objects.filter(Machine_Id=machine_id,Timestamp=timestamp).first()


    if existing_record is None:

        machine_data_storing = MachineRawData(
            # timestamp=timezone.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f'),

            Timestamp=timestamp,
            Machine_Id=machine_id,
            Machine_Location=machine_location,
            Digital_Input=digital_input,
            Digital_Output=digital_output,
            Analog_Input=analog_input,
            Analog_Output=analog_output,
            Other=other
        )



        machine_data_storing.save()
