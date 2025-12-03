from homeassistant.helpers.entity import Entity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
	# 센서 인스턴스 생성 및 등록, entry별로 hass.data에 보관
	sensor = MultipackLastAction()
	async_add_entities([sensor])
	hass.data.setdefault(DOMAIN, {})
	hass.data[DOMAIN].setdefault(entry.entry_id, {})
	hass.data[DOMAIN][entry.entry_id]["last_action_sensor"] = sensor

class MultipackLastAction(Entity):
	def __init__(self):
		self._attr_name = "마지막 명령"
		self._attr_unique_id = f"{DOMAIN}_last_action"
		self._state = "대기 중"

	@property
	def state(self):
		return self._state

	def update_state(self, msg):
		self._state = msg
		self.schedule_update_ha_state()
