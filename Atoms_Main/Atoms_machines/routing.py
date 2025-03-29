from django.urls import path
from . import consumers
print("in routing")
websocket_urlpatterns=[
    path('ws/machine_mqtt_data/', consumers.ChatConsumer.as_asgi()),
    path('ws/kpi_web_socket/', consumers.KpiConsumer.as_asgi()),
    path('ws/Control_Socket/', consumers.ControlSocket.as_asgi()),
    path('ws/dashboardSocket/', consumers.DashboardSocket.as_asgi())

]