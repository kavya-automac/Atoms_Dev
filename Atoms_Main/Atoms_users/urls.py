
from django.urls import path
from .views import *

urlpatterns = [

    # path('get_node_LR_api/', get_node_LR_api),
    path('login/', login_view),
    path('logout/', logout_view, name='logout'),
    path('Machines_List/', Machines_List, name='logout'),
    path('Machine_module/', Machine_module),#dropdown
    path('Trail_List/', Machines_List, name='Trail_List'),
    path('Trail_module/', Trail_module, name='Trails_dropdown'),#trails dropdown
    path('Machines_sub_details/', Machines_sub_details),#trails dropdown
    path('Trail_details/', Trail_details, name='Trail_details'),#trails dropdown
    path('Reports_details/', Reports_details, name='Reports_details'),
    path('Reports_module/', Report_module, name='Reports_module'),
    path('Report_List/', Machines_List, name='Report_List'),

]


