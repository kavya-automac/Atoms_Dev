import json
# from .models import *
import logging

from django.apps import apps


logger = logging.getLogger("django")

logger.info('data storing file .....!')

def Machine_data_to_db(mqtt_machines_data):
    print("in Machine_data_to_db")
    payload = json.loads(mqtt_machines_data)


    timestamp = payload['timestamp'].split('.')[0]
    machine_id = payload['machine_id']
    machine_location = payload['machine_location']
    digital_input = payload.get('digital_inputs')
    digital_output = payload.get('digital_outputs')
    analog_input = payload.get('analog_inputs')
    analog_output = payload.get('analog_outputs')
    other=payload.get('other')

    digital_input = [True if value.lower() == 'on' else False for value in digital_input]

    digital_output = [True if value.lower() == 'on' else False for value in digital_output]
    MachineRawData = apps.get_model('Atoms_machines', 'MachineRawData')
    existing_record = MachineRawData.objects.filter(Machine_Id=machine_id,Timestamp=timestamp).first()


    if existing_record is None:
        logger.info('data storing.....!')

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
