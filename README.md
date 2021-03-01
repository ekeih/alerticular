# Alerticular

[![Docker Repository on Quay](https://quay.io/repository/ekeih/alerticular/status "Docker Repository on Quay")](https://quay.io/repository/ekeih/alerticular)

Alerticular is the bridge between your infrastructure and your notification target. What does that mean? Well, Alerticular receives a message and sends it somewhere else. For now it supports [Prometheus Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) as input and [Telegram](https://telegram.org/) as output.

So whenever Prometheus triggers an alert you can use Alerticular to receive a Telegram message. (In the future Alerticular might support more platforms, e.g. receiving messages from [kubewatch](https://github.com/bitnami-labs/kubewatch).)

Alerticular is developed with a focus on Kubernetes. There shouldn't be an issue runnig it in another way, but some examples may assume that it is used in a Kubernetes cluster with Alertmanager running in the same cluster.

## Installation

Alerticular is written in Python, so in general every _Python way_ of installing software should work.

### Pip

Pip is best used inside of a [virtualenv](https://docs.python.org/3/tutorial/venv.html).

```
git clone git@github.com:ekeih/alerticular.git
cd alerticular
pip install poetry
poetry install
alerticular --bot-token $TOKEN
```

### Docker

```
docker run --rm --env ALERTICULAR_BOT_TOKEN="$TOKEN" quay.io/ekeih/alerticular
```

### Kubernetes / Helm

```
# Create a new namespace
kubectl create namespace alerticular

# Create secret with the Telegram token
kubectl -n alerticular create secret generic alerticular --from-literal="token=$TOKEN"

# Install Alerticular using the Helm chart
git clone git@github.com:ekeih/alerticular.git
cd alerticular
helm upgrade --install alerticular ./charts/alerticular`
```

Please check the [values.yaml](./charts/alerticular/values.yaml) for all available chart options.

## Configure Telegram

1. Talk to the [BotFather](https://t.me/BotFather) via Telegram.
2. Send `/newbot` and follow the instructions. For details check out the official [bot documentation](https://core.telegram.org/bots#3-how-do-i-create-a-bot).
3. Copy the bot token.
4. Start Alerticular and pass the token
   - either as command line parameter `alerticular --bot-token $TOKEN`
   - or as environment variable `ALERTICULAR_BOT_TOKEN="$TOKEN"`
5. Figure out the chat ID by
   - either starting a conversation with the bot by sending `/start`
   - or talking to the bot (or inviting it to a group/channel) and then fetching the updates manually from the Telegram API
     ```
     curl -s https://api.telegram.org/bot$TOKEN/getUpdates | jq '.result | .[].message.chat.id'
     12345678
     ```
6. Copy the chat ID for later.

## Configure Alertmanager

Please refer to the [upstream documentation](https://prometheus.io/docs/alerting/latest/configuration) for a full reference of the available Alertmanager options. Alertmanager is able to call a webhook to send alerts and Alerticular is able to receive, parse and forward those. Alerticular supports [a few different URL formats to receive messages](./alerticular/webhook.py#L41). The most verbose format is `http://host:8080/from/{source}/to/{chat}/on/{target}`, so to send an Alertmanager alert to a Telegram user with the chat ID 12345678 the URL would be `https://alerticular.alerticular:8080/from/alertmanager/to/12345678/on/telegram` (assuming Alerticular is running in Kubernetes cluster in a namespace called `alerticular`). In Alertmanager the configuration could look like this:

```
route:
  group_by: ["alertname"]
  receiver: "telegramuser1"
  routes:
    - receiver: "telegramuser2"
      match:
        alertname: EmergencyAlert
receivers:
  - name: "telegramuser1"
    webhook_configs:
      - url: "http://alerticular.alerticular:8080/from/alertmanager/to/12345678/on/telegram"
  - name: "telegramuser2"
    webhook_configs:
      - url: "http://alerticular.alerticular:8080/from/alertmanager/to/87654321/on/telegram"
```

If the Telegram user has a username configured it is also possible to use the username instead of the chat ID in the URL.

## Templating

Alerticular ships with a default [Jinja2 template](./alerticular/templates/alertmanager.md) for the Telegram messages. To override the template it is currently necessary to override the file (e.g. by mounting a ConfigMap in Kubernetes) but soon an easier way to pass a custom template will be provided.

## Metrics

By default Alerticular exposes Prometheus metrics at port 8081, e.g. http://localhost:8081/metrics.
