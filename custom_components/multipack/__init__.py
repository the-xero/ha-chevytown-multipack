from homeassistant.helpers import discovery
from .const import DOMAIN

async def async_setup(hass, config):
    """Set up the Multipack integration."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass, entry):
    """Set up a config entry by forwarding to platforms and storing entry data."""
    hass.data.setdefault(DOMAIN, {})
    # 각 entry 별로 데이터를 저장할 dict 생성
    hass.data[DOMAIN].setdefault(entry.entry_id, {})
    # 플랫폼 포워딩 (sensor, button)
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "button"])
    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry and platforms."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor", "button"])
    if unload_ok:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return unload_ok
