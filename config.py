import dataclasses

@dataclasses.dataclass
class GlobalConfig:
  TRACKING_ENABLED = False
  PATH = None
  KEY = None

CONFIG = GlobalConfig()