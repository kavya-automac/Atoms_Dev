from datetime import datetime

from Atoms_users.models import Alarm_data


def demo_alarm(data_dict,datapoint,latest_record,previous_record):
    time_data = latest_record.Timestamp
    # timestamp_dt = datetime.fromisoformat(str(time_data))

    # Format the datetime object
    # formatted_timestamp_str = timestamp_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    if datapoint == 'Digital_Input[0]':
        # print('.....>>>')
        Machine_Status_val = data_dict["get_value"]# datapoint value

        if latest_record and Machine_Status_val == 'Off':
            previous_v = eval(f'previous_record.{datapoint}')
            if previous_v == 'On':
                # print('????///????/')
                # response_data = {"alarm_message": "Message Off", "Timestamp": formatted_timestamp_str}
                create_alarm_row = Alarm_data(machine_id=data_dict['machine_id'], TimeStamp=time_data,
                                              Message="Machine Off")
                create_alarm_row.save()
            else:
                pass
        else:
            pass
    if datapoint == 'Analog_Input[0]':
        # print('.....>>><<')

        temp_val = data_dict["get_value"]
        if temp_val < 50 or temp_val > 100:
            # print('????????/')
            create_alarm_row = Alarm_data(machine_id=data_dict['machine_id'], TimeStamp=time_data,
                                          Message="Temperature High")
            create_alarm_row.save()

        else:
            pass
    else:
        pass