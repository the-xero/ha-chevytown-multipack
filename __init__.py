from homeassistant.helpers import discovery
from .const import DOMAIN

async def async_setup(hass, config):
    """Set up the Multipack integration."""
    hass.data[DOMAIN] = {}
    return True
