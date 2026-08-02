# Somfy Protexial / Protexiom / Protexial IO

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)
[![Maintainers](https://img.shields.io/badge/maintainers-@AuroreVgn%20|%20@the8tre-blue.svg?style=flat-square)](#)

![header](assets/header.png)

## Other languages

[English](README.en.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Italiano](README.it.md) | [Nederlands](README.nl.md) | [Português](README.pt.md)

## About

🔀 This 2.0.x version is an **updated fork** of the original integration by [the8tre](https://github.com/the8tre), available [here](https://github.com/the8tre/somfy-protexial).

The main objectives of this integration are to anticipate:

- the **shutdown of the 2G network** by providing a reliable alternative without having to replace the entire alarm system, allowing intrusion (or any other) alerts to be sent directly through Home Assistant and the smartphone application, including critical notifications (i.e. notifications that bypass silent mode).
- the [**shutdown of the Somfy Protexial/Protexiom servers**](https://forum.hacf.fr/t/integration-custom-centrale-somfy-protexial/23589/223) (although the impact is expected to be very limited).

This integration provides an interface with Somfy Protexial, Protexiom and Protexial IO alarm control panels.

Tested models:

| Model | Version | Status |
| -------------- | --------------- | ------------------ |
| Protexial IO | `2013 (v10_13)` | :white_check_mark: |
| Protexiom 5000 | `2013 (v10_3)` | :white_check_mark: |
| Protexial | `2013 (v10_13)` | :white_check_mark: |
| Protexial | `2013 (v10_14)` | :white_check_mark: |
| Protexial | `2013 (v10_15)` | :white_check_mark: |
| Protexial | `2010 (v7_9)` | :white_check_mark: |
| Protexial | `2010 (v8_1)` | :white_check_mark: |
| Protexial | `2008` | :white_check_mark: |

⚠️ If your model is not listed here, it does **not** necessarily mean that it is unsupported. It may simply not have been tested yet or reported by users.

🔎 The integration provides real-time monitoring of the alarm system and its devices.

👉🏻 The integration allows you to control:

- 🚨 the alarm by zones (A, B, C)
- 🪟 roller shutters
- 💡 lights

🔃 The integration also supports resetting alarm, radio link and battery faults.

#### The following entities are supported:

| Entity | Description | Version |
| ----------------------------------- | ----------------------------------------------------------- |-----------------------------------------------------------|
| `alarm_control_panel.alarme` | Supports `armed_away`, `armed_home`, `armed_night` modes | 1.2.4 |
| `cover.volets` | Open, close and stop. Position control is not supported | 1.2.4 |
| `light.lumieres` | On/Off (state maintained by the integration. It cannot detect whether the lights were switched using another method such as a remote control, wall switch or another integration.) | 1.2.4 |
| `binary_sensor.batterie` | Aggregated battery status | 1.2.4 |
| `binary_sensor.boitier` | Control panel status | 1.2.4 |
| `binary_sensor.communication_radio` | Radio communication status | 1.2.4 |
| `binary_sensor.communication_gsm` | GSM communication status | 1.2.4 |
| `binary_sensor.mouvement_detecte` | Motion detection status | 1.2.4 |
| `binary_sensor.porte_ou_fenetre` | Door or window status | 1.2.4 |
| `binary_sensor.camera` | Camera connection status | 1.2.4 |
| `sensor.signal_gsm_5` | GSM signal strength (/5) | 1.2.6 |
| `sensor.operateur_gsma` | GSM operator | 1.2.6 |
| `sensor.alarme_derniere_sync` | Last synchronization with the alarm panel | 2.0.7 |

#### The following binary sensors are created to represent every alarm device and expose their attributes:

| Entity | Description - Attributes | Version |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------- | --------|
| `binary_sensor.do_ouvt_xxx` | Door contact - Attributes: battery, panel communication, fault, tamper, open/closed, paused | 2.0.0 |
| `binary_sensor.do_vitre_ouvt_xxx` | Window contact with glass-break detection - Attributes: battery, panel communication, fault, tamper, open/closed, paused | 2.0.0 |
| `binary_sensor.do_vitre_ouvt_xxx` | Acoustic glass-break detector - Attributes: battery, panel communication, fault, tamper, open/closed, paused | 2.0.0 |
| `binary_sensor.do_gar_xxx` | Garage door contact - Attributes: battery, panel communication, fault, tamper, open/closed, paused | 2.0.0 |
| `binary_sensor.dm_image_mvt_xxx` | Motion detector with image capture - Attributes: battery, panel communication, fault, tamper, paused | 2.0.0 |
| `binary_sensor.dm_mvt_xxx` | Motion detector - Attributes: battery, panel communication, fault, tamper, paused | 2.0.0 |
| `binary_sensor.tr_tel_xxx` | Alarm control panel - Attributes: battery, panel communication, fault, tamper, paused | 2.0.0 |
| `binary_sensor.clavier_clv_xxx` | Keypad - Attributes: battery, panel communication, fault, tamper, paused | 2.0.0 |
| `binary_sensor.cl_lcd_clv_xxx` | LCD keypad - Attributes: battery, panel communication, fault, tamper, paused | 2.0.0 |
| `binary_sensor.sir_ext_xxx` | Outdoor siren - Attributes: battery, panel communication, fault, tamper, paused | 2.0.0 |
| `binary_sensor.sir_int_xxx` | Indoor siren - Attributes: battery, panel communication, fault, tamper, paused | 2.0.0 |
| `binary_sensor.d_fumee_fumee_xxx` | Smoke detector - Attributes: battery, panel communication, fault, paused | 2.0.0 |
| `binary_sensor.tc_multi_tlcmd_xxx` | Multi-channel remote control - Attributes: panel communication, paused | 2.0.0 |
| `binary_sensor.tc_4_tlcmd_xxx` | Multi-zone alarm remote control - Attributes: panel communication, paused | 2.0.0 |
| `binary_sensor.badge_bdg_axxx` | RFID badge - Attributes: panel communication, paused | 2.0.0 |

Attributes are available in the **Details** panel.

<img width="160" height="243" alt="image" src="https://github.com/user-attachments/assets/1fd0de09-5f3e-4dc0-b147-bb55593adf45" />

<img width="526" height="301" alt="image" src="https://github.com/user-attachments/assets/50ad793d-bddc-44b5-915a-b569b7cb5050" />

#### The following buttons are supported:

| Entity | Description | Version |
| ----------------------------------- | ----------------------------------------------------------- |-----------------------------------------------------------|
| `button.reinitialiser_defaut_alarme` | Reset alarm faults (motion, intrusion, tamper) | 2.0.7 |
| `button.reinitialiser_defaut_liaison_radio` | Reset radio communication faults between the control panel and sensors | 2.0.7 |
| `button.reinitialiser_defaut_piles` | Reset battery faults | 2.0.7 |

## Installation

### Option A: Install via HACS (Recommended)

1. Add this GitHub repository to HACS
   - Automatically: [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=integration&repository=somfy-protexial&owner=AuroreVgn) <br />
   - Manually:
      - HACS → Integrations → '...' menu → Custom repositories
      - Repository: `https://github.com/AuroreVgn/somfy-protexial`
      - Category: `Integration`
3. Download the integration
   - HACS → Integrations → Somfy Protexial → Download
4. Restart Home Assistant

### Option B: Manual installation

1. Download the latest release archive: [somfy_protexial.zip](https://github.com/AuroreVgn/somfy-protexial/archive/refs/tags/2.0.11.zip)
2. Locate the directory containing your Home Assistant `configuration.yaml` file.
3. If the `custom_components` directory does not exist, create it.
4. Create a `somfy_protexial` directory inside `custom_components`.
5. Extract the contents of `somfy_protexial.zip` into the `somfy_protexial` directory.
6. Restart Home Assistant.

## Configuration

- Add the integration using [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=somfy_protexial) or manually.
- Settings → Devices & Services → + Add Integration → Somfy Protexial

### 1. Alarm control panel address

- Enter the URL of your alarm panel's local web interface:
  `http://192.168.1.234` or `http://192.168.1.234:9876`

</br>

<img src="assets/welcome.png" width="50%"><img src="assets/login_io.jpeg" width="50%">

### 2. User credentials

- Username: `"u"` (**keep the pre-filled value**)
- Password: Enter your usual password.
- Authentication code: Enter the code from your authentication card corresponding to the requested challenge.

<img src="assets/step2.png" width="50%">

### 3. Additional configuration

The available arming modes are based on the zones configured in your Somfy alarm control panel:

- Away mode (always configured): Zones A+B+C
- Night mode (optional): Any combination of A, B, C, A+B, B+C or A+C
- Home mode (optional): Any combination of A, B, C, A+B, B+C or A+C

**Arm/Disarm Code:**  
If you specify a code, it will be required whenever the alarm is armed or disarmed.

**Refresh interval:**  
From **15 seconds** to **1 hour**. The default value is **60 seconds**.

Using a shorter interval is not recommended, as it may cause the alarm's web interface to become unstable.

<img src="assets/step3.png" width="50%">

## Notes

### Home Assistant Lovelace Card (Status & Control)

A dedicated Lovelace [card](https://github.com/developpeurbox/somfy-protexial-card) has been developed specifically for this integration.

### Mushroom Template Card (Per-device details)

A Home Assistant template to display each alarm device and its attributes (battery, communication, etc.) is available [here](https://github.com/AuroreVgn/somfy-protexial/blob/main/assets/Template%20Home%20Assistant).

<img width="485" height="127" alt="image" src="https://github.com/user-attachments/assets/d4f385c0-0171-4968-b369-c4cb86d8409e" />

### Version compatibility

The compatibility list shown at the top of this page is **not exhaustive**. This integration may work with additional versions of Somfy alarm panels. Feel free to let me know if you've successfully tested another version!

The model year of your alarm web interface is displayed at the bottom of the pages:

<img src="assets/version.png" width="30%">

Some alarm panels also expose their firmware version through:

*http://192.168.1.234/cfg/vers*

or

*http://192.168.1.234:9876/cfg/vers*

### Using the original web interface

⚠️ **The alarm control panel only supports one active user session at a time. If you want to use the original web interface, you must temporarily disable this integration.**

### Using the original mobile application

⚠️ The official **Somfy Alarme** mobile application can still be used while this integration is active.

### Reconfiguring the integration

The integration fully supports reconfiguration directly from the Home Assistant graphical interface.

## Contributions are welcome!

If you'd like to contribute, please read the [Contribution guidelines](CONTRIBUTING.md).

## Credits

This integration is largely based on the work of [@Ludeeus](https://github.com/ludeeus) and the [integration_blueprint][integration_blueprint].

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square
[license-shield]: https://img.shields.io/github/license/the8tre/somfy-protexial.svg?style=flat-square
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40the8tre-blue.svg?style=flat-square
[releases-shield]: https://img.shields.io/github/v/release/AuroreVgn/somfy-protexial.svg?style=flat-square
[releases]: https://github.com/AuroreVgn/somfy-protexial/releases
[user_profile]: https://github.com/AuroreVgn
