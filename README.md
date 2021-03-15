[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

# HA-Emulated-Color-Temp-Light
Home Assistant component for emulating SUPPORT_COLOR_TEMP for color lights that doesn't support color temp (like some Ikea Tradfri bulbs).

This is basically copy of HA core light group entity, but with support for only one light entity and forced SUPPORT_COLOR_TEMP feature.

![image](https://user-images.githubusercontent.com/20594810/111164606-82c1d480-859e-11eb-87a8-f1af0a7c2a2f.png)


# Installation and configuration
1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `emulated_color_temp`.
4. Download _all_ the files from the `custom_components/emulated_color_temp/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Add this to your `configuration.yaml` (edit `name` to your desired entity name and `entity_id` to your original light entity id without color temperature support):
```
light:
  - platform: emulated_color_temp
    name: Your new light name
    entity_id: light.original_light_entity
```
7. Restart Home Assistant

