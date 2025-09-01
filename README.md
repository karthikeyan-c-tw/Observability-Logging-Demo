# 📦 Message App Monitoring Demo

This project demonstrates a simple microservice architecture deployed on Kubernetes with observability using **Prometheus** and **Grafana**.

## 📚 Project Overview

The system consists of:

1. **Spring Boot Application** – A REST API service
2. **Python Job** – A scheduled job that calls the API
3. **Prometheus** – Metrics collector
4. **Grafana** – Visualization dashboard

All components are containerized, deployed to Kubernetes, and run within the same namespace.

---

## 🧩 Components

### 1. 🚀 Spring Boot Application (`spring-app`)

A minimal REST API written in Java using Spring Boot.  
It exposes an endpoint that returns a greeting message:

- **Endpoint:** `GET /message`
- **Input:** text message as path variable
- **Output:** A "Hello" message

The app also exposes **Prometheus metrics** at: `/actuator/prometheus`

> Metrics include HTTP request counts, durations, and health info.

---

### 2. 🐍 Volume Generator Job (`volume-generator`)

A Streamlit Python script that runs as a Kubernetes **Deployment** exposed on port 8501. It:

- Accepts a message and a count via a simple web UI
- On submission, it triggers the url multiple times until count is reached
- Generates synthetic traffic to demonstrate monitoring in Prometheus

---

### 3. 📡 Prometheus

[Prometheus](https://prometheus.io/) is configured to:

- Scrape metrics from the Spring Boot app
- Optionally scrape Kubernetes system metrics (API server, kubelets, etc.)
- Store time-series metrics for queries and alerting

Scrape interval: `15s`

---

### 4. 📊 Grafana

[Grafana](https://grafana.com/) is deployed with:

- Prometheus as the default data source
- Dashboards can be imported for:
    - Spring Boot metrics
    - Kubernetes CPU/memory usage
- Port-forwarded for local access via `localhost:3000`

---

## 🚀 Deployment Instructions

1. Create the Kubernetes namespace:

   ```bash
   kubectl create namespace message-app
   ```
2. Deploy the Spring Boot app, Prometheus, Grafana, and CronJob using provided YAML files.
3. Port-forward services to access them locally.
    
    ```bash
    #Spring App (if needed):
    kubectl port-forward svc/spring-app 7000:7000 -n message-app
   
   #Python Streamlit App:
    kubectl port-forward svc/volume-generator 8501:8501 -n message-app
    
    #Prometheus:
    kubectl port-forward svc/prometheus 9090:9090 -n message-app
    
    #Grafana:
    kubectl port-forward svc/grafana 3000:3000 -n message-app
    ```

