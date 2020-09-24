# CovidFR-Influx

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Verbalinsurection_CovidFR-Influx&metric=alert_status)](https://sonarcloud.io/dashboard?id=Verbalinsurection_CovidFR-Influx)
[![CodeFactor](https://www.codefactor.io/repository/github/verbalinsurection/covidfr-influx/badge)](https://www.codefactor.io/repository/github/verbalinsurection/covidfr-influx)
[![Dependabot](https://badgen.net/dependabot/verbalinsurection/covidfr-influx?icon=dependabot)](DEPENDABOT)
[![Docker Hub package](https://img.shields.io/badge/images%20on-Docker%20Hub-blue.svg)](https://hub.docker.com/r/verbalinsurection/covidfr-influx)
[![GitHub](https://img.shields.io/github/license/Verbalinsurection/covidfr-influx)](LICENSE)

> En: Download, enrichment and load Covid-19 French data on Influx-Db with Grafana dashboard.

> Fr: Telecharger, enrichir et enregistrer les données concernant le Covid-19 pour la France dans une base Influx-Db représentées sur un dashboard Grafana.

![Image Overview](https://raw.githubusercontent.com/Verbalinsurection/CovidFR-Influx/main/dashboard/dash1.jpg)

# Data source
## Hospital data
- Santé Publique France (https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/)
    - Hospitalizations per day and per department
    - Resuscitation case per day and per department
    - Return home per day and per department
    - Death per day and per department

## Geographical center of French departments (city)
- Institut national de l'information géographique et forestière (http://www.ign.fr/publications-de-l-ign/Institut/Publications/IGN_Magazine/82/IGN_MAG_82.pdf#15)
    - City name

## City GPS coordinates
- Laposte (https://datanova.legroupe.laposte.fr/explore/dataset/laposte_hexasmal/information/?disjunctive.code_commune_insee&disjunctive.nom_de_la_commune&disjunctive.code_postal&disjunctive.libell_d_acheminement&disjunctive.ligne_5)
    - Latitude and longitude by city

# How to use
## Docker
`docker pull verbalinsurection/covidfr-influx`

## Environment variable
|variable|default|description|
|--|--|--|
|`CVFI_LOGLEVELCONSOLE`|20|Logging Levels (see below table)|
|`FILE_HOSP`|https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7|url to last hospital data file|
|`SCHEDULE`|19:15|Hour scheduled check for new data|
|`SCHEDULE_DELTA_M`|30|Duration in minute for waiting new data from schedule hour|
|`WAIT_NEW_M`|10|Wait between two check for new data|
|`INFLUX_HOST`||Influxdb host|
|`INFLUX_PORT`|8086|Influxdb port|
|`INFLUX_DB`|covidfr|Influxdb database name|
|`INFLUX_USER`||Influxdb use n ame|
|`INFLUX_PASS`||Influxdb user password|

### Logging Levels
|level|numerical value|
|--|--|
|`CRITICAL`|50|
|`ERROR`|40|
|`WARNING`|30|
|`INFO`|20|
|`DEBUG`|10|
|`NOTSET`|0|

# Various information
> For development, you can use vscode with the devcontainer in this repo

> Use GitFlow, so if you want to submit a PR, please use `develop` branch

> The new hospital data overwrite the old ones to take into account any corrections in the source file
