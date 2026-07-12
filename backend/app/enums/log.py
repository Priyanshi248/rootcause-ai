from enum import Enum


class LogSource(str, Enum):
    APPLICATION = "application"
    NGINX = "nginx"
    DOCKER = "docker"
    KUBERNETES = "kubernetes"
    SYSTEM = "system"
    CUSTOM = "custom"