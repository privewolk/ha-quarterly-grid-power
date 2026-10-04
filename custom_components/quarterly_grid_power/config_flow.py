from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import CONF_POWER_ENTITY, DOMAIN


class QuarterlyGridPowerConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle the integration setup flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step."""
        if user_input is not None:
            power_entity = user_input[CONF_POWER_ENTITY]

            await self.async_set_unique_id(
                f"quarterly_grid_power_{power_entity}"
            )
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="Quarterly Grid Power",
                data={
                    CONF_POWER_ENTITY: power_entity,
                },
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_POWER_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        device_class="power",
                        multiple=False,
                    )
                )
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
        )