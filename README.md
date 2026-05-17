# CRUD Master - Microservices Movie Platform

A complete microservices-based application for managing a movie inventory and handling order processing. This project demonstrates synchronous HTTP communication and asynchronous message queuing (RabbitMQ) across an isolated virtualized infrastructure.

## 🚀 Architecture Overview

The system consists of three primary services running in separate Ubuntu VMs managed by Vagrant:

1.  **API Gateway (`gateway-vm`)**: The entry point. It proxies HTTP requests to the Inventory service and pushes order messages to RabbitMQ for the Billing service.
2.  **Inventory App (`inventory-vm`)**: A Flask REST API that manages a PostgreSQL database of movies.
3.  **Billing App (`billing-vm`)**: A hybrid service containing a background worker that processes RabbitMQ messages and a REST API to view order history, backed by its own PostgreSQL database.

## 🛠 Project Structure

```text
crud-master/
├── Vagrantfile             # Orchestrates the 3-VM setup
├── .env                    # Centralized environment configuration
├── scripts/                # Automated provisioning (Bash)
│   ├── provision_gateway.sh
│   ├── provision_inventory.sh
│   └── provision_billing.sh
├── srcs/
│   ├── api-gateway/        # Flask Reverse Proxy
│   ├── inventory-app/      # Movie CRUD Service (HTTP)
│   └── billing-app/        # Order Processing Service (RabbitMQ + HTTP)
└── resum.md                # Detailed billing & integration technical map
```

## ⚙️ Prerequisites

- **Vagrant** (v2.2+)
- **VirtualBox**
- **Terminal** (bash/zsh)

## 🏁 Getting Started

1.  **Clone the repository.**
2.  **Launch the infrastructure:**
    ```bash
    vagrant up
    ```
    *Note: This will take a few minutes while it installs PostgreSQL, RabbitMQ, and Python on all three VMs.*
3.  **Verify status:**
    ```bash
    vagrant status
    ```
    *All machines (gateway, inventory, billing) should be `running`.*

## 🧪 Testing the APIs

The **API Gateway** is exposed on your local machine at `http://localhost:5000`.

### 1. Movie Inventory (Synchronous HTTP)
- **Add a Movie:**
  ```bash
  curl -X POST http://localhost:5000/api/movies/ -H "Content-Type: application/json" -d '{"title": "Interstellar", "description": "Space exploration"}'
  ```
- **List Movies:**
  ```bash
  curl http://localhost:5000/api/movies/
  ```

### 2. Billing & Orders (Asynchronous RabbitMQ)
- **Place an Order:**
  ```bash
  curl -X POST http://localhost:5000/api/billing/ -H "Content-Type: application/json" -d '{"user_id": "123", "number_of_items": "2", "total_amount": "50.00"}'
  ```
  *(Gateway returns `202 Accepted` immediately as the message enters the queue).*
- **View Order History:**
  ```bash
  curl http://localhost:5000/api/orders/
  ```

## 🛡 Resilience & Process Management

All services are managed by **PM2** inside the VMs. 

### Testing System Resilience:
1.  Stop the billing service: `vagrant ssh billing -c "sudo -u vagrant pm2 stop billing-api"`
2.  Send an order: The order is successfully "Accepted" by the Gateway and held in RabbitMQ.
3.  Start the service: `vagrant ssh billing -c "sudo -u vagrant pm2 start billing-api"`
4.  The order is processed automatically as soon as the service recovers.

## 🧹 Maintenance

- **Stop VMs:** `vagrant halt`
- **Rebuild from scratch:** `vagrant destroy -f && vagrant up`
- **Check Logs:** `vagrant ssh <vm_name> -c "sudo -u vagrant pm2 logs"`
