# from __future__ import absolute_import, unicode_literals
# import os
# from datetime import timedelta
#
# from celery import Celery
# from celery.schedules import crontab
# from django.conf import settings
# print('^^^^ in celery.py ^^^^^^^')
#
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE','Atoms_Main.settings')
#
# app=Celery('Atoms_Main')
#
# app.conf.enable_utc=False
#
# app.conf.update(timezone='Asia/Kolkata')
#
# app.config_from_object(settings, namespace='CELERY')
#
# #beat settngs
#
# app.conf.beat_schedule={
#
#
#
#     'sending_periodically':{
#         'task':'Atoms_machines.tasks.dashboard_web',
#         'schedule':timedelta(seconds=1),
#     }
# }
# # Atoms_machines.send_task('Atoms_machines.io_status_websocket.dashboard_web', args=[user_id, dept])
#
# app.autodiscover_tasks()
# print('//////////',app.autodiscover_tasks())
# @app.task(bind=True)
# def debug_task(self):
#     print('-------------------------------------------------------',f'Request:{self.request!r}')
