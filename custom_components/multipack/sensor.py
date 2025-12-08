from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
from datetime import datetime

async def async_setup_entry(hass, entry, async_add_entities):
    sensor = MultipackLastAction(hass, entry)
    async_add_entities([sensor])
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(entry.entry_id, {})
    hass.data[DOMAIN][entry.entry_id]["last_action_sensor"] = sensor

class MultipackLastAction(SensorEntity):
    def __init__(self, hass, entry):
        self._hass = hass
        self._entry = entry
        self._attr_name = "마지막 명령"
        self._attr_unique_id = f"{DOMAIN}_last_action_{entry.entry_id}"
        self._state = "대기 중"
        self._last_updated = None

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return "mdi:car"

    @property
    def extra_state_attributes(self):
        """Return extra state attributes."""
        return {
            "last_updated": self._last_updated.isoformat() if self._last_updated else None,
            "entry_id": self._entry.entry_id
        }

    async def async_update_state(self, msg):
        """Update state asynchronously."""
        self._state = msg
        self._last_updated = datetime.now()
        self.async_write_ha_state()
