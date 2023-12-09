"""
This file contains configuration for resource package.
"""

import logging
from os import environ

from resources.config import resource_config

config_data = {
    "base_url": environ["PROXIMA_BASE_URL"],
    "enable_logging": True,
    "logger": logging,
    "nova_token": f"Basic {environ['NOVA_INTERNAL_TOKEN']}",
    "orbit_token": f"Basic {environ['ORBIT_INTERNAL_TOKEN']}",
    "celestial_token": f"Basic {environ['CELESTIAL_INTERNAL_TOKEN']}",
}
resource_config.init(data=config_data)
