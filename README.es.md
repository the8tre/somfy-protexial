# Somfy Protexial / Protexiom / Protexial IO

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)
[![Maintainers](https://img.shields.io/badge/maintainers-@AuroreVgn%20|%20@the8tre-blue.svg?style=flat-square)](#)

![header](assets/header.png)

## Otros idiomas

[English](README.en.md) | [Deutsch](README.de.md) | [Español](README.es.md) | [Italiano](README.it.md) | [Nederlands](README.nl.md) | [Português](README.pt.md)

## Acerca de

🔀 Esta versión 2.0.x es un **fork actualizado** de la integración original de [the8tre](https://github.com/the8tre), disponible [aquí](https://github.com/the8tre/somfy-protexial).

Los principales objetivos de esta integración son anticiparse a:

- el **apagado de la red 2G**, proporcionando una alternativa fiable sin necesidad de sustituir todo el sistema de alarma, permitiendo recibir alertas de intrusión (u otros eventos) directamente en Home Assistant y en la aplicación móvil mediante notificaciones críticas (es decir, notificaciones que suenan incluso con el teléfono en silencio).
- el [**cierre de los servidores de Somfy Protexial/Protexiom**](https://forum.hacf.fr/t/integration-custom-centrale-somfy-protexial/23589/223) (aunque se espera que el impacto sea muy limitado).

Esta integración proporciona la comunicación con las centrales de alarma Somfy Protexial, Protexiom y Protexial IO.

### Modelos probados

| Modelo | Versión | Estado |
| -------------- | --------------- | ------------------ |
| Protexial IO | `2013 (v10_13)` | :white_check_mark: |
| Protexiom 5000 | `2013 (v10_3)` | :white_check_mark: |
| Protexial | `2013 (v10_13)` | :white_check_mark: |
| Protexial | `2013 (v10_14)` | :white_check_mark: |
| Protexial | `2013 (v10_15)` | :white_check_mark: |
| Protexial | `2010 (v7_9)` | :white_check_mark: |
| Protexial | `2010 (v8_1)` | :white_check_mark: |
| Protexial | `2008` | :white_check_mark: |

⚠️ Que un modelo no aparezca en esta lista **no significa** que no sea compatible. Simplemente puede que todavía no haya sido probado o comunicado por otros usuarios.

🔎 La integración permite visualizar el estado de la alarma y de todos sus dispositivos.

👉🏻 La integración permite controlar:

- 🚨 la alarma por zonas (A, B y C)
- 🪟 las persianas
- 💡 las luces

🔃 La integración también permite restablecer los fallos de alarma, comunicación por radio y batería.

#### Entidades compatibles

| Entidad | Descripción | Versión |
| ----------------------------------- | ----------------------------------------------------------- |-----------------------------------------------------------|
| `alarm_control_panel.alarme` | Compatible con los modos `armed_away`, `armed_home` y `armed_night` | 1.2.4 |
| `cover.volets` | Abrir, cerrar y detener. No admite control de posición. | 1.2.4 |
| `light.lumieres` | Encendido/apagado (el estado es mantenido por la integración. No es posible detectar si las luces se han encendido o apagado mediante un mando a distancia, un interruptor u otra integración). | 1.2.4 |
| `binary_sensor.batterie` | Estado agregado de las baterías | 1.2.4 |
| `binary_sensor.boitier` | Estado de la central | 1.2.4 |
| `binary_sensor.communication_radio` | Estado de la comunicación por radio | 1.2.4 |
| `binary_sensor.communication_gsm` | Estado de la comunicación GSM | 1.2.4 |
| `binary_sensor.mouvement_detecte` | Estado de detección de movimiento | 1.2.4 |
| `binary_sensor.porte_ou_fenetre` | Estado de puertas y ventanas | 1.2.4 |
| `binary_sensor.camera` | Estado de conexión de la cámara | 1.2.4 |
| `sensor.signal_gsm_5` | Intensidad de la señal GSM (/5) | 1.2.6 |
| `sensor.operateur_gsma` | Operador GSM | 1.2.6 |
| `sensor.alarme_derniere_sync` | Última sincronización con la central de alarma | 2.0.7 |

#### Se crean los siguientes sensores binarios para representar cada dispositivo de la alarma junto con sus atributos:

| Entidad | Descripción – Atributos | Versión |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------- | --------|
| `binary_sensor.do_ouvt_xxx` | Contacto de puerta: batería, comunicación con la central, fallo, sabotaje, abierta/cerrada, pausado | 2.0.0 |
| `binary_sensor.do_vitre_ouvt_xxx` | Contacto de ventana con detección de rotura de cristal: batería, comunicación con la central, fallo, sabotaje, abierta/cerrada, pausado | 2.0.0 |
| `binary_sensor.do_vitre_ouvt_xxx` | Detector acústico de rotura de cristales: batería, comunicación con la central, fallo, sabotaje, abierta/cerrada, pausado | 2.0.0 |
| `binary_sensor.do_gar_xxx` | Contacto de puerta de garaje: batería, comunicación con la central, fallo, sabotaje, abierta/cerrada, pausado | 2.0.0 |
| `binary_sensor.dm_image_mvt_xxx` | Detector de movimiento con captura de imágenes: batería, comunicación con la central, fallo, sabotaje, pausado | 2.0.0 |
| `binary_sensor.dm_mvt_xxx` | Detector de movimiento: batería, comunicación con la central, fallo, sabotaje, pausado | 2.0.0 |
| `binary_sensor.tr_tel_xxx` | Central de alarma: batería, comunicación con la central, fallo, sabotaje, pausado | 2.0.0 |
| `binary_sensor.clavier_clv_xxx` | Teclado: batería, comunicación con la central, fallo, sabotaje, pausado | 2.0.0 |
| `binary_sensor.cl_lcd_clv_xxx` | Teclado LCD: batería, comunicación con la central, fallo, sabotaje, pausado | 2.0.0 |
| `binary_sensor.sir_ext_xxx` | Sirena exterior: batería, comunicación con la central, fallo, sabotaje, pausado | 2.0.0 |
| `binary_sensor.sir_int_xxx` | Sirena interior: batería, comunicación con la central, fallo, sabotaje, pausado | 2.0.0 |
| `binary_sensor.d_fumee_fumee_xxx` | Detector de humo: batería, comunicación con la central, fallo, pausado | 2.0.0 |
| `binary_sensor.tc_multi_tlcmd_xxx` | Mando a distancia multicanal: comunicación con la central, pausado | 2.0.0 |
| `binary_sensor.tc_4_tlcmd_xxx` | Mando a distancia para varias zonas: comunicación con la central, pausado | 2.0.0 |
| `binary_sensor.badge_bdg_axxx` | Llavero RFID: comunicación con la central, pausado | 2.0.0 |

Los atributos pueden consultarse en el menú **"Detalles"**.

<img width="160" height="243" alt="image" src="https://github.com/user-attachments/assets/1fd0de09-5f3e-4dc0-b147-bb55593adf45" />

<img width="526" height="301" alt="image" src="https://github.com/user-attachments/assets/50ad793d-bddc-44b5-915a-b569b7cb5050" />

#### Botones compatibles

| Entidad | Descripción | Versión |
| ----------------------------------- | ----------------------------------------------------------- |-----------------------------------------------------------|
| `button.reinitialiser_defaut_alarme` | Restablecer los fallos de alarma (movimiento, apertura y sabotaje) | 2.0.7 |
| `button.reinitialiser_defaut_liaison_radio` | Restablecer los fallos de comunicación por radio entre la central y los sensores | 2.0.7 |
| `button.reinitialiser_defaut_piles` | Restablecer los fallos de batería | 2.0.7 |

## Instalación

### Opción A: Instalación mediante HACS (recomendada)

1. Añada este repositorio de GitHub a HACS.
   - Automáticamente: [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=integration&repository=somfy-protexial&owner=AuroreVgn) <br />
   - Manualmente:
      - HACS → Integraciones → Menú "..." → Repositorios personalizados
      - Repositorio: `https://github.com/AuroreVgn/somfy-protexial`
      - Categoría: `Integración`
3. Descargue la integración.
   - HACS → Integraciones → Somfy Protexial → Descargar
4. Reinicie Home Assistant.

### Opción B: Instalación manual

1. Descargue el archivo de la última versión disponible: [somfy_protexial.zip](https://github.com/AuroreVgn/somfy-protexial/archive/refs/tags/2.0.11.zip)
2. Localice el directorio que contiene el archivo `configuration.yaml` de su instalación de Home Assistant.
3. Si no existe el directorio `custom_components`, créelo.
4. Cree un directorio `somfy_protexial` dentro de `custom_components`.
5. Extraiga el contenido de `somfy_protexial.zip` en el directorio `somfy_protexial`.
6. Reinicie Home Assistant.

## Configuración

- Añada la integración utilizando [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=somfy_protexial) o manualmente.
- Ajustes → Dispositivos y servicios → + Añadir integración → Somfy Protexial

### 1. Dirección de la central de alarma

- Introduzca la URL de la interfaz web local de su central:
  `http://192.168.1.234` o `http://192.168.1.234:9876`

</br>

<img src="assets/welcome.png" width="50%"><img src="assets/login_io.jpeg" width="50%">

### 2. Credenciales del usuario

- Usuario: `"u"` (**mantenga el valor predefinido**)
- Contraseña: Introduzca la contraseña que utiliza habitualmente.
- Código de autenticación: Introduzca el código de la tarjeta de autenticación correspondiente al desafío solicitado.

<img src="assets/step2.png" width="50%">

### 3. Configuración adicional

Los distintos modos de armado utilizan las zonas configuradas en la central Somfy:

- Armado en ausencia (siempre disponible): zonas A+B+C
- Armado nocturno (opcional): cualquier combinación de A, B, C, A+B, B+C o A+C
- Armado en casa (opcional): cualquier combinación de A, B, C, A+B, B+C o A+C

**Código de armado/desarmado**

Si especifica un código, este se solicitará cada vez que arme o desarme la alarma.

**Intervalo de actualización**

Desde **15 segundos** hasta **1 hora**. El valor predeterminado es **60 segundos**.

No se recomienda utilizar un intervalo inferior, ya que la interfaz web de la central puede volverse inestable.

<img src="assets/step3.png" width="50%">

## Información adicional

### Tarjeta Lovelace para Home Assistant (estado y control)

Se ha desarrollado una [tarjeta Lovelace](https://github.com/developpeurbox/somfy-protexial-card) específicamente para esta integración.

### Tarjeta Mushroom Template (detalles de los dispositivos)

Hay disponible una plantilla de Home Assistant para mostrar cada dispositivo de la alarma junto con sus atributos (batería, comunicación, etc.) [aquí](https://github.com/AuroreVgn/somfy-protexial/blob/main/assets/Template%20Home%20Assistant).

<img width="485" height="127" alt="image" src="https://github.com/user-attachments/assets/d4f385c0-0171-4968-b369-c4cb86d8409e" />

### Compatibilidad de versiones

La lista de compatibilidad mostrada al principio de esta página **no es exhaustiva**. Es muy posible que esta integración sea compatible con otras versiones de las centrales Somfy. Si prueba otra versión con éxito, no dude en comunicármelo.

El año o la generación de la interfaz web de su central aparece en la parte inferior de las páginas:

<img src="assets/version.png" width="30%">

Algunas centrales también proporcionan su versión de firmware mediante la siguiente URL:

*http://192.168.1.234/cfg/vers*

o

*http://192.168.1.234:9876/cfg/vers*

### Uso de la interfaz web original

⚠️ **La central solo admite una sesión de usuario activa al mismo tiempo. Si desea utilizar la interfaz web original, deberá desactivar temporalmente esta integración.**

### Uso de la aplicación móvil oficial

⚠️ La aplicación oficial **Somfy Alarme** puede seguir utilizándose aunque la integración esté activa.

### Reconfiguración de la integración

La integración admite la reconfiguración completa directamente desde la interfaz gráfica de Home Assistant.

## ¡Las contribuciones son bienvenidas!

Si desea contribuir al proyecto, consulte las [Contribution guidelines](CONTRIBUTING.md).

## Créditos

Esta integración está basada en gran medida en el trabajo de [@Ludeeus](https://github.com/ludeeus) y en el proyecto [integration_blueprint][integration_blueprint].

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square
[license-shield]: https://img.shields.io/github/license/the8tre/somfy-protexial.svg?style=flat-square
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40the8tre-blue.svg?style=flat-square
[releases-shield]: https://img.shields.io/github/v/release/AuroreVgn/somfy-protexial.svg?style=flat-square
[releases]: https://github.com/AuroreVgn/somfy-protexial/releases
[user_profile]: https://github.com/AuroreVgn
