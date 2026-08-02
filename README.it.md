# Somfy Protexial / Protexiom / Protexial IO

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)
[![Maintainers](https://img.shields.io/badge/maintainers-@AuroreVgn%20|%20@the8tre-blue.svg?style=flat-square)](#)

![header](assets/header.png)

## Altre lingue

[English](README.en.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Italiano](README.it.md) | [Nederlands](README.nl.md) | [Português](README.pt.md)

## Informazioni

🔀 Questa versione 2.0.x è un **fork aggiornato** dell'integrazione originale di [the8tre](https://github.com/the8tre), disponibile [qui](https://github.com/the8tre/somfy-protexial).

Gli obiettivi principali di questa integrazione sono:

- anticipare la **disattivazione della rete 2G**, offrendo un'alternativa affidabile senza dover sostituire l'intero sistema di allarme. In questo modo è possibile ricevere notifiche di intrusione (o di altri eventi) direttamente tramite Home Assistant e l'applicazione per smartphone, incluse le notifiche critiche (cioè notifiche che vengono ricevute anche quando il telefono è in modalità silenziosa).
- anticipare la [**chiusura dei server Somfy Protexial/Protexiom**](https://forum.hacf.fr/t/integration-custom-centrale-somfy-protexial/23589/223), anche se l'impatto previsto dovrebbe essere molto limitato.

Questa integrazione permette di collegare le centrali di allarme Somfy Protexial, Protexiom e Protexial IO a Home Assistant.

### Modelli testati

| Modello | Versione | Stato |
| -------------- | --------------- | ------------------ |
| Protexial IO | `2013 (v10_13)` | :white_check_mark: |
| Protexiom 5000 | `2013 (v10_3)` | :white_check_mark: |
| Protexial | `2013 (v10_13)` | :white_check_mark: |
| Protexial | `2013 (v10_14)` | :white_check_mark: |
| Protexial | `2013 (v10_15)` | :white_check_mark: |
| Protexial | `2010 (v7_9)` | :white_check_mark: |
| Protexial | `2010 (v8_1)` | :white_check_mark: |
| Protexial | `2008` | :white_check_mark: |

⚠️ Se il tuo modello non è presente in questo elenco **non significa** necessariamente che non sia compatibile. Potrebbe semplicemente non essere ancora stato testato o segnalato dagli utenti.

🔎 L'integrazione consente di visualizzare lo stato dell'allarme e di tutti i dispositivi associati.

👉🏻 L'integrazione permette di controllare:

- 🚨 l'allarme per zone (A, B e C)
- 🪟 le tapparelle
- 💡 le luci

🔃 L'integrazione consente inoltre di ripristinare gli errori relativi all'allarme, alla comunicazione radio e alle batterie.

#### Entità supportate

| Entità | Descrizione | Versione |
| ----------------------------------- | ----------------------------------------------------------- |-----------------------------------------------------------|
| `alarm_control_panel.alarme` | Supporta le modalità `armed_away`, `armed_home` e `armed_night` | 1.2.4 |
| `cover.volets` | Apertura, chiusura e arresto. Il controllo della posizione non è supportato. | 1.2.4 |
| `light.lumieres` | Accensione/spegnimento (lo stato viene mantenuto dall'integrazione. Non è possibile sapere se le luci sono state controllate tramite telecomando, interruttore o un'altra integrazione). | 1.2.4 |
| `binary_sensor.batterie` | Stato aggregato delle batterie | 1.2.4 |
| `binary_sensor.boitier` | Stato della centrale | 1.2.4 |
| `binary_sensor.communication_radio` | Stato della comunicazione radio | 1.2.4 |
| `binary_sensor.communication_gsm` | Stato della comunicazione GSM | 1.2.4 |
| `binary_sensor.mouvement_detecte` | Stato del rilevamento di movimento | 1.2.4 |
| `binary_sensor.porte_ou_fenetre` | Stato di porte e finestre | 1.2.4 |
| `binary_sensor.camera` | Stato della connessione della telecamera | 1.2.4 |
| `sensor.signal_gsm_5` | Intensità del segnale GSM (/5) | 1.2.6 |
| `sensor.operateur_gsma` | Operatore GSM | 1.2.6 |
| `sensor.alarme_derniere_sync` | Ultima sincronizzazione con la centrale | 2.0.7 |

#### Per ogni dispositivo dell'allarme vengono creati i seguenti sensori binari con i relativi attributi:

| Entità | Descrizione – Attributi | Versione |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------- | --------|
| `binary_sensor.do_ouvt_xxx` | Contatto porta - Attributi: batteria, comunicazione con la centrale, errore, manomissione, aperto/chiuso, sospeso | 2.0.0 |
| `binary_sensor.do_vitre_ouvt_xxx` | Contatto finestra con rilevamento rottura vetro - Attributi: batteria, comunicazione con la centrale, errore, manomissione, aperto/chiuso, sospeso | 2.0.0 |
| `binary_sensor.do_vitre_ouvt_xxx` | Sensore acustico di rottura vetri - Attributi: batteria, comunicazione con la centrale, errore, manomissione, aperto/chiuso, sospeso | 2.0.0 |
| `binary_sensor.do_gar_xxx` | Contatto porta garage - Attributi: batteria, comunicazione con la centrale, errore, manomissione, aperto/chiuso, sospeso | 2.0.0 |
| `binary_sensor.dm_image_mvt_xxx` | Rilevatore di movimento con acquisizione immagini - Attributi: batteria, comunicazione con la centrale, errore, manomissione, sospeso | 2.0.0 |
| `binary_sensor.dm_mvt_xxx` | Rilevatore di movimento - Attributi: batteria, comunicazione con la centrale, errore, manomissione, sospeso | 2.0.0 |
| `binary_sensor.tr_tel_xxx` | Centrale di allarme - Attributi: batteria, comunicazione con la centrale, errore, manomissione, sospeso | 2.0.0 |
| `binary_sensor.clavier_clv_xxx` | Tastiera - Attributi: batteria, comunicazione con la centrale, errore, manomissione, sospeso | 2.0.0 |
| `binary_sensor.cl_lcd_clv_xxx` | Tastiera LCD - Attributi: batteria, comunicazione con la centrale, errore, manomissione, sospeso | 2.0.0 |
| `binary_sensor.sir_ext_xxx` | Sirena esterna - Attributi: batteria, comunicazione con la centrale, errore, manomissione, sospeso | 2.0.0 |
| `binary_sensor.sir_int_xxx` | Sirena interna - Attributi: batteria, comunicazione con la centrale, errore, manomissione, sospeso | 2.0.0 |
| `binary_sensor.d_fumee_fumee_xxx` | Rilevatore di fumo - Attributi: batteria, comunicazione con la centrale, errore, sospeso | 2.0.0 |
| `binary_sensor.tc_multi_tlcmd_xxx` | Telecomando multicanale - Attributi: comunicazione con la centrale, sospeso | 2.0.0 |
| `binary_sensor.tc_4_tlcmd_xxx` | Telecomando allarme multizona - Attributi: comunicazione con la centrale, sospeso | 2.0.0 |
| `binary_sensor.badge_bdg_axxx` | Badge RFID - Attributi: comunicazione con la centrale, sospeso | 2.0.0 |

Gli attributi sono visibili nel menu **"Dettagli"**.

<img width="160" height="243" alt="image" src="https://github.com/user-attachments/assets/1fd0de09-5f3e-4dc0-b147-bb55593adf45" />

<img width="526" height="301" alt="image" src="https://github.com/user-attachments/assets/50ad793d-bddc-44b5-915a-b569b7cb5050" />

#### Pulsanti supportati

| Entità | Descrizione | Versione |
| ----------------------------------- | ----------------------------------------------------------- |-----------------------------------------------------------|
| `button.reinitialiser_defaut_alarme` | Ripristina gli errori di allarme (movimento, apertura e manomissione) | 2.0.7 |
| `button.reinitialiser_defaut_liaison_radio` | Ripristina gli errori di comunicazione radio tra la centrale e i sensori | 2.0.7 |
| `button.reinitialiser_defaut_piles` | Ripristina gli errori delle batterie | 2.0.7 |

## Installazione

### Opzione A: Installazione tramite HACS (consigliata)

1. Aggiungere questo repository GitHub a HACS
   - Automaticamente: [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=integration&repository=somfy-protexial&owner=AuroreVgn) <br />
   - Manualmente:
      - HACS → Integrazioni → Menu "..." → Repository personalizzati
      - Repository: `https://github.com/AuroreVgn/somfy-protexial`
      - Categoria: `Integrazione`
3. Scaricare l'integrazione
   - HACS → Integrazioni → Somfy Protexial → Scarica
4. Riavviare Home Assistant

### Opzione B: Installazione manuale

1. Scaricare l'archivio dell'ultima versione disponibile: [somfy_protexial.zip](https://github.com/AuroreVgn/somfy-protexial/archive/refs/tags/2.0.11.zip)
2. Individuare la cartella contenente il file `configuration.yaml` della propria installazione di Home Assistant.
3. Se la cartella `custom_components` non esiste, crearla.
4. Creare una cartella `somfy_protexial` all'interno di `custom_components`.
5. Estrarre il contenuto di `somfy_protexial.zip` nella cartella `somfy_protexial`.
6. Riavviare Home Assistant.

## Configurazione

- Aggiungere l'integrazione utilizzando [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=somfy_protexial) oppure manualmente.
- Impostazioni → Dispositivi e servizi → + Aggiungi integrazione → Somfy Protexial

### 1. Indirizzo della centrale

- Inserire l'URL dell'interfaccia web locale della centrale:
  `http://192.168.1.234` oppure `http://192.168.1.234:9876`

</br>

<img src="assets/welcome.png" width="50%"><img src="assets/login_io.jpeg" width="50%">

### 2. Credenziali utente

- Utente: `"u"` (**mantenere il valore precompilato**)
- Password: inserire la password normalmente utilizzata.
- Codice di autenticazione: inserire il codice della scheda di autenticazione corrispondente alla richiesta visualizzata.

<img src="assets/step2.png" width="50%">

### 3. Configurazione aggiuntiva

Le diverse modalità di inserimento utilizzano le zone configurate nella centrale Somfy:

- Inserimento totale (sempre disponibile): zone A+B+C
- Inserimento notturno (opzionale): qualsiasi combinazione tra A, B, C, A+B, B+C o A+C
- Inserimento parziale / in casa (opzionale): qualsiasi combinazione tra A, B, C, A+B, B+C o A+C

**Codice di inserimento/disinserimento**

Se viene configurato un codice, questo verrà richiesto ogni volta che si inserisce o si disinserisce l'allarme.

**Intervallo di aggiornamento**

Da **15 secondi** a **1 ora**. Il valore predefinito è **60 secondi**.

Non è consigliabile utilizzare un intervallo inferiore, poiché l'interfaccia web della centrale potrebbe diventare instabile.

<img src="assets/step3.png" width="50%">

## Note

### Scheda Lovelace per Home Assistant (stato e controllo)

È stata sviluppata una [scheda Lovelace](https://github.com/developpeurbox/somfy-protexial-card) dedicata a questa integrazione.

### Scheda Mushroom Template (dettagli dei dispositivi)

È disponibile [qui](https://github.com/AuroreVgn/somfy-protexial/blob/main/assets/Template%20Home%20Assistant) un modello Home Assistant per visualizzare ciascun dispositivo dell'allarme con i relativi attributi (batteria, comunicazione, ecc.).

<img width="485" height="127" alt="image" src="https://github.com/user-attachments/assets/d4f385c0-0171-4968-b369-c4cb86d8409e" />

### Compatibilità delle versioni

L'elenco delle versioni compatibili riportato all'inizio di questa pagina **non è esaustivo**. È possibile che questa integrazione sia compatibile anche con altre versioni delle centrali Somfy. Se hai testato con successo un'altra versione, fammelo sapere!

L'anno o la generazione dell'interfaccia web della centrale è riportato nella parte inferiore delle pagine:

<img src="assets/version.png" width="30%">

Alcune centrali mettono inoltre a disposizione la versione del firmware tramite il seguente URL:

*http://192.168.1.234/cfg/vers*

oppure

*http://192.168.1.234:9876/cfg/vers*

### Utilizzo dell'interfaccia web originale

⚠️ **La centrale supporta una sola sessione utente alla volta. Se desideri utilizzare l'interfaccia web originale, dovrai disabilitare temporaneamente questa integrazione.**

### Utilizzo dell'applicazione mobile originale

⚠️ L'app ufficiale **Somfy Alarme** può continuare a essere utilizzata anche quando questa integrazione è attiva.

### Riconfigurazione dell'integrazione

L'integrazione supporta la riconfigurazione completa direttamente dall'interfaccia grafica di Home Assistant.

## I contributi sono i benvenuti!

Se desideri contribuire al progetto, consulta le [Contribution guidelines](CONTRIBUTING.md).

## Crediti

Questa integrazione è basata principalmente sul lavoro di [@Ludeeus](https://github.com/ludeeus) e sul progetto [integration_blueprint][integration_blueprint].

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square
[license-shield]: https://img.shields.io/github/license/the8tre/somfy-protexial.svg?style=flat-square
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40the8tre-blue.svg?style=flat-square
[releases-shield]: https://img.shields.io/github/v/release/AuroreVgn/somfy-protexial.svg?style=flat-square
[releases]: https://github.com/AuroreVgn/somfy-protexial/releases
[user_profile]: https://github.com/AuroreVgn
