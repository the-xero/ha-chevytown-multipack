from homeassistant.helpers.entity import Entity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([MultipackLastAction()])

class MultipackLastAction(Entity):
    def __init__(self):
        self._attr_name = "마지막 명령"
        self._state = "대기 중"

    @property
    def state(self):
        return self._state

    def update_state(self, msg):
        self._state = msg
        self.schedule_update_ha_state()
