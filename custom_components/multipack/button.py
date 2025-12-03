from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import COMMANDS, DOMAIN
import async_timeout

async def async_setup_entry(hass, entry, async_add_entities):
    buttons = []
    for key, value in COMMANDS.items():
        buttons.append(MultipackButton(key, value["name"], value["cmd"], entry))
    async_add_entities(buttons)

class MultipackButton(ButtonEntity):
    def __init__(self, key, name, cmd, entry, icon=None):
        self._attr_name = name
        self._attr_unique_id = f"multipack_{key}"
        self._cmd = cmd
        self._entry = entry
        self._icon = icon

    @property
    def icon(self):
        return self._icon

    async def async_press(self):
        id_ = self._entry.data["id"]
        key_ = self._entry.data["key"]
        url = f"https://mp.gmone.co.kr/api?id={id_}&key={key_}&cmd={self._cmd}"

        session = async_get_clientsession(self.hass)
        try:
            async with async_timeout.timeout(10):
                resp = await session.get(url)
                result = await resp.text()
        except Exception as exc:
            sensor = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {}).get("last_action_sensor")
            if sensor:
                sensor.update_state(f"{self._attr_name} 실패: {str(exc)}")
            return

        sensor = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {}).get("last_action_sensor")
        if sensor:
            sensor.update_state(f"{self._attr_name} 실행 완료")

