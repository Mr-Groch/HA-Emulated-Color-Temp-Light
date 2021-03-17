"""Platform for light integration."""
import asyncio
from typing import List, Optional, Tuple

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
# Import the device class from the component that you want to support
from homeassistant.components import light
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP,
    ATTR_EFFECT,
    ATTR_EFFECT_LIST,
    ATTR_FLASH,
    ATTR_HS_COLOR,
    ATTR_MAX_MIREDS,
    ATTR_MIN_MIREDS,
    ATTR_TRANSITION,
    ATTR_WHITE_VALUE,
    PLATFORM_SCHEMA,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    SUPPORT_COLOR_TEMP,
    SUPPORT_EFFECT,
    SUPPORT_FLASH,
    SUPPORT_TRANSITION,
    SUPPORT_WHITE_VALUE,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_SUPPORTED_FEATURES,
    CONF_ENTITY_ID,
    CONF_NAME,
    CONF_OFFSET,
    EVENT_HOMEASSISTANT_START,
    STATE_ON,
    STATE_UNAVAILABLE,
)
from homeassistant.core import CoreState, State
from homeassistant.util import color as color_util
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.typing import ConfigType, HomeAssistantType


# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ENTITY_ID): cv.entity_domain(light.DOMAIN),
    vol.Required(CONF_NAME): cv.string,
    vol.Optional(CONF_OFFSET, default=0): vol.All(
            vol.Coerce(int), vol.Range(min=-129, max=500)
        ),
})


async def async_setup_platform(
    hass: HomeAssistantType, config: ConfigType, async_add_entities, discovery_info=None
) -> None:
    """Set up the Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    light_entity = config[CONF_ENTITY_ID]
    name = config[CONF_NAME]
    offset = config[CONF_OFFSET]

    # Add devices
    async_add_entities([EmulatedColorTempLight(light_entity, name, offset)])


class EmulatedColorTempLight(light.LightEntity):
    """Representation of Light."""

    def __init__(self, light_entity, name, offset):
        """Initialize Light."""
        self._light = light_entity
        self._name = name
        self._offset = offset
        self._is_on = False
        self._available = False
        self._brightness: Optional[int] = None
        self._hs_color: Optional[Tuple[float, float]] = None
        self._color_temp: Optional[int] = None
        self._min_mireds: int = 154
        self._max_mireds: int = 500
        self._white_value: Optional[int] = None
        self._effect_list: Optional[List[str]] = None
        self._effect: Optional[str] = None
        self._supported_features: int = 0

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""

        async def async_state_changed_listener(event):
            """Handle child updates."""
            self.async_set_context(event.context)
            await self.async_defer_or_update_ha_state()

        assert self.hass
        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [self._light], async_state_changed_listener
            )
        )

        if self.hass.state == CoreState.running:
            await self.async_update()
            return

        """Register listeners."""
        async def _update_at_start(_):
            await self.async_update()
            self.async_write_ha_state()

        self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, _update_at_start)

    async def async_defer_or_update_ha_state(self) -> None:
        """Only update once at start."""
        assert self.hass is not None

        if self.hass.state != CoreState.running:
            return

        await self.async_update()
        self.async_write_ha_state()

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name
        
    @property
    def is_on(self) -> bool:
        """Return the on/off state of the light group."""
        return self._is_on
    
    @property
    def available(self) -> bool:
        """Return whether the light group is available."""
        return self._available

    @property
    def brightness(self) -> Optional[int]:
        """Return the brightness of this light between 0..255."""
        return self._brightness

    @property
    def hs_color(self) -> Optional[Tuple[float, float]]:
        """Return the hue and saturation color value [float, float]."""
        return self._hs_color
        
    @property
    def color_temp(self) -> Optional[int]:
        """Return the CT color value in mireds."""
        return self._color_temp

    @property
    def min_mireds(self) -> int:
        """Return the coldest color_temp that this light group supports."""
        return self._min_mireds

    @property
    def max_mireds(self) -> int:
        """Return the warmest color_temp that this light group supports."""
        return self._max_mireds
        
    @property
    def white_value(self) -> Optional[int]:
        """Return the white value of this light group between 0..255."""
        return self._white_value
        
    @property
    def effect_list(self) -> Optional[List[str]]:
        """Return the list of supported effects."""
        return self._effect_list
        
    @property
    def effect(self) -> Optional[str]:
        """Return the current effect."""
        return self._effect
        
    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return self._supported_features
        
    @property
    def should_poll(self) -> bool:
        """No polling needed"""
        return False
        
    @property
    def extra_state_attributes(self):
        """Return the state attributes for the light group."""
        return {ATTR_ENTITY_ID: self._light}

    async def async_turn_on(self, **kwargs):
        """Forward the turn_on command to light"""
        data = {ATTR_ENTITY_ID: self._light}
        
        emulate_color_temp = False

        if ATTR_BRIGHTNESS in kwargs:
            data[ATTR_BRIGHTNESS] = kwargs[ATTR_BRIGHTNESS]

        if ATTR_HS_COLOR in kwargs:
            data[ATTR_HS_COLOR] = kwargs[ATTR_HS_COLOR]

        if ATTR_COLOR_TEMP in kwargs:
            data[ATTR_COLOR_TEMP] = kwargs[ATTR_COLOR_TEMP]

            state = self.hass.states.get(self._light)
            support = state.attributes.get(ATTR_SUPPORTED_FEATURES)
            # Only pass color temperature to supported light
            if bool(support & SUPPORT_COLOR) and not bool(
                support & SUPPORT_COLOR_TEMP
            ):
                emulate_color_temp = True
                self._color_temp = data[ATTR_COLOR_TEMP]

        if ATTR_WHITE_VALUE in kwargs:
            data[ATTR_WHITE_VALUE] = kwargs[ATTR_WHITE_VALUE]

        if ATTR_EFFECT in kwargs:
            data[ATTR_EFFECT] = kwargs[ATTR_EFFECT]

        if ATTR_TRANSITION in kwargs:
            data[ATTR_TRANSITION] = kwargs[ATTR_TRANSITION]

        if ATTR_FLASH in kwargs:
            data[ATTR_FLASH] = kwargs[ATTR_FLASH]

        if not emulate_color_temp:
            await self.hass.services.async_call(
                light.DOMAIN,
                light.SERVICE_TURN_ON,
                data,
                blocking=True,
                context=self._context,
            )
            return

        emulate_color_temp_data = data.copy()
        temp_k = color_util.color_temperature_mired_to_kelvin(
            emulate_color_temp_data[ATTR_COLOR_TEMP] + self._offset
        )
        hs_color = color_util.color_temperature_to_hs(temp_k)
        emulate_color_temp_data[ATTR_HS_COLOR] = hs_color
        del emulate_color_temp_data[ATTR_COLOR_TEMP]

        await self.hass.services.async_call(
            light.DOMAIN,
            light.SERVICE_TURN_ON,
            emulate_color_temp_data,
            blocking=True,
            context=self._context,
        )

    async def async_turn_off(self, **kwargs):
        """Forward the turn_off command to light"""
        data = {ATTR_ENTITY_ID: self._light}

        if ATTR_TRANSITION in kwargs:
            data[ATTR_TRANSITION] = kwargs[ATTR_TRANSITION]

        await self.hass.services.async_call(
            light.DOMAIN,
            light.SERVICE_TURN_OFF,
            data,
            blocking=True,
            context=self._context,
        )

    async def async_update(self):
        """Query light and determine the state."""
        state = self.hass.states.get(self._light)

        self._is_on = (state.state == STATE_ON)
        self._available = (state.state != STATE_UNAVAILABLE)

        self._brightness = state.attributes.get(ATTR_BRIGHTNESS)

        self._hs_color = state.attributes.get(ATTR_HS_COLOR)

        self._white_value = state.attributes.get(ATTR_WHITE_VALUE)

        self._color_temp = state.attributes.get(ATTR_COLOR_TEMP, self._color_temp)
        self._min_mireds = state.attributes.get(ATTR_MIN_MIREDS, 154)
        self._max_mireds = state.attributes.get(ATTR_MAX_MIREDS, 500)

        self._effect_list = state.attributes.get(ATTR_EFFECT_LIST)
        self._effect = state.attributes.get(ATTR_EFFECT)
        
        self._supported_features = state.attributes.get(ATTR_SUPPORTED_FEATURES)
        # Bitwise-or the supported features with the color temp feature
        self._supported_features |= SUPPORT_COLOR_TEMP
