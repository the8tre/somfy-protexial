# Somfy Protexial / Protexiom / Protexial IO

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)
[![Maintainers](https://img.shields.io/badge/maintainers-@AuroreVgn%20|%20@the8tre-blue.svg?style=flat-square)](#)

![header](assets/header.png)

## Other languages
[English](README.en.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Italiano](README.it.md) | [Nederlands](README.nl.md) | [Português](README.pt.md)

## À propos

🔀 Cette version 2.0.x est un [Fork](https://github.com/the8tre/somfy-protexial) **mis à jour** de l’intégration originale de [the8tre](https://github.com/the8tre).

Les principaux objectifs de cette intégration sont d'anticiper : 
- l'**arrêt de la 2G** en proposant une alternative fiable sans devoir tout changer pour alerter d'une intrusion (ou autre) directement via Home Assistant et l'application smartphone permettant la mise en place d'alertes critiques (ie. qui notifient même en silencieux).
- [l'**arrêt des serveurs Somfy Protexial/Protexiom**](https://forum.hacf.fr/t/integration-custom-centrale-somfy-protexial/23589/223) (même si l'impact est à priori très limité).

Cette intégration gère l'interface avec une centrale d'alarme Somfy Protexial, Protexiom ou Protexial IO.

Modèles testés :
| Modèle         | Version         | Statut             |
| -------------- | --------------- | ------------------ |
| Protexial IO   | `2013 (v10_13)` | :white_check_mark: |
| Protexiom 5000 | `2013 (v10_3)`  | :white_check_mark: |
| Protexial      | `2013 (v10_13)` | :white_check_mark: |
| Protexial      | `2013 (v10_14)` | :white_check_mark: |
| Protexial      | `2013 (v10_15)` | :white_check_mark: |
| Protexial      | `2010 (v7_9)`   | :white_check_mark: |
| Protexial      | `2010 (v8_1)`   | :white_check_mark: |
| Protexial      | `2008`          | :white_check_mark: |

⚠️ Un modèle non présent ici ne signifie pas que cela ne fonctionnera pas, juste qu'il n'a pas été testé ou ajouté faute de retours.

🔎 L'intégration permet la visualisation de l'état de l'alarme et de ces éléments.

👉🏻 L'intégration permet le pilotage :

- 🚨 de l'alarme par zones (A, B, C)
- 🪟 des volets roulants
- 💡des lumières

🔃 L'intégration permet également la réinitialisation des défauts (alarmes, liaisons et piles).

#### Les entités suivantes sont gérées :
| Entité                              | Description                                                 | Version                                                    |
| ----------------------------------- | ----------------------------------------------------------- |-----------------------------------------------------------|
| `alarm_control_panel.alarme`        | Support des modes `armed_away`, `armed_home`, `armed_night` | 1.2.4                                                     |
| `cover.volets`                      | Ouverture, fermeture et arrêt. Pas de contrôle de position  | 1.2.4                                                      |
| `light.lumieres`                    | Allumé ou éteint (état maintenu par l'intégration : ne permet pas de savoir si les lumières ont été allumées/éteintes avec un autre moyen (télécommande, bouton, autre intégration))          | 1.2.4                                                      |
| `binary_sensor.batterie`            | État aggrégé des batteries des éléments                     | 1.2.4                                                      |
| `binary_sensor.boitier`             | État du boîtier                                             | 1.2.4                                                      |
| `binary_sensor.communication_radio` | État de la communication radio.                             | 1.2.4                                                      |
| `binary_sensor.communication_gsm`   | État de la communication GSM                                | 1.2.4                                                      |
| `binary_sensor.mouvement_detecte`   | État de détection de mouvement                              | 1.2.4                                                      |
| `binary_sensor.porte_ou_fenetre`    | État d'ouvertue de porte ou fenêtre                         | 1.2.4                                                      |
| `binary_sensor.camera`              | État de connexion de la caméra                              | 1.2.4                                                      |
| `sensor.signal_gsm_5`               | Puissance du signal GSM (/5)                                | 1.2.6                                                      |
| `sensor.operateur_gsma`             | Opérateur GSM                                               | 1.2.6                                                      |
| `sensor.alarme_derniere_sync`       | Denière synchronisation avec l'alarme                       | 2.0.7                                                      |

#### Les entités (sensors) suivants sont créées avec des attributs (attributes) et représente la liste des éléments de l'alarme :
| Entité                              | Description -  Attributs                                                                                 | Version |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------- | --------|
| `binary_sensor.do_ouvt_xxx`         | Ouverture de porte - Attributs batterie, lien avec la centrale, erreur, arrachement, ouvert/fermé, pause | 2.0.0   |
| `binary_sensor.do_vitre_ouvt_xxx`   | Ouverture de fenêtre avec détection de bris de vitre - Attributs batterie, lien avec la centrale, erreur, arrachement, ouvert/fermé, pause                    | 2.0.0   |
| `binary_sensor.do_vitre_ouvt_xxx`   | Détecteur audiosonique de bris de vitres - Attributs batterie, lien avec la centrale, erreur, arrachement, ouvert/fermé, pause                    | 2.0.0   |
| `binary_sensor.do_gar_xxx`          | Ouverture de porte de garage - Attributs batterie, lien avec la centrale, erreur, arrachement, ouvert/fermé, pause                    | 2.0.0   |
| `binary_sensor.dm_image_mvt_xxx`    | Détecteur de mouvements avec prise d'images - Attributs batterie, lien avec la centrale, erreur, arrachement, pause               | 2.0.0   |
| `binary_sensor.dm_mvt_xxx`          | Détecteur de mouvements - Attributs batterie, lien avec la centrale, erreur, arrachement, pause               | 2.0.0   |
| `binary_sensor.tr_tel_xxx`          | Centrale - Attributs batterie, lien avec la centrale, erreur, arrachement, pause               | 2.0.0   |
| `binary_sensor.clavier_clv_xxx`     | Clavier - Attributs batterie, lien avec la centrale, erreur, arrachement, pause               | 2.0.0   |
| `binary_sensor.cl_lcd_clv_xxx`      | Clavier avec écran LCD - Attributs batterie, lien avec la centrale, erreur, arrachement, pause               | 2.0.0   |  
| `binary_sensor.sir_ext_xxx`         | Sirène extérieure - Attributs batterie, lien avec la centrale, erreur, arrachement, pause               | 2.0.0   |  
| `binary_sensor.sir_int_xxx`         | Sirène intérieure - Attributs batterie, lien avec la centrale, erreur, arrachement, pause               | 2.0.0   |  
| `binary_sensor.d_fumee_fumee_xxx`   | Détecteur de fumée - Attributs batterie, lien avec la centrale, erreur, pause                            | 2.0.0   |  
| `binary_sensor.tc_multi_tlcmd_xxx`  | Télécommande multi canaux - Attributs lien avec la centrale, pause                                              | 2.0.0   |
| `binary_sensor.tc_4_tlcmd_xxx`      | Télécommande alarme multi zones - Attributs lien avec la centrale, pause                                              | 2.0.0   |
| `binary_sensor.badge_bdg_axxx`   | Badge - Attributs lien avec la centrale, pause                                              | 2.0.0   |

Les attributs sont visibles dans le menus "Détails"

<img width="160" height="243" alt="image" src="https://github.com/user-attachments/assets/1fd0de09-5f3e-4dc0-b147-bb55593adf45" />


<img width="526" height="301" alt="image" src="https://github.com/user-attachments/assets/50ad793d-bddc-44b5-915a-b569b7cb5050" />


#### Les boutons suivants sont gérés :
| Entité                              | Description                                                 | Version                                                    |
| ----------------------------------- | ----------------------------------------------------------- |-----------------------------------------------------------|
| `button.reinitialiser_defaut_alarme`|  Réinitialisation des défauts d'alarmes (mouvement, ouverture, arrachement)  | 2.0.7                                                     |
| `button.reinitialiser_defaut_liaison_radio`| Réinitialisation des défauts de lien entre la centrale et les capteurs  | 2.0.7                                                      |
| `button.reinitialiser_defaut_piles`| Réinitialisation des défauts piles    | 2.0.7                                                      

## Installation

### Option A : Installation via HACS (recommandé)

1. Ajouter ce repository GitHub à HACS
   - automatiquement [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=integration&repository=somfy-protexial&owner=AuroreVgn) <br />
   - manuellement
      - HACS :arrow_right: Intégrations :arrow_right: Menu '...' :arrow_right: Dépôts personnalisés
      - Dépôt: `https://github.com/AuroreVgn/somfy-protexial`
      - Catégorie: `Intégration`
3. Télécharger l'intégration
   - HACS :arrow_right: Intégrations :arrow_right: Somfy Protexial :arrow_right: Télécharger
4. Redémarrer Home Assistant

### Option B : Installation manuelle

1. Télécharger l'archive de la dernière version disponible: [somfy_protexial.zip](https://github.com/AuroreVgn/somfy-protexial/archive/refs/tags/2.0.11.zip)
2. Localiser le répertoire contenant le fichier `configuration.yaml` dans votre installation de HA
3. Si il n'y a pas de répertoire `custom_components` le créer
4. Créer un répertoire `somfy_protexial` dans `custom_components`
5. Extraire le contenu de `somfy_protexial.zip` dans le répertoire `somfy_protexial`
6. Redémarrer Home Assistant

## Configuration

- Ajouter l'intégration [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=somfy_protexial) ou manuellement
- Paramètres :arrow_right: Appareils et services :arrow_right: + Ajouter une intégration :arrow_right: Somfy Protexial

### 1. Adresse de la centrale

- Saisisser l'URL de l'interface web locale de votre centrale: `http://192.168.1.234` ou `http://192.168.1.234:9876`
  </br>
  <img src="assets/welcome.png"  width="50%"><img src="assets/login_io.jpeg"  width="50%">

### 2. Identifiants de l'utilisateur

- Utilisateur : `"u"`, **conserver la valeur pré-remplie**
- Mot de passe : Saisir le mot de passe habituellement utilisé
- Code : Saisir le code de la carte d'authentification correspondant au challenge demandé
  <img src="assets/step2.png"  width="50%">

### 3. Configuration additionelle

Les différents modes d'armement exploitent les zones définies par la configuration de la centrale Somfy:

- Armement en absence (toujours configuré) : zones A+B+C
- Armement pour la nuit (optionnel) : zones au choix (A, B, C, A+B, B+C, A+C)
- Armement en présence (optionnel) : zones au choix (A, B, C, A+B, B+C, A+C)

Code d'armement : si vous spécifiez un code celui-ci sera demandé lors de l'armement/désarmement.

Interval de rafraîchissement : de 15 secondes à 1 heure, 60 secondes par défaut (il n'est pas conseillé de mettre moins, sinon l'interface web de l'alarme a tendance à planter).

<img src="assets/step3.png"  width="50%">

## À noter

### Carte Lovelace pour Home Assistant (statut et pilotage)

Une [carte](https://github.com/developpeurbox/somfy-protexial-card) a été développé spécialement pour cette intégration.

### Carte Mushroom Template (détails par éléments)

Un template pour créer chaque éléments avec leur attributs (piles, liaison, ...) est disponible [ici](https://github.com/AuroreVgn/somfy-protexial/blob/main/assets/Template%20Home%20Assistant).

<img width="485" height="127" alt="image" src="https://github.com/user-attachments/assets/d4f385c0-0171-4968-b369-c4cb86d8409e" />

### Carte Lovelace pour Home Assistant uniquement pour la batterie et la détection d'ouverture

Une version simplifiée de la carte permettant de suivre uniquement l'ouverture et la batterie d'un détecteur est disponible [ici](https://forum.hacf.fr/t/integration-custom-centrale-somfy-protexial/23589/295).

### Problématique de sur-consommation de piles pour la centrale
Une solution a été proposé [ici](https://forum.hacf.fr/t/integration-custom-centrale-somfy-protexial/23589/188) et [là](https://forum.hacf.fr/t/integration-custom-centrale-somfy-protexial/23589/191).

### Compatibilité de version

La liste visible en haut de cette page n'est pas exhaustive, il est tout à fait possible que cette intégration soit compatible avec d'autres versions de la centrale Somfy. N'hésitez pas à m'en faire part si c'est le cas !

👉🏻Un fil de discussion à ce sujet est disponible ici: [HACF - Intégration Custom: Centrale Somfy Protexial](https://forum.hacf.fr/t/integration-custom-centrale-somfy-protexial/23589/1)

L'année de l'interface de votre centrale apparait en bas des pages:</br>
<img src="assets/version.png"  width="30%">

Certaines centrales fournissent leur version via cette URL : *http://192.168.1.234/cfg/vers* ou *http://192.168.1.234:9876/cfg/vers*

### Utilisation de l'interface web d'origine

⚠️ **La centrale ne gérant qu'une seule session utilisateur à la fois il est nécesaire de désactiver temporairement l'intégration si vous voulez pouvoir utiliser l'interface web.**

### Utilisation de l'application mobile d'origine

⚠️ L'utilisation de l'application mobile 'Somfy Alarme' reste possible même avec l'intégration active.

### Re-configuration de l'intégration

L'intégration supporte la re-configuration à partie de l'interface graphique.

## Les contributions sont les bienvenues !
Si vous voulez contribuer :  [Contribution guidelines](CONTRIBUTING.md)

## Credits
Le code a principalement été repris de [@Ludeeus](https://github.com/ludeeus) [integration_blueprint][integration_blueprint].

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square
[license-shield]: https://img.shields.io/github/license/the8tre/somfy-protexial.svg?style=flat-square
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40the8tre-blue.svg?style=flat-square
[releases-shield]: https://img.shields.io/github/v/release/AuroreVgn/somfy-protexial.svg?style=flat-square
[releases]: https://github.com/AuroreVgn/somfy-protexial/releases
[user_profile]: https://github.com/AuroreVgn
