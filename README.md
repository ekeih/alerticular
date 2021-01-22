# alerticular

[![Docker Repository on Quay](https://quay.io/repository/ekeih/alerticular/status "Docker Repository on Quay")](https://quay.io/repository/ekeih/alerticular)

## Kubernetes / Helm

- Create secret with your Telegram token: `kubectl create secret generic alerticular --from-literal='token=$TOKEN'`
- `helm upgrade --install alerticular ./alerticular/charts`

## Current state

- `pip install -e .`
- Start with `alerticular --bot-token $TOKEN`
- Metrics endpoint runs on `http://localhost:8081/metrics`
- Go to `http://localhost:8080/telegram/$CHAT_ID/spam` to send a message
