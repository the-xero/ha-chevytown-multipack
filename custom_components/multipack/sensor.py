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
        # 변경: _attr_name을 영문으로 설정 (translation_key로 한글 이름 제어)
        self._attr_name = "Last Action"
        car_name = entry.data.get("car_name", "multipack")
        # unique_id를 소문자로 정규화
        self._attr_unique_id = f"{car_name.lower()}_last_action"
        # translation_key 설정 (영문 기반 entity_id, 한글 이름)
        self._attr_translation_key = "last_action"
        self._state = "대기 중"
        self._last_updated = None

    @property
    def device_info(self):
        """Return device info."""
        car_name = self._entry.data.get("car_name", "multipack")
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": car_name,
            "manufacturer": "Chevytown",
            "model": "Multipack Connected"
        }

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return "mdi:car-info"

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
