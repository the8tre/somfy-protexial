# Somfy Protexial / Protexiom / Protexial IO

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)
[![Maintainers](https://img.shields.io/badge/maintainers-@AuroreVgn%20|%20@the8tre-blue.svg?style=flat-square)](#)

![header](assets/header.png)

## Weitere Sprachen

[English](README.en.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Italiano](README.it.md) | [Nederlands](README.nl.md) | [Português](README.pt.md)

## Über diese Integration

🔀 Diese Version 2.0.x ist ein **aktualisierter Fork** der ursprünglichen Integration von [the8tre](https://github.com/the8tre), verfügbar [hier](https://github.com/the8tre/somfy-protexial).

Die Hauptziele dieser Integration sind:

- das **Abschalten des 2G-Netzes** zu antizipieren, indem eine zuverlässige Alternative bereitgestellt wird, ohne die gesamte Alarmanlage austauschen zu müssen. Benachrichtigungen über Einbrüche (oder andere Ereignisse) können direkt über Home Assistant und die Smartphone-App versendet werden, einschließlich kritischer Benachrichtigungen (die auch im Lautlos-Modus ausgelöst werden).
- das [**Abschalten der Somfy Protexial-/Protexiom-Server**](https://forum.hacf.fr/t/integration-custom-centrale-somfy-protexial/23589/223) zu berücksichtigen (auch wenn die Auswirkungen voraussichtlich sehr gering sein werden).

Diese Integration ermöglicht die Anbindung einer Somfy Protexial-, Protexiom- oder Protexial IO-Alarmzentrale an Home Assistant.

### Getestete Modelle

| Modell | Version | Status |
| -------------- | --------------- | ------------------ |
| Protexial IO | `2013 (v10_13)` | :white_check_mark: |
| Protexiom 5000 | `2013 (v10_3)` | :white_check_mark: |
| Protexial | `2013 (v10_13)` | :white_check_mark: |
| Protexial | `2013 (v10_14)` | :white_check_mark: |
| Protexial | `2013 (v10_15)` | :white_check_mark: |
| Protexial | `2010 (v7_9)` | :white_check_mark: |
| Protexial | `2010 (v8_1)` | :white_check_mark: |
| Protexial | `2008` | :white_check_mark: |

⚠️ Dass ein Modell hier nicht aufgeführt ist, bedeutet **nicht**, dass es nicht unterstützt wird. Es wurde möglicherweise lediglich noch nicht getestet oder gemeldet.

🔎 Die Integration ermöglicht die Anzeige des Alarmstatus sowie des Status aller Alarmkomponenten.

👉🏻 Folgende Funktionen können gesteuert werden:

- 🚨 Alarm nach Zonen (A, B, C)
- 🪟 Rollläden
- 💡 Beleuchtung

🔃 Darüber hinaus können Alarm-, Funkverbindungs- und Batteriestörungen zurückgesetzt werden.

#### Unterstützte Entitäten

| Entität | Beschreibung | Version |
| ----------------------------------- | ----------------------------------------------------------- |-----------------------------------------------------------|
| `alarm_control_panel.alarme` | Unterstützt die Modi `armed_away`, `armed_home` und `armed_night` | 1.2.4 |
| `cover.volets` | Öffnen, Schließen und Stoppen. Keine Positionssteuerung. | 1.2.4 |
| `light.lumieres` | Ein/Aus (der Status wird von der Integration verwaltet. Es kann nicht erkannt werden, ob das Licht über eine Fernbedienung, einen Schalter oder eine andere Integration geschaltet wurde.) | 1.2.4 |
| `binary_sensor.batterie` | Zusammengefasster Batteriestatus | 1.2.4 |
| `binary_sensor.boitier` | Status der Alarmzentrale | 1.2.4 |
| `binary_sensor.communication_radio` | Status der Funkverbindung | 1.2.4 |
| `binary_sensor.communication_gsm` | Status der GSM-Verbindung | 1.2.4 |
| `binary_sensor.mouvement_detecte` | Status der Bewegungserkennung | 1.2.4 |
| `binary_sensor.porte_ou_fenetre` | Status von Türen und Fenstern | 1.2.4 |
| `binary_sensor.camera` | Status der Kameraverbindung | 1.2.4 |
| `sensor.signal_gsm_5` | GSM-Signalstärke (/5) | 1.2.6 |
| `sensor.operateur_gsma` | GSM-Netzbetreiber | 1.2.6 |
| `sensor.alarme_derniere_sync` | Letzte Synchronisierung mit der Alarmzentrale | 2.0.7 |

#### Für jedes Alarmgerät werden folgende Binary Sensoren mit Attributen erstellt:

| Entität | Beschreibung – Attribute | Version |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------- | --------|
| `binary_sensor.do_ouvt_xxx` | Türkontakt – Batterie, Verbindung zur Zentrale, Fehler, Sabotage, offen/geschlossen, pausiert | 2.0.0 |
| `binary_sensor.do_vitre_ouvt_xxx` | Fensterkontakt mit Glasbrucherkennung – Batterie, Verbindung zur Zentrale, Fehler, Sabotage, offen/geschlossen, pausiert | 2.0.0 |
| `binary_sensor.do_vitre_ouvt_xxx` | Akustischer Glasbruchmelder – Batterie, Verbindung zur Zentrale, Fehler, Sabotage, offen/geschlossen, pausiert | 2.0.0 |
| `binary_sensor.do_gar_xxx` | Garagentorkontakt – Batterie, Verbindung zur Zentrale, Fehler, Sabotage, offen/geschlossen, pausiert | 2.0.0 |
| `binary_sensor.dm_image_mvt_xxx` | Bewegungsmelder mit Bildaufnahme – Batterie, Verbindung zur Zentrale, Fehler, Sabotage, pausiert | 2.0.0 |
| `binary_sensor.dm_mvt_xxx` | Bewegungsmelder – Batterie, Verbindung zur Zentrale, Fehler, Sabotage, pausiert | 2.0.0 |
| `binary_sensor.tr_tel_xxx` | Alarmzentrale – Batterie, Verbindung zur Zentrale, Fehler, Sabotage, pausiert | 2.0.0 |
| `binary_sensor.clavier_clv_xxx` | Tastatur – Batterie, Verbindung zur Zentrale, Fehler, Sabotage, pausiert | 2.0.0 |
| `binary_sensor.cl_lcd_clv_xxx` | LCD-Tastatur – Batterie, Verbindung zur Zentrale, Fehler, Sabotage, pausiert | 2.0.0 |
| `binary_sensor.sir_ext_xxx` | Außensirene – Batterie, Verbindung zur Zentrale, Fehler, Sabotage, pausiert | 2.0.0 |
| `binary_sensor.sir_int_xxx` | Innensirene – Batterie, Verbindung zur Zentrale, Fehler, Sabotage, pausiert | 2.0.0 |
| `binary_sensor.d_fumee_fumee_xxx` | Rauchmelder – Batterie, Verbindung zur Zentrale, Fehler, pausiert | 2.0.0 |
| `binary_sensor.tc_multi_tlcmd_xxx` | Mehrkanal-Fernbedienung – Verbindung zur Zentrale, pausiert | 2.0.0 |
| `binary_sensor.tc_4_tlcmd_xxx` | Mehrzonen-Fernbedienung – Verbindung zur Zentrale, pausiert | 2.0.0 |
| `binary_sensor.badge_bdg_axxx` | RFID-Badge – Verbindung zur Zentrale, pausiert | 2.0.0 |

Die Attribute sind im Menü **„Details“** sichtbar.

<img width="160" height="243" alt="image" src="https://github.com/user-attachments/assets/1fd0de09-5f3e-4dc0-b147-bb55593adf45" />

<img width="526" height="301" alt="image" src="https://github.com/user-attachments/assets/50ad793d-bddc-44b5-915a-b569b7cb5050" />

#### Unterstützte Schaltflächen

| Entität | Beschreibung | Version |
| ----------------------------------- | ----------------------------------------------------------- |-----------------------------------------------------------|
| `button.reinitialiser_defaut_alarme` | Alarmstörungen zurücksetzen (Bewegung, Öffnung, Sabotage) | 2.0.7 |
| `button.reinitialiser_defaut_liaison_radio` | Funkverbindungsfehler zwischen Zentrale und Sensoren zurücksetzen | 2.0.7 |
| `button.reinitialiser_defaut_piles` | Batteriestörungen zurücksetzen | 2.0.7 |

## Installation

### Option A: Installation über HACS (empfohlen)

1. Dieses GitHub-Repository zu HACS hinzufügen
   - Automatisch: [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=integration&repository=somfy-protexial&owner=AuroreVgn) <br />
   - Manuell:
      - HACS → Integrationen → Menü „...“ → Benutzerdefinierte Repositories
      - Repository: `https://github.com/AuroreVgn/somfy-protexial`
      - Kategorie: `Integration`
3. Die Integration herunterladen
   - HACS → Integrationen → Somfy Protexial → Herunterladen
4. Home Assistant neu starten

### Option B: Manuelle Installation

1. Das Archiv der neuesten Version herunterladen: [somfy_protexial.zip](https://github.com/AuroreVgn/somfy-protexial/archive/refs/tags/2.0.11.zip)
2. Das Verzeichnis suchen, das die Datei `configuration.yaml` Ihrer Home-Assistant-Installation enthält.
3. Falls das Verzeichnis `custom_components` nicht existiert, erstellen Sie es.
4. Erstellen Sie darin ein Verzeichnis `somfy_protexial`.
5. Entpacken Sie den Inhalt von `somfy_protexial.zip` in dieses Verzeichnis.
6. Starten Sie Home Assistant neu.

## Konfiguration

- Fügen Sie die Integration hinzu: [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=somfy_protexial) oder manuell.
- Einstellungen → Geräte & Dienste → + Integration hinzufügen → Somfy Protexial

### 1. Adresse der Alarmzentrale

- Geben Sie die URL der lokalen Weboberfläche Ihrer Alarmzentrale ein:
  `http://192.168.1.234` oder `http://192.168.1.234:9876`

</br>

<img src="assets/welcome.png" width="50%"><img src="assets/login_io.jpeg" width="50%">

### 2. Benutzeranmeldung

- Benutzername: `"u"` (**den vorausgefüllten Wert beibehalten**)
- Passwort: Geben Sie Ihr gewohntes Passwort ein.
- Authentifizierungscode: Geben Sie den Code Ihrer Authentifizierungskarte entsprechend der angezeigten Challenge ein.

<img src="assets/step2.png" width="50%">

### 3. Zusätzliche Konfiguration

Die verschiedenen Scharfschaltungsmodi basieren auf den in der Somfy-Zentrale konfigurierten Bereichen:

- Abwesenheitsmodus (immer verfügbar): Bereiche A+B+C
- Nachtmodus (optional): frei wählbare Kombination aus A, B, C, A+B, B+C oder A+C
- Anwesenheitsmodus (optional): frei wählbare Kombination aus A, B, C, A+B, B+C oder A+C

**Code für Scharf-/Unscharfschaltung**

Wenn Sie einen Code festlegen, wird dieser beim Scharf- und Unscharfschalten abgefragt.

**Aktualisierungsintervall**

Von **15 Sekunden** bis **1 Stunde**. Standardwert: **60 Sekunden**.

Ein kürzeres Intervall wird nicht empfohlen, da die Weboberfläche der Alarmzentrale dadurch instabil werden kann.

<img src="assets/step3.png" width="50%">

## Hinweise

### Lovelace-Karte für Home Assistant (Status & Steuerung)

Für diese Integration wurde eine spezielle [Lovelace-Karte](https://github.com/developpeurbox/somfy-protexial-card) entwickelt.

### Mushroom-Template-Karte (Gerätedetails)

Ein Home-Assistant-Template zur Darstellung aller Alarmkomponenten einschließlich ihrer Attribute (Batterie, Funkverbindung usw.) ist [hier](https://github.com/AuroreVgn/somfy-protexial/blob/main/assets/Template%20Home%20Assistant) verfügbar.

<img width="485" height="127" alt="image" src="https://github.com/user-attachments/assets/d4f385c0-0171-4968-b369-c4cb86d8409e" />

### Versionskompatibilität

Die oben aufgeführte Kompatibilitätsliste ist **nicht vollständig**. Diese Integration kann durchaus mit weiteren Versionen von Somfy-Alarmzentralen funktionieren. Wenn Sie eine andere Version erfolgreich getestet haben, freue ich mich über eine Rückmeldung.

Das Baujahr bzw. die Generation der Weboberfläche Ihrer Alarmzentrale wird am unteren Rand der Seiten angezeigt:

<img src="assets/version.png" width="30%">

Einige Zentralen stellen ihre Firmware-Version außerdem unter folgender URL bereit:

*http://192.168.1.234/cfg/vers*

oder

*http://192.168.1.234:9876/cfg/vers*

### Verwendung der originalen Weboberfläche

⚠️ **Die Alarmzentrale unterstützt immer nur eine aktive Benutzersitzung gleichzeitig. Wenn Sie die originale Weboberfläche verwenden möchten, müssen Sie die Integration vorübergehend deaktivieren.**

### Verwendung der originalen mobilen App

⚠️ Die offizielle **Somfy Alarme**-App kann auch bei aktiver Integration weiterhin verwendet werden.

### Neukonfiguration der Integration

Die Integration unterstützt eine vollständige Neukonfiguration direkt über die grafische Benutzeroberfläche von Home Assistant.

## Beiträge sind willkommen!

Wenn Sie zur Weiterentwicklung beitragen möchten, lesen Sie bitte die [Contribution guidelines](CONTRIBUTING.md).

## Danksagung

Diese Integration basiert größtenteils auf der Arbeit von [@Ludeeus](https://github.com/ludeeus) und dem Projekt [integration_blueprint][integration_blueprint].

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square
[license-shield]: https://img.shields.io/github/license/the8tre/somfy-protexial.svg?style=flat-square
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40the8tre-blue.svg?style=flat-square
[releases-shield]: https://img.shields.io/github/v/release/AuroreVgn/somfy-protexial.svg?style=flat-square
[releases]: https://github.com/AuroreVgn/somfy-protexial/releases
[user_profile]: https://github.com/AuroreVgn
