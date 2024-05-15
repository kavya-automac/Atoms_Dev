import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from . import io_status_websocket
import schedule
import time
from asgiref.sync import sync_to_async
from .mqtt_code import client
from Atoms_users.Nested_Queries import user_department
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from . models import MachineRawData
channel_layer = get_channel_layer()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        connected_status=True

        query_string=self.scope['query_string'].decode()
        machine_id = query_string.split('=')[1].split('&')[0]

        # print('machine_id connect ',machine_id)
        client.publish("ws_con/"+machine_id, json.dumps({"con_status": connected_status, "machine_id":machine_id,"ws_grp":"iostatus"}))

        await self.channel_layer.group_add(str(machine_id)+'_io', self.channel_name)
        # group_name=self.scope["url_route"]["kwargs"]["group_name"]
        # print('group_name',group_name)
        await self.accept()
        from Atoms_users.api_functions import Machine_Iostatus_web2
        from Atoms_users.models import MachineDetails
        try:
            md = await sync_to_async(MachineDetails.objects.get)(Machine_id=machine_id)
            node_id = md.pk
            print('node_id connect', node_id)
            test = await Machine_Iostatus_web2(node_id)
            test_res = json.dumps({"iostatus":test})

            channel_layer = get_channel_layer()
            await channel_layer.group_send(str(machine_id)+'_io',
                                           {"type": "chat.message", "text": test_res})
        except Exception as e:
            status = json.dumps({"status": e})

            channel_layer = get_channel_layer()
            await channel_layer.group_send(str(machine_id)+'_io',
                                           {"type": "chat.message", "text": status})

        # md = MachineDetails.objects.get(Machine_id=machine_id)
        # node_id = md.pk
        # print('node_id connect', node_id)
        # test = Machine_Iostatus(node_id)
        # try:
        #     sync_to_async(channel_layer.group_send)(str(machine_id)+'_io',
        #                                             {"type": "chat.message", "text": test})
        # except Exception as e:
        #     print("io error - ", e)

    async def disconnect(self, close_code):
        connected_status = False

        query_string = self.scope['query_string'].decode()
        machine_id = query_string.split('=')[1]
        # print('machineid io websocket',machine_id)
        client.publish("ws_con/"+machine_id, json.dumps({"con_status": connected_status, "machine_id":machine_id,"ws_grp":"iostatus"}))

        await self.channel_layer.group_discard(str(machine_id)+'_io', self.channel_name)

    async def receive(self, text_data):
        query_string = self.scope['query_string'].decode()
        machine_id = query_string.split('=')[1]

        await self.channel_layer.group_send(str(machine_id)+'_io', {
            "type": "chat.message",
            "text": text_data  # Send the processed data as the message
        })

    async def chat_message(self, event):

        try:
            # Send the received data to the WebSocket connection
            await self.send(text_data=event["text"])
            # print("eventtttttttttttttttttttttttttt",event["text"])
            # await self.send(text_data=json.dumps(event["text"]))
            # await asyncio.sleep(1)
        except Exception as e:
            print("chat message error - ", e)



class KpiConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            connected_status = True
            # client.publish("ws_con","Connected")
            # print("Connected")
            query_string = self.scope['query_string'].decode()
            # print('query_string',query_string)
            machine_id = query_string.split('=')[1].split('&')[0]
            # username = query_string.split('=')[2]
            # print('username',username)
            client.publish("ws_con/"+machine_id, json.dumps({"con_status": connected_status, "machine_id": machine_id, "ws_grp": "kpis"}))


            await self.channel_layer.group_add(str(machine_id)+'_kpi', self.channel_name)

            await self.accept()
            from Atoms_users.api_functions import machine_kpis_web2
            from Atoms_users.models import MachineDetails
            try:
                md = await sync_to_async(MachineDetails.objects.get)(Machine_id=machine_id)
                node_id = md.pk
                print('node_id connect', node_id)
                test = await machine_kpis_web2(node_id)
               # changed currenttime to latest time
                latest_time_obj = await sync_to_async(
                    MachineRawData.objects.filter(Machine_Id=machine_id).order_by('-id').first)()


                print('..',latest_time_obj)
                if latest_time_obj:
                    print('..........................')
                    # Manually serialize the relevant fields to a dictionary
                    latest_time = {
                        'Timestamp': latest_time_obj.Timestamp.strftime(
                            '%Y-%m-%d %H:%M:%S') if latest_time_obj.Timestamp else None,
                    }
                    print('latest_time',latest_time)
                else:
                    latest_time = None

                print('latest_time websockety', latest_time)


                # Create the result data dictionary
                result_data =latest_time
                print('result_data',result_data)
                test.update(result_data)

                test_res = json.dumps(test)

                channel_layer = get_channel_layer()
                await channel_layer.group_send(str(machine_id)+'_kpi',
                                               {"type": "kpiweb", "text": test_res})

            except Exception as e:
                status = json.dumps({"status": e})

                channel_layer = get_channel_layer()
                await channel_layer.group_send(str(machine_id)+'_kpi',
                                               {"type": "kpiweb", "text": status})

            # Start calling kpi_socket function periodically
            self.machine_id = machine_id
            # self.username=username
            # self.scheduler_task = asyncio.create_task(self.schedule_kpi_socket())
        except Exception as e:
            print("errorrrrr",e)

    async def disconnect(self, close_code):
        # Cancel the scheduler task when disconnecting
        connected_status = False
        query_string = self.scope['query_string'].decode()
        machine_id = query_string.split('=')[1].split('&')[0]
        # username = query_string.split('=')[2]

        client.publish("ws_con/"+machine_id, json.dumps({"con_status": connected_status, "machine_id": machine_id, "ws_grp": "kpis"}))

        # if hasattr(self, 'scheduler_task'):# hasattr() function is an inbuilt utility function,\
        #     # which is used to check if an object has the given named attribute and return true if present, else false.
        #     self.scheduler_task.cancel()

        await self.channel_layer.group_discard(str(machine_id)+'_kpi', self.channel_name)

    # async def schedule_kpi_socket(self):
    #     while True:
    #         try:
    #
    #             await kpi_websocket.kpi_socket(self.machine_id)
    #             # await kpi_websocket.kpi_socket(self.username,self.machine_id)
    #
    #             await asyncio.sleep(2)
    #         except asyncio.CancelledError:
    #             break

    async def kpiweb(self, event):
        try:
            await self.send(text_data=event["text"])
        except Exception as e:
            print("kpi message error - ", e)


class ControlSocket(AsyncWebsocketConsumer):
    async def connect(self):
        connected_status=True

        query_string=self.scope['query_string'].decode()
        machine_id = query_string.split('=')[1]
        # print('machine_id connect ',machine_id)
        client.publish("control/"+machine_id, json.dumps({"con_status": connected_status, "machine_id":machine_id,"ws_grp":"control"}))




        await self.channel_layer.group_add(str(machine_id)+'_control', self.channel_name)
        await self.accept()
        from Atoms_users.api_functions import Machine_Control_web2
        from Atoms_users.models import MachineDetails
        try:
            md = await sync_to_async(MachineDetails.objects.get)(Machine_id=machine_id)
            node_id = md.pk
            print('node_id connect', node_id)
            test = await Machine_Control_web2(node_id)
            test_res = json.dumps({"control": test})

            channel_layer = get_channel_layer()
            await channel_layer.group_send(str(machine_id)+'_control',
                                           {"type": "control.message", "text": test_res})
        except Exception as e:
            status = json.dumps({"status": e})

            channel_layer = get_channel_layer()
            await channel_layer.group_send(str(machine_id)+'_control',
                                           {"type": "control.message", "text": status})


    async def disconnect(self, close_code):
        connected_status = False



        query_string = self.scope['query_string'].decode()
        machine_id = query_string.split('=')[1]
        # print('machineid',machine_id)
        client.publish("control/"+machine_id, json.dumps({"con_status": connected_status, "machine_id":machine_id,"ws_grp":"control"}))



    async def receive(self, text_data):
        query_string = self.scope['query_string'].decode()

        machine_id = query_string.split('=')[1]



        await self.channel_layer.group_send("mqtt_data", {
            "type": "control.message",
            "text": text_data  # Send the processed data as the message
        })

    async def control_message(self, event):


        try:
            await self.send(text_data=event["text"])

            # await asyncio.sleep(1)
        except Exception as e:
            print("control message error - ", e)


class DashboardSocket(AsyncWebsocketConsumer):
    async def connect(self):
        connected_status=True
        query_string=self.scope['query_string'].decode()
        user_id = query_string.split('=')[1]
        # print('user_id connect ',user_id)
        # user_lr = get_node_LR(user_id, "User")
        # department = get_immediate_parent(user_lr['left'], user_lr['right'])
        # get_department_node = Nested_Table.objects.get(Node_Left=department['immediate_parent']['immediate_left'],
        #                                                Node_Right=department['immediate_parent']['immediate_right'])
        # print('get_department_node',get_department_node)
        dept = await user_department(user_id)
        # print('...........................',dept)


        # client.publish("ws_con/", json.dumps({"con_status": connected_status, "machine_id":machine_id,"ws_grp":"control"}))

        await self.channel_layer.group_add(dept+'_dashboard', self.channel_name)
        await self.accept()

        self.scheduler_task = asyncio.create_task(self.dashboard_web_socket())

    async def disconnect(self, close_code):
        connected_status = False
        # print('ddddddddddddddddddddddddddd')

        query_string = self.scope['query_string'].decode()
        user_id = query_string.split('=')[1]
        # print('machineid',user_id)
        dept = await user_department(user_id)
        # print('...........................', dept)

        # client.publish("ws_con", json.dumps({"con_status": connected_status, "machine_id":machine_id,"ws_grp":"control"}))

        if hasattr(self, 'scheduler_task'):  # hasattr() function is an inbuilt utility function,\
            # which is used to check if an object has the given named attribute and return true if present, else false.
            self.scheduler_task.cancel()


        await self.channel_layer.group_discard(dept+'_dashboard', self.channel_name)

    async def receive(self, text_data):
        query_string = self.scope['query_string'].decode()

        user_id = query_string.split('=')[1]
        dept = await user_department(user_id)
        # print('...........................', dept)

        await self.channel_layer.group_send(dept+"_dashboard", {
            "type": "dashboard.message",
            "text": text_data  # Send the processed data as the message
        })

    async def dashboard_web_socket(self):
        while True:
            try:
                query_string = self.scope['query_string'].decode()
                user_id = query_string.split('=')[1]
                dept = await user_department(user_id)
                # print('..................schedule.........', dept)

                await io_status_websocket.dashboard_web(user_id,dept)

                # await io_status_websocket.dashboard_web(self.user_id)
                # await kpi_websocket.kpi_socket(self.username,self.machine_id)

                await asyncio.sleep(2)
            except asyncio.CancelledError:
                break

    async def dashboard_message(self, event):


        try:
            await self.send(text_data=event["text"])

            await asyncio.sleep(1)
        except Exception as e:
            print("dashboard message error - ", e)

#
# class DashboardSocket1(AsyncWebsocketConsumer):
#     async def connect(self):
#         query_string = self.scope['query_string'].decode()
#         user_id = query_string.split('=')[1]
#
#         dept = await user_department(user_id)
#
#         await self.channel_layer.group_add(dept+'_dashboard', self.channel_name)
#         await self.accept()
#         from Atoms_machines import io_status_websocket
#         await io_status_websocket.dashboard_web(user_id, dept)
#
#
#
#         # self.scheduler_task = asyncio.create_task(self.schedule_dashboard_web_socket())
#
#     async def disconnect(self, close_code):
#         query_string = self.scope['query_string'].decode()
#         user_id = query_string.split('=')[1]
#         dept = await user_department(user_id)
#
#         # if hasattr(self, 'scheduler_task'):
#         #     self.scheduler_task.cancel()
#
#         await self.channel_layer.group_discard(dept+'_dashboard', self.channel_name)
#
#     async def receive(self, text_data):
#         query_string = self.scope['query_string'].decode()
#
#         user_id = query_string.split('=')[1]
#         dept = await user_department(user_id)
#
#         await self.channel_layer.group_send(dept+"_dashboard", {
#             "type": "dashboard.message",
#             "text": text_data  # Send the processed data as the message
#         })
#
#     # async def schedule_dashboard_web_socket(self):
#     #     try:
#     #         query_string = self.scope['query_string'].decode()
#     #         user_id = query_string.split('=')[1]
#     #         dept = await user_department(user_id)
#     #         await io_status_websocket.dashboard_web(user_id, dept)
#     #     except asyncio.CancelledError:
#     #         return  # Exit if the task is cancelled
#     #     except Exception as e:
#     #         print("Error in scheduling dashboard_web_socket:", e)
#     #
#     #     # Schedule the next call after 5 seconds
#     #     # asyncio.get_event_loop().call_later(1, self.schedule_dashboard_web_socket)
#
#     async def dashboard_message(self, event):
#
#         try:
#             await self.send(text_data=event["text"])
#
#         except Exception as e:
#             print("dashboard message error - ", e)

# con_fun=dash_obj.connect()