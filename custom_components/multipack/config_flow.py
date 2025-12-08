import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

class MultipackConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # 입력값 검증
            id_val = user_input.get("id", "").strip() if user_input.get("id") else ""
            key_val = user_input.get("key", "").strip() if user_input.get("key") else ""
            
            if not id_val:
                errors["base"] = "invalid_id"
            elif not key_val:
                errors["base"] = "invalid_key"
            elif len(id_val) < 2:
                errors["base"] = "invalid_id"
            else:
                # 기존 항목 확인 (중복 방지)
                await self.async_set_unique_id(id_val)
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=f"Multipack ({id_val})",
                    data={
                        "id": id_val,
                        "key": key_val
                    }
                )

        data_schema = vol.Schema({
            vol.Required("id"): str,
            vol.Required("key"): str
        })
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
