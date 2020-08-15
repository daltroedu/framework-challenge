import os
import sys

from dotenv import load_dotenv, find_dotenv

from app.config import config

load_dotenv(find_dotenv())

ENV_APP = os.environ.get('ENV_APP')
ENV_APP = ENV_APP[:1].upper() + ENV_APP[1:].lower()

_current = getattr(sys.modules['app.config.config'], '{0}Config'.format(ENV_APP))()

for atr in [f for f in dir(_current) if not '__' in f]:
    val = os.environ.get(atr, getattr(_current, atr))
    setattr(sys.modules[__name__], atr, val)