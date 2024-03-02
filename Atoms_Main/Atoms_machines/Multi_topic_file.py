from .Data_in_DB import *

def all_topics(connected_machine_data,topic):
    print('topic',topic)
    # print("topics in all topics file befor",topic)
    if topic == 'machine_data_dev':
        Machine_data_to_db(connected_machine_data)
    if topic == 'Maithri_test':
        print("mai")
        Machine_data_to_db(connected_machine_data)

