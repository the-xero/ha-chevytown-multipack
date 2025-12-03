from homeassistant.components.button import ButtonEntity
from .const import COMMANDS, DOMAIN
import aiohttp

async def async_setup_entry(hass, entry, async_add_entities):
    buttons = []
    for key, value in COMMANDS.items():
        buttons.append(MultipackButton(key, value["name"], value["cmd"], entry))
    async_add_entities(buttons)

class MultipackButton(ButtonEntity):
    def __init__(self, key, name, cmd, entry):
        self._attr_name = name
        self._attr_unique_id = f"multipack_{key}"
        self._cmd = cmd
        self._entry = entry

    async def async_press(self):
        id_ = self._entry.data["id"]
        key_ = self._entry.data["key"]
        url = f"https://mp.gmone.co.kr/api?id={id_}&key={key_}&cmd={self._cmd}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                result = await resp.text()
        # 상태 저장
        hass = self.hass
        hass.states.async_set("sensor.multipack_last_action", f"{self._attr_name} 실행 완료")
