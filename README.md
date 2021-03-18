[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![Community Forum](https://img.shields.io/badge/Community-Forum-41BDF5.svg?style=popout)](https://community.home-assistant.io/t/emulated-color-temp-light/291271)
[![paypalme_badge](https://img.shields.io/badge/Donate-PayPal-0070ba?style=flat)](https://paypal.me/MrGroch)

# HA-Emulated-Color-Temp-Light
Home Assistant component for emulating SUPPORT_COLOR_TEMP for color lights that doesn't support color temp (like some Ikea Tradfri bulbs).

This is basically copy of HA core light group entity, but with support for only one light entity and forced SUPPORT_COLOR_TEMP feature.

![image](https://user-images.githubusercontent.com/20594810/111164606-82c1d480-859e-11eb-87a8-f1af0a7c2a2f.png)


## Installation

### Using [HACS](https://hacs.xyz/) (recommended)

This integration can be added to HACS as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories):
* URL: `https://github.com/Mr-Groch/HA-Emulated-Color-Temp-Light`
* Category: `Integration`

After adding a custom repository you can use HACS to install this integration using user interface.

### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `emulated_color_temp`.
4. Download _all_ the files from the `custom_components/emulated_color_temp/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. [Configure](#Configuration) custom component in `configuration.yaml` file.
7. Restart Home Assistant.

## Configuration

After installation of the custom component, it needs to be configured in `configuration.yaml` file.

Add this to your `configuration.yaml` (this is example config):
```
light:
  - platform: emulated_color_temp
    name: Your new light name
    entity_id: light.original_light_entity
```

Available options:

| Option | Required | Description |
| - | - | - |
| name | Yes | Desired entity name |
| entity_id | Yes | Original light entity id without color temperature support |
| offset | No | Color temperature offset in mireds, can be positive (max: 500) and negative (min: -129). [Ikea Tradfri warm color bulbs](https://www.zigbee2mqtt.io/devices/LED1924G9.html#ikea-led1924g9) need to have about -100 offset. (default: 0) |
