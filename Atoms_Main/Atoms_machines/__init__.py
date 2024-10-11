from . import mqtt_code
import logging

logger = logging.getLogger("django")
logger.info('init...!')
# print('init')
# mqtt_code.client.loop_start()
mqtt_code.client_1.loop_start()