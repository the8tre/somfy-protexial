# Somfy Protexial / Protexiom / Protexial IO

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)
[![Maintainers](https://img.shields.io/badge/maintainers-@AuroreVgn%20|%20@the8tre-blue.svg?style=flat-square)](#)

![header](assets/header.png)

## Andere talen

[English](README.en.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Italiano](README.it.md) | [Nederlands](README.nl.md) | [Português](README.pt.md)

## Over

🔀 Deze versie 2.0.x is een **bijgewerkte fork** van de oorspronkelijke integratie van [the8tre](https://github.com/the8tre), beschikbaar [hier](https://github.com/the8tre/somfy-protexial).

De belangrijkste doelstellingen van deze integratie zijn:

- het **uitfaseren van het 2G-netwerk** opvangen door een betrouwbaar alternatief te bieden, zonder het volledige alarmsysteem te hoeven vervangen. Hierdoor kunnen inbraakmeldingen (of andere meldingen) rechtstreeks via Home Assistant en de smartphone-app worden verzonden, inclusief kritieke meldingen (die ook doorkomen wanneer de telefoon op stil staat).
- anticiperen op de [**sluiting van de Somfy Protexial/Protexiom-servers**](https://forum.hacf.fr/t/integration-custom-centrale-somfy-protexial/23589/223), hoewel de impact naar verwachting zeer beperkt zal zijn.

Deze integratie maakt verbinding met Somfy Protexial-, Protexiom- en Protexial IO-alarmsystemen.

### Geteste modellen

| Model | Versie | Status |
| -------------- | --------------- | ------------------ |
| Protexial IO | `2013 (v10_13)` | :white_check_mark: |
| Protexiom 5000 | `2013 (v10_3)` | :white_check_mark: |
| Protexial | `2013 (v10_13)` | :white_check_mark: |
| Protexial | `2013 (v10_14)` | :white_check_mark: |
| Protexial | `2013 (v10_15)` | :white_check_mark: |
| Protexial | `2010 (v7_9)` | :white_check_mark: |
| Protexial | `2010 (v8_1)` | :white_check_mark: |
| Protexial | `2008` | :white_check_mark: |

⚠️ Dat een model hier niet wordt vermeld, betekent **niet** dat het niet wordt ondersteund. Het kan eenvoudigweg nog niet getest zijn of nog niet door gebruikers zijn gemeld.

🔎 De integratie maakt het mogelijk de status van het alarmsysteem en alle aangesloten apparaten te bekijken.

👉🏻 Met deze integratie kunt u het volgende bedienen:

- 🚨 het alarmsysteem per zone (A, B en C)
- 🪟 rolluiken
- 💡 verlichting

🔃 Daarnaast kunnen alarm-, radioverbinding- en batterijfouten worden gereset.

#### Ondersteunde entiteiten

| Entiteit | Beschrijving | Versie |
| ----------------------------------- | ----------------------------------------------------------- |-----------------------------------------------------------|
| `alarm_control_panel.alarme` | Ondersteunt de modi `armed_away`, `armed_home` en `armed_night` | 1.2.4 |
| `cover.volets` | Openen, sluiten en stoppen. Positieregeling wordt niet ondersteund. | 1.2.4 |
| `light.lumieres` | Aan/uit (de status wordt door de integratie bijgehouden. Er kan niet worden vastgesteld of de verlichting via een afstandsbediening, schakelaar of een andere integratie is bediend). | 1.2.4 |
| `binary_sensor.batterie` | Gecombineerde batterijstatus | 1.2.4 |
| `binary_sensor.boitier` | Status van de alarmcentrale | 1.2.4 |
| `binary_sensor.communication_radio` | Status van de radioverbinding | 1.2.4 |
| `binary_sensor.communication_gsm` | Status van de GSM-verbinding | 1.2.4 |
| `binary_sensor.mouvement_detecte` | Status van bewegingsdetectie | 1.2.4 |
| `binary_sensor.porte_ou_fenetre` | Status van deuren en ramen | 1.2.4 |
| `binary_sensor.camera` | Status van de cameraverbinding | 1.2.4 |
| `sensor.signal_gsm_5` | GSM-signaalsterkte (/5) | 1.2.6 |
| `sensor.operateur_gsma` | GSM-provider | 1.2.6 |
| `sensor.alarme_derniere_sync` | Laatste synchronisatie met de alarmcentrale | 2.0.7 |

#### Voor elk alarmapparaat worden de volgende binaire sensoren met attributen aangemaakt:

| Entiteit | Beschrijving – Attributen | Versie |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------- | --------|
| `binary_sensor.do_ouvt_xxx` | Deurcontact - Attributen: batterij, verbinding met de centrale, fout, sabotage, open/gesloten, gepauzeerd | 2.0.0 |
| `binary_sensor.do_vitre_ouvt_xxx` | Raamcontact met glasbreukdetectie - Attributen: batterij, verbinding met de centrale, fout, sabotage, open/gesloten, gepauzeerd | 2.0.0 |
| `binary_sensor.do_vitre_ouvt_xxx` | Akoestische glasbreukdetector - Attributen: batterij, verbinding met de centrale, fout, sabotage, open/gesloten, gepauzeerd | 2.0.0 |
| `binary_sensor.do_gar_xxx` | Garagedeurcontact - Attributen: batterij, verbinding met de centrale, fout, sabotage, open/gesloten, gepauzeerd | 2.0.0 |
| `binary_sensor.dm_image_mvt_xxx` | Bewegingsmelder met beeldopname - Attributen: batterij, verbinding met de centrale, fout, sabotage, gepauzeerd | 2.0.0 |
| `binary_sensor.dm_mvt_xxx` | Bewegingsmelder - Attributen: batterij, verbinding met de centrale, fout, sabotage, gepauzeerd | 2.0.0 |
| `binary_sensor.tr_tel_xxx` | Alarmcentrale - Attributen: batterij, verbinding met de centrale, fout, sabotage, gepauzeerd | 2.0.0 |
| `binary_sensor.clavier_clv_xxx` | Toetsenbord - Attributen: batterij, verbinding met de centrale, fout, sabotage, gepauzeerd | 2.0.0 |
| `binary_sensor.cl_lcd_clv_xxx` | LCD-toetsenbord - Attributen: batterij, verbinding met de centrale, fout, sabotage, gepauzeerd | 2.0.0 |
| `binary_sensor.sir_ext_xxx` | Buitensirene - Attributen: batterij, verbinding met de centrale, fout, sabotage, gepauzeerd | 2.0.0 |
| `binary_sensor.sir_int_xxx` | Binnensirene - Attributen: batterij, verbinding met de centrale, fout, sabotage, gepauzeerd | 2.0.0 |
| `binary_sensor.d_fumee_fumee_xxx` | Rookmelder - Attributen: batterij, verbinding met de centrale, fout, gepauzeerd | 2.0.0 |
| `binary_sensor.tc_multi_tlcmd_xxx` | Meerkanaals afstandsbediening - Attributen: verbinding met de centrale, gepauzeerd | 2.0.0 |
| `binary_sensor.tc_4_tlcmd_xxx` | Afstandsbediening voor meerdere alarmzones - Attributen: verbinding met de centrale, gepauzeerd | 2.0.0 |
| `binary_sensor.badge_bdg_axxx` | RFID-badge - Attributen: verbinding met de centrale, gepauzeerd | 2.0.0 |

De attributen zijn zichtbaar in het menu **"Details"**.

<img width="160" height="243" alt="image" src="https://github.com/user-attachments/assets/1fd0de09-5f3e-4dc0-b147-bb55593adf45" />

<img width="526" height="301" alt="image" src="https://github.com/user-attachments/assets/50ad793d-bddc-44b5-915a-b569b7cb5050" />

#### Ondersteunde knoppen

| Entiteit | Beschrijving | Versie |
| ----------------------------------- | ----------------------------------------------------------- |-----------------------------------------------------------|
| `button.reinitialiser_defaut_alarme` | Alarmfouten resetten (beweging, opening en sabotage) | 2.0.7 |
| `button.reinitialiser_defaut_liaison_radio` | Radioverbindingsfouten tussen de centrale en de sensoren resetten | 2.0.7 |
| `button.reinitialiser_defaut_piles` | Batterijfouten resetten | 2.0.7 |

## Installatie

### Optie A: Installatie via HACS (aanbevolen)

1. Voeg deze GitHub-repository toe aan HACS.
   - Automatisch: [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=integration&repository=somfy-protexial&owner=AuroreVgn) <br />
   - Handmatig:
      - HACS → Integraties → Menu "..." → Aangepaste repositories
      - Repository: `https://github.com/AuroreVgn/somfy-protexial`
      - Categorie: `Integratie`
3. Download de integratie.
   - HACS → Integraties → Somfy Protexial → Downloaden
4. Herstart Home Assistant.

### Optie B: Handmatige installatie

1. Download het archief van de nieuwste beschikbare versie: [somfy_protexial.zip](https://github.com/AuroreVgn/somfy-protexial/archive/refs/tags/2.0.11.zip)
2. Zoek de map waarin het bestand `configuration.yaml` van uw Home Assistant-installatie zich bevindt.
3. Maak de map `custom_components` aan als deze nog niet bestaat.
4. Maak binnen `custom_components` een map `somfy_protexial` aan.
5. Pak de inhoud van `somfy_protexial.zip` uit in de map `somfy_protexial`.
6. Herstart Home Assistant.

## Configuratie

- Voeg de integratie toe via [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=somfy_protexial) of handmatig.
- Instellingen → Apparaten en diensten → + Integratie toevoegen → Somfy Protexial

### 1. Adres van de alarmcentrale

- Voer de URL van de lokale webinterface van uw alarmcentrale in:
  `http://192.168.1.234` of `http://192.168.1.234:9876`

</br>

<img src="assets/welcome.png" width="50%"><img src="assets/login_io.jpeg" width="50%">

### 2. Gebruikersgegevens

- Gebruikersnaam: `"u"` (**laat de vooraf ingevulde waarde ongewijzigd**)
- Wachtwoord: voer uw gebruikelijke wachtwoord in.
- Authenticatiecode: voer de code van uw authenticatiekaart in die overeenkomt met de gevraagde challenge.

<img src="assets/step2.png" width="50%">

### 3. Aanvullende configuratie

De verschillende inschakelmodi zijn gebaseerd op de zones die in de Somfy-alarmcentrale zijn geconfigureerd:

- Afwezigheidsmodus (altijd beschikbaar): zones A+B+C
- Nachtmodus (optioneel): een willekeurige combinatie van A, B, C, A+B, B+C of A+C
- Thuismodus (optioneel): een willekeurige combinatie van A, B, C, A+B, B+C of A+C

**In-/uitschakelcode**

Als u een code opgeeft, wordt deze gevraagd bij het in- en uitschakelen van het alarmsysteem.

**Vernieuwingsinterval**

Van **15 seconden** tot **1 uur**. De standaardwaarde is **60 seconden**.

Het wordt afgeraden een korter interval te gebruiken, omdat de webinterface van de alarmcentrale hierdoor instabiel kan worden.

<img src="assets/step3.png" width="50%">

## Opmerkingen

### Lovelace-kaart voor Home Assistant (status en bediening)

Er is een speciale [Lovelace-kaart](https://github.com/developpeurbox/somfy-protexial-card) ontwikkeld voor deze integratie.

### Mushroom Template-kaart (apparaatdetails)

Een Home Assistant-template om elk alarmapparaat met zijn attributen (batterij, verbinding, enz.) weer te geven is [hier](https://github.com/AuroreVgn/somfy-protexial/blob/main/assets/Template%20Home%20Assistant) beschikbaar.

<img width="485" height="127" alt="image" src="https://github.com/user-attachments/assets/d4f385c0-0171-4968-b369-c4cb86d8409e" />

### Versiecompatibiliteit

De compatibiliteitslijst bovenaan deze pagina is **niet volledig**. Het is goed mogelijk dat deze integratie ook compatibel is met andere versies van Somfy-alarmcentrales. Laat het gerust weten als u een andere versie succesvol hebt getest.

Het bouwjaar of de generatie van de webinterface van uw alarmcentrale wordt onderaan de pagina's weergegeven:

<img src="assets/version.png" width="30%">

Sommige centrales stellen hun firmwareversie ook beschikbaar via:

*http://192.168.1.234/cfg/vers*

of

*http://192.168.1.234:9876/cfg/vers*

### Gebruik van de originele webinterface

⚠️ **De alarmcentrale ondersteunt slechts één actieve gebruikerssessie tegelijk. Als u de originele webinterface wilt gebruiken, moet u deze integratie tijdelijk uitschakelen.**

### Gebruik van de originele mobiele app

⚠️ De officiële **Somfy Alarme**-app kan ook worden gebruikt terwijl deze integratie actief is.

### De integratie opnieuw configureren

De integratie ondersteunt volledige herconfiguratie rechtstreeks vanuit de grafische gebruikersinterface van Home Assistant.

## Bijdragen zijn welkom!

Wilt u bijdragen aan het project? Raadpleeg dan de [Contribution guidelines](CONTRIBUTING.md).

## Dankwoord

Deze integratie is grotendeels gebaseerd op het werk van [@Ludeeus](https://github.com/ludeeus) en het project [integration_blueprint][integration_blueprint].

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square
[license-shield]: https://img.shields.io/github/license/the8tre/somfy-protexial.svg?style=flat-square
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40the8tre-blue.svg?style=flat-square
[releases-shield]: https://img.shields.io/github/v/release/AuroreVgn/somfy-protexial.svg?style=flat-square
[releases]: https://github.com/AuroreVgn/somfy-protexial/releases
[user_profile]: https://github.com/AuroreVgn
