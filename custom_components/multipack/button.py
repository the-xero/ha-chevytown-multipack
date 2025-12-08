from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import COMMANDS, DOMAIN
import async_timeout
import logging
import json
import asyncio

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
        self._notification_entity = entry.data.get("notification_entity") or None
        self._attr_should_poll = False

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._car_name,
            "manufacturer": "@the-xero",
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
            # 변경: 타임아웃을 30초로 연장
            async with async_timeout.timeout(30):
                resp = await session.get(url)
                result = await resp.text()
                _LOGGER.debug(f"[{self._attr_name}] API 응답(status={resp.status}): {result}")

        except async_timeout.TimeoutError:
            _LOGGER.error(f"{self._attr_name}: HTTP 타임아웃 (30초)")
            # 네트워크 타임아웃은 즉시 timeout 처리
            await self._update_sensor(f"timeout: {self._attr_name}")
            return
        except Exception as exc:
            _LOGGER.error(f"{self._attr_name} 실행 중 오류: {type(exc).__name__}: {exc}")
            await self._update_sensor(f"timeout: {self._attr_name}")
            return

        # 1) API 응답 자체로 성공 판단 ({"success":1}, "1", JSON 숫자 1 등)
        if self._api_response_indicates_success(result):
            _LOGGER.info(f"{self._attr_name} 명령 전송 성공 (API 응답)")
            await self._update_sensor(f"명령 전송 성공: {self._attr_name}")
            return

        # 2) API에서 즉시 성공 응답이 없을 경우: notification_entity 설정이 있으면 알림을 폴링하여 실제 실행 여부 확인
        if self._notification_entity:
            expected_phrases = self._expected_phrases_for_cmd(self._cmd)
            if expected_phrases:
                ok = await self._wait_for_notification(expected_phrases, timeout=20)
                if ok:
                    _LOGGER.info(f"{self._attr_name} 명령 실행 성공 (notification 확인)")
                    await self._update_sensor(f"명령 실행 성공: {self._attr_name}")
                    return
                # 알림 미수신 -> timeout 처리
                _LOGGER.warning(f"{self._attr_name} 알림 미수신 (notification timeout)")
                await self._update_sensor(f"timeout: {self._attr_name}")
                return

        # 3) notification_entity 미설정 또는 기대문구 없음 -> timeout 처리
        _LOGGER.warning(f"{self._attr_name} 명확한 성공 응답 없음 및 notification 미설정 -> timeout")
        await self._update_sensor(f"timeout: {self._attr_name}")

    def _api_response_indicates_success(self, response_text: str) -> bool:
        """API는 명령 전송의 성공/실패만 반환하므로 다음 케이스만 성공으로 간주:
           - 정확한 문자열 "1"
           - JSON 숫자 1 또는 JSON 객체에서 success/result/status 키가 1/"1"/True
        """
        txt = (response_text or "").strip()
        # 정확히 "1"인 경우 성공
        if txt == "1":
            return True

        # JSON 형태 검사
        try:
            data = json.loads(response_text)
            # 응답이 단순 숫자 1인 경우
            if data == 1:
                return True
            # 응답이 dict인 경우 특정 키 검사
            if isinstance(data, dict):
                for key in ("success", "result", "status"):
                    if key in data:
                        val = data.get(key)
                        # 정수 1, 문자열 "1", 또는 True 를 성공으로 간주
                        if val == 1 or str(val) == "1" or val is True:
                            return True
        except Exception:
            pass
        return False

    def _expected_phrases_for_cmd(self, cmd: str):
        """명령별로 notification에서 기대하는 문구 목록 반환(한국어/영문 포함)."""
        # 한국어 문구 우선, 소문자 비교에 대비한 영문/한국어 혼합
        mapping = {
            "WINDOW_OPEN": ["창문이 열렸습니다", "윈도우가 열렸습니다", "window opened"],
            "WINDOW_CLOSE": ["창문이 닫혔습니다", "윈도우가 닫혔습니다", "window closed"],
            "DOOR_OPEN": ["도어가 열렸습니다", "door unlocked"],
            "DOOR_LOCK": ["도어가 잠겼습니다", "door locked"],
            "SUNROOF_OPEN": ["썬루프가 열렸습니다", "sunroof opened"],
            "SUNROOF_TILT": ["썬루프가 틸트 되었습니다", "sunroof tilted"],
            "SUNROOF_CLOSE": ["썬루프가 닫혔습니다", "sunroof closed"],
            "VEHICLE_START": ["시동이 걸렸습니다", "engine started", "vehicle started"],
            "VEHICLE_STOP": ["시동이 OFF되었습니다", "engine off", "vehicle stopped"]
        }
        return mapping.get(cmd, [])

    async def _wait_for_notification(self, expected_phrases, timeout=20):
        """notification_entity 상태를 폴링하여 expected_phrases가 포함되는지 확인."""
        ent = self._notification_entity
        if not ent:
            return False
        interval = 1.0
        elapsed = 0.0
        while elapsed < timeout:
            state_obj = self._hass.states.get(ent)
            if state_obj and state_obj.state:
                txt = str(state_obj.state).lower()
                for phrase in expected_phrases:
                    if phrase.lower() in txt:
                        return True
            await asyncio.sleep(interval)
            elapsed += interval
        return False

    async def _parse_response(self, response: str) -> bool:
        """이 함수는 기존 코드와 호환성을 위해 유지(사용 안됨 가능)."""
        try:
            data = json.loads(response)
            return data.get("result") == "success" or data.get("status") == "ok"
        except (json.JSONDecodeError, ValueError):
            return "success" in (response or "").lower() or "ok" in (response or "").lower()

    async def _update_sensor(self, msg):
        """Update last action sensor."""
        sensor = self._hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {}).get("last_action_sensor")
        if sensor:
            await sensor.async_update_state(msg)
        else:
            _LOGGER.warning(f"센서를 찾을 수 없음: {self._entry.entry_id}")

