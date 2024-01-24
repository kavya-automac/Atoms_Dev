
from django.urls import path
from .views import *

urlpatterns = [

    # path('get_node_LR_api/', get_node_LR_api),
    path('login/', login_view),
    path('logout/', logout_view, name='logout'),
    path('Machines_List/', Machines_List, name='logout'),

]

