# Somfy Protexial / Protexiom / Protexial IO

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)
[![Project Maintenance][maintenance-shield]][user_profile]

![header](assets/header.png)

## À propos

Cette intégration gère l'interface avec une centrale d'alarme Somfy Protexial, Protexiom ou Protexial IO

Modèles testés:
| Modèle         | Version         | Statut             |
| -------------- | --------------- | ------------------ |
| Protexial IO   | `2013 (v10_13)` | :white_check_mark: |
| Protexiom 5000 | `2013 (v10_3)`  | :white_check_mark: |
| Protexial      | `2010 (v8_1)`   | :white_check_mark: |
| Protexiom      | `2008`          | :white_check_mark: |

L'intégration permet le pilotage:

- de l'alarme par zones (A, B, C)
- des volets roulants
- des lumières

Les entités suivantes sont gérées:
| Entité                              | Description                                                 |
| ----------------------------------- | ----------------------------------------------------------- |
| `alarm_control_panel.alarme`        | Support des modes `armed_away`, `armed_home`, `armed_night` |
| `cover.volets`                      | Ouverture, fermeture et arrêt. Pas de contrôle de position. |
| `light.lumieres`                    | Allumé ou éteint (état maintenu par l'intégration).         |
| `binary_sensor.batterie`            | Etat aggrégé des batteries des éléments.                    |
| `binary_sensor.boitier`             | Etat du boitier.                                            |
| `binary_sensor.communication_radio` | Etat de la communication radio.                             |
| `binary_sensor.communication_gsm`   | Etat de la communication GSM.                               |
| `binary_sensor.mouvement_detecte`   | Etat de détection de mouvement.                             |
| `binary_sensor.porte_ou_fenetre`    | Etat d'ouvertue de porte ou fenêtre.                        |
| `binary_sensor.camera`              | Etat de connexion de la caméra.                             |


{% if not installed %}

## Installation

- Ajouter l'intégration: [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=somfy_protexial)
  </br>ou manuellement
- Paramètres :arrow_right: Appareils et services :arrow_right: + Ajouter une intégration :arrow_right: Somfy Protexial

{% endif %}

## Configuration

### 1. Adresse de la centrale

- Saisisser l'URL de l'interface web locale de votre centrale: `http://192.168.1.234`
![welcome](assets/welcome.png)  ![login_io](assets/login_io.jpeg)


### 2. Identifiants de l'utilisateur

- Utilisateur: `"u"`, conserver la valeur pré-remplie
- Mot de passe: Saisir le mot de passe habituellement utilisé
- Code: Saisir le code de la carte d'authentification correspondant au challenge demandé
  ![step2](assets/step2.png)

### 3. Configuration additionelle

Les différents modes d'armement exploitent les zones définies par la configuration de la centrale Somfy:

- Armement en absence (toujours configuré): Zones A+B+C
- Armement pour la nuit (optionnel): Zones au choix (A, B, C, A+B, B+C, A+C)
- Armement en présence (optionnel): Zones au choix (A, B, C, A+B, B+C, A+C)

Code d'armement: Si vous spécifiez un code celui-ci sera demandé lors de l'armement/désarmement.

Interval de rafraîchissement: de 15 secondes à 1 heure, 60 secondes par défaut.
![step3](assets/step3.png)

## À noter

### Compatibilité de version

La liste visible en haut de cette page n'est pas exhaustive, il est tout à fait possible que cette intégration soit compatible avec d'autres version de centrale Somfy. N'hésitez pas à m'en faire part si c'est le cas !

Un fil de discussion à ce sujet est disponible ici: [HACF - Intégration Custom: Centrale Somfy Protexial](https://forum.hacf.fr/t/integration-custom-centrale-somfy-protexial/23589/1)

L'année de l'interface de votre centrale apparait en bas des pages:</br>
![version](assets/version.png)

Certaines centrales fournissent leur version via cette url: http://192.168.1.234/cfg/vers

### Utilisation de l'interface web d'origine

La centrale ne gérant qu'une seule session utilisateur à la fois il est nécesaire de désactiver temporairement l'intégration si vous voulez pouvoir utiliser l'interface web.

### Re-configuration de l'intégration
L'intégration supporte la re-configuration à partie de l'interface graphique.

## Les contributions sont les bienvenues !

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square
[license-shield]: https://img.shields.io/github/license/the8tre/somfy-protexial.svg?style=flat-square
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40the8tre-blue.svg?style=flat-square
[releases-shield]: https://img.shields.io/github/release/the8tre/somfy-protexial.svg?style=flat-square
[releases]: https://github.com/the8tre/somfy-protexial/releases
[user_profile]: https://github.com/the8tre
