from django.conf import settings
from decimal import Decimal

CC_CONFIRMATIONS = getattr(settings, 'CC_CONFIRMATIONS', 2)
CC_ADDRESS_QUEUE = getattr(settings, 'CC_ADDRESS_QUEUE', 20)
CC_ALLOW_NEGATIVE_BALANCE = getattr(settings, 'CC_ALLOW_NEGATIVE_BALANCE', Decimal('0.001'))
