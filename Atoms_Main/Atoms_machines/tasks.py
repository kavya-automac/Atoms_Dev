# import json
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from asgiref.sync import sync_to_async
# from celery import shared_task
#
# channel_layer = get_channel_layer()
#
#
# # @shared_task(bind=True)
# # @sync_to_async
# #
# # def dashboard_web(user_id,dept):
# #     print('in dash')
# #     # user_id = 10
# #     # print('dashboard_web function')
# #     # user_id = request.headers['user-id']
# #     from Atoms_users.Nested_Queries import get_node_LR, get_grandparent, get_immediate_parent, get_descendent
# #     from Atoms_users.api_functions import count_machines,dashboard_data
# #     user_lr = get_node_LR(user_id, "User")
# #     layer = get_grandparent(user_lr['left'], user_lr['right'])
# #     department = get_immediate_parent(user_lr['left'], user_lr['right'])
# #     get_dashboard = get_descendent(department['immediate_parent']['immediate_left'],
# #                                    department['immediate_parent']['immediate_right'], 'Dashboard', 'node')
# #     get_machines = get_descendent(layer['grandparent']['grandparent_l'], layer['grandparent']['grandparent_r'],
# #                                   'Machine', 'node')
# #     machines = get_machines['descendents']
# #     dash = get_dashboard['descendents']
# #     # print(machines)
# #     # print('dash', dash)
# #     # Querying MachineDetails model to get machine details
# #     total_count_result = count_machines(machines)
# #     dashboard_cards = dashboard_data(dash)
# #     # print('dashboard_cards', dashboard_cards)
# #     dash_web_response ={'total_count_result': total_count_result,
# #                          'dashboard_cards': dashboard_cards}
# #
# #     dashboard_resut = json.dumps(dash_web_response)
# #     print('dashboard_resut',dashboard_resut)
# #
# #     async_to_sync(channel_layer.group_send)(dept+'_dashboard',
# #                                             {"type": "dashboard.message", "text": dashboard_resut})
# #
