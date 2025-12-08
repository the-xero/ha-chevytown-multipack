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
            id_val = user_input.get("id", "").strip()
            key_val = user_input.get("key", "").strip()
            
            if not id_val:
                errors["base"] = "invalid_id"
            elif not key_val:
                errors["base"] = "invalid_key"
            elif len(id_val) < 3:
                errors["base"] = "invalid_id"
            else:
                return self.async_create_entry(
                    title=f"Multipack ({id_val})",
                    data=user_input
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
