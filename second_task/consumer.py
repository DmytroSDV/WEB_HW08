import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import pika

from conn_modd.models import Contact
import conn_modd.connect

