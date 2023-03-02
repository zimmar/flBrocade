from .services.app_db import AppDb
from .services.app_logging import AppLogging
from .modules.san.core import SanSwitch

app_db = AppDb()
app_logging = AppLogging()
san_switch = SanSwitch()