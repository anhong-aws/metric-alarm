# constants.py

# Configuration keys
ACCOUNT_ID = "account_id"
ROLE = "role"
MINUTES = 'minutes'
PERIOD = 'period'
SUM = 'Sum'

# SNS flags
SEND_SNS_FLAG = 'send_sns_flag'
SEND_LINKED_SNS_FLAG = 'send_linked_sns_flag'
AUTO_DISABLE_SERVICE_FLAG = 'auto_disable_service_flag'

# SNS topic names
PAYER_TOPIC_NAME = 'payer_topic_name'
LINKED_TOPIC_NAME = 'linked_topic_name'

# Threshold and points
THRESHOLD = 'threshold'
AUTO_DISABLE_SERVICE_THRESHOLD='auto_disable_service_threshold'
CONSECUTIVE_POINTS = 'consecutive_points'

from enum import Enum

class Status(Enum):
    OPEN = 'open'
    CLOSE = 'close'