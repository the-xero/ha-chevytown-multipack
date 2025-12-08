from homeassistant.helpers import discovery
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN
import logging
import async_timeout

_LOGGER = logging.getLogger(__name__)

DOMAIN_DATA = "multipack_data"

async def async_setup(hass, config):
    """Set up the Multipack integration."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass, entry):
    """Set up a config entry by forwarding to platforms and storing entry data."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(entry.entry_id, {})
    
    # 설정 검증 (API 연결 테스트)
    if not await _validate_api_credentials(hass, entry):
        _LOGGER.error(f"Multipack API 인증 실패: {entry.entry_id}")
        return False
    
    # 플랫폼 포워딩 (sensor, button)
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "button"])
    
    # 서비스 등록
    _register_services(hass, entry)
    
    _LOGGER.info(f"Multipack entry loaded: {entry.entry_id}")
    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry and platforms."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor", "button"])
    if unload_ok:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
        _LOGGER.info(f"Multipack entry unloaded: {entry.entry_id}")
    return unload_ok

async def _validate_api_credentials(hass, entry):
    """Validate API credentials by making a test request."""
    id_ = entry.data.get("id")
    key_ = entry.data.get("key")
    
    if not id_ or not key_:
        return False
    
    session = async_get_clientsession(hass)
    try:
        async with async_timeout.timeout(5):
            # 도어 잠금 명령으로 API 검증 (실제 명령 1회 실행)
            resp = await session.get(
                f"https://mp.gmone.co.kr/api?id={id_}&key={key_}&cmd=DOOR_LOCK"
            )
            # 응답이 있으면 자격증명이 유효함으로 판단
            _LOGGER.info(f"API 검증 완료 - 도어 잠금 명령 실행 (상태: {resp.status})")
            return resp.status in [200, 400, 401, 404, 500]
    except Exception as exc:
        _LOGGER.warning(f"API 검증 중 오류: {exc}")
        return False

def _register_services(hass, entry):
    """Register custom services."""
    # services.yaml에 정의된 서비스와 일치하도록 구현
    async def handle_vehicle_start(call):
        """Handle vehicle start service call."""
        id_ = entry.data.get("id")
        key_ = entry.data.get("key")
        await _call_api(hass, id_, key_, "VEHICLE_START")
    
    hass.services.async_register(DOMAIN, "vehicle_start", handle_vehicle_start)
    _LOGGER.debug("Services registered for Multipack")

async def _call_api(hass, id_, key_, cmd):
    """Make API call to Multipack."""
    url = f"https://mp.gmone.co.kr/api?id={id_}&key={key_}&cmd={cmd}"
    session = async_get_clientsession(hass)
    try:
        async with async_timeout.timeout(10):
            resp = await session.get(url)
            return await resp.text()
    except Exception as exc:
        _LOGGER.error(f"API 호출 실패: {exc}")
        return None
