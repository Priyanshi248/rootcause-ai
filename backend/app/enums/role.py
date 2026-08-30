from enum import Enum


class Role(str, Enum):
    ADMIN = "ADMIN"
    ENGINEER = "ENGINEER"
    SRE = "SRE"
    VIEWER = "VIEWER"