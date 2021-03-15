# HA-Emulated-Color-Temp-Light
Home Assistant component for emulating SUPPORT_COLOR_TEMP for color lights that doesn't support color temp (like some Ikea Tradfri bulbs).
This is basically copy of HA core light group entity, but with support for only one light entity and forced SUPPORT_COLOR_TEMP feature.

# Installation and configuration
1. Copy emulated_color_temp directory to HA custom_components directory ex. `\config\custom_components\emulated_color_temp`
2. Add to `configuration.yaml`:
```
light:
  - platform: emulated_color_temp
    name: Your new light name
    entity_id: light.original_light_entity
```

