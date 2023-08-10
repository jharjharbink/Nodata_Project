import logging
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

chanel = logging.StreamHandler(sys.stdout)
chanel.setLevel(logging.DEBUG)

logger.addHandler(chanel)
