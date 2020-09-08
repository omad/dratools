
# Monitoring using InfluxDB + Telegraf + Grafana

[Setup Telegraf, InfluxDb and Grafana in Docker.](https://medium.com/@musaib_khan/setup-telegraf-influxdb-and-grafana-in-docker-b1c6ac6bd523)

``` bash
docker volume create grafana-volume
docker volume create influxdb-volume
docker-compose -f docker-compose.yml up -d
```

## Setup Grafana
Login in Grafana by your-ip:3000/
Username: admin
Pass: admin

Add InfluxDB data source:
Basic Auth > user: telegraf & Pass: telegraf
InfluxDB: user: admin & Pass: Welcome123

Import Dashboard 1150 from grafana.com
Import Dashboard https://grafana.com/grafana/dashboards/11777

[Grafana Dashboards](https://grafana.com/grafana/dashboards/)

Install a dashboard using Grafana CLI
```bash
docker exec -i grafana sh -c 'grafana-cli plugins install raintank-worldping-app'
docker restart grafana

```

## Fancier Grafana

* [Visualising Latecy Variance with Grafana](https://hveem.no/visualizing-latency-variance-with-grafana)

https://www.martinvdm.nl/2020/05/08/docker-dashboard-with-grafana-telegraf-influxdb-and-viewed-in-home-assistant/




## Access InfluxDB directly

``` bash
docker exec -it influxdb sh
# influx
Connected to http://localhost:8086 version 1.8.0
InfluxDB shell version: 1.8.0


> use telegraf
Using database telegraf


> show measurements
> select * from snmp limit 5
```

