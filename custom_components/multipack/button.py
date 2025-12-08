from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import COMMANDS, DOMAIN
import async_timeout
import logging
import json

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    buttons = []
    car_name = entry.data.get("car_name", "car")
    for key, value in COMMANDS.items():
        buttons.append(MultipackButton(
            hass,
            key,
            value["name"],
            value["cmd"],
            entry,
            car_name=car_name,
            icon=value.get("icon")
        ))
    async_add_entities(buttons)

class MultipackButton(ButtonEntity):
    def __init__(self, hass, key, name, cmd, entry, car_name=None, icon=None):
        self._hass = hass
        self._attr_name = name
        car_prefix = car_name.lower() if car_name else "multipack"
        # unique_id를 소문자로 정규화하여 entity_id 생성 제어
        self._attr_unique_id = f"{car_prefix}_{cmd}"
        # translation_key를 cmd 기반으로 설정 (영문 기반 entity_id 생성)
        self._attr_translation_key = cmd.lower()
        self._cmd = cmd
        self._entry = entry
        self._icon = icon
        self._car_name = car_name
        self._attr_should_poll = False

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._car_name,
            "manufacturer": "Chevytown",
            "model": "Multipack Connected"
        }

    @property
    def icon(self):
        return self._icon

    async def async_press(self):
        """Handle button press."""
        id_ = self._entry.data["id"]
        key_ = self._entry.data["key"]
        url = f"https://mp.gmone.co.kr/api?id={id_}&key={key_}&cmd={self._cmd}"

        session = async_get_clientsession(self._hass)
        try:
            async with async_timeout.timeout(10):
                resp = await session.get(url)
                
                if resp.status == 200:
                    result = await resp.text()
                    _LOGGER.debug(f"[{self._attr_name}] API 응답: {result}")
                    
                    # 응답 파싱 (JSON 또는 텍스트)
                    success = await self._parse_response(result)
                    if success:
                        _LOGGER.info(f"{self._attr_name} 실행 완료")
                        await self._update_sensor(f"✓ {self._attr_name}")
                    else:
                        _LOGGER.warning(f"{self._attr_name} 실행 실패: {result}")
                        await self._update_sensor(f"✗ {self._attr_name}")
                else:
                    _LOGGER.error(f"API 오류 - 상태 코드: {resp.status}")
                    await self._update_sensor(f"✗ {self._attr_name} (HTTP {resp.status})")
                    
        except async_timeout.TimeoutError:
            _LOGGER.error(f"{self._attr_name}: 타임아웃 (10초)")
            await self._update_sensor(f"✗ {self._attr_name} (타임아웃)")
        except Exception as exc:
            _LOGGER.error(f"{self._attr_name} 실행 중 오류: {type(exc).__name__}: {exc}")
            await self._update_sensor(f"✗ {self._attr_name} ({type(exc).__name__})")

    async def _parse_response(self, response: str) -> bool:
        """Parse API response to determine success."""
        try:
            # JSON 응답 시도
            data = json.loads(response)
            # API 응답 형식에 따라 수정 필요
            return data.get("result") == "success" or data.get("status") == "ok"
        except (json.JSONDecodeError, ValueError):
            # 텍스트 응답: "success", "ok" 포함 여부 확인
            return "success" in response.lower() or "ok" in response.lower()

    async def _update_sensor(self, msg):
        """Update last action sensor."""
        sensor = self._hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {}).get("last_action_sensor")
        if sensor:
            await sensor.async_update_state(msg)
        else:
            _LOGGER.warning(f"센서를 찾을 수 없음: {self._entry.entry_id}")

