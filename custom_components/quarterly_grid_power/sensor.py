from __future__ import annotations

from datetime import datetime, timedelta
import logging
import math

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_POWER_ENTITY, DOMAIN, SAMPLE_INTERVAL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the quarterly average power sensor."""
    async_add_entities(
        [
            QuarterlyAveragePowerSensor(
                hass=hass,
                entry=entry,
            )
        ]
    )


class QuarterlyAveragePowerSensor(SensorEntity, RestoreEntity):
    """Sensor that calculates average grid power per quarter-hour."""

    _attr_has_entity_name = True
    _attr_name = "Current quarter average"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = "power"
    _attr_state_class = "measurement"

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self.entry = entry
        self._power_entity = entry.data[CONF_POWER_ENTITY]

        self._attr_unique_id = f"{self._power_entity}_quarterly_average"

        self._total = 0.0
        self._sample_count = 0
        self._last_power = 0.0
        self._attr_native_value = 0.0

        self._remove_interval_listener = None

    async def async_added_to_hass(self) -> None:
        """Run when the entity is added to Home Assistant."""
        await super().async_added_to_hass()

        last_state = await self.async_get_last_state()

        if last_state is not None:
            try:
                self._attr_native_value = float(last_state.state)
            except ValueError:
                self._attr_native_value = 0.0

        self._remove_interval_listener = async_track_time_interval(
            self.hass,
            self._async_sample,
            timedelta(seconds=SAMPLE_INTERVAL),
        )

        await self._async_sample(datetime.now())

    async def async_will_remove_from_hass(self) -> None:
        """Run when the entity is removed."""
        if self._remove_interval_listener is not None:
            self._remove_interval_listener()
            self._remove_interval_listener = None

        await super().async_will_remove_from_hass()

    @callback
    async def _async_sample(self, now: datetime) -> None:
        """Read the source entity and update the average."""
        try:
            source_state = self.hass.states.get(self._power_entity)

            _LOGGER.warning(
                "Reading source entity %s; state object=%s",
                self._power_entity,
                source_state,
            )

            if source_state is None:
                _LOGGER.error(
                    "Source entity does not exist: %s",
                    self._power_entity,
                )
                self._attr_available = False
                self.async_write_ha_state()
                return

            power = float(source_state.state)
            power = max(power, 0.0)

            if now.minute % 15 == 0 and now.second < SAMPLE_INTERVAL:
                self._total = self._last_power
                self._sample_count = 1
            else:
                self._total += power
                self._sample_count += 1

            self._last_power = power
            self._attr_native_value = self._total / self._sample_count
            self._attr_available = True

            _LOGGER.warning(
                "Quarterly Grid Power value: %.1f W from %s",
                self._attr_native_value,
                self._power_entity,
            )

            self.async_write_ha_state()

        except Exception:
            _LOGGER.exception("Error while sampling Quarterly Grid Power")
            self._attr_available = False
            self.async_write_ha_state()