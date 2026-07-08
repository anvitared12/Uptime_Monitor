# Uptime Monitor

A simple **Uptime Monitoring MVP** built using **FastAPI**, **SQLite**, **SQLAlchemy**, **HTML**, **CSS**, and **Vanilla JavaScript**. The application periodically checks registered URLs, stores health check history, and displays the latest website status through a lightweight frontend.

---

# Repository Structure

```text
.
├── backend/
├── frontend/
└── docker-compose.yml
```

---

# AI Collaboration Log

This project was intentionally built as a step by step process so that each process i smonitored, rather than asking AI to generate the entire application.

## AI Tools Used

- GitHub Copilot
- OpenAI Codex

## Development Approach

Instead of generating the entire solution at once, I instructed the AI to act as a senior software engineer and mentor, guiding me through the project one step at a time.

The prompt emphasized:

- Explain **why** each component is needed.
- Explain **what** it does.
- Explain **how** it connects to the overall architecture.
- Generate only the code for the current step.
- Explain important functions.
- Explain what commands to run.
- Explain expected output.
- Wait for confirmation before moving to the next step.

This approach helped me understand the complete request flow:

```text
Browser
      │
      ▼
Frontend (HTML + JS)
      │
      ▼
FastAPI Backend
      │
      ▼
SQLite Database
      │
      ▼
Scheduler (APScheduler)
      │
      ▼
Website Ping
      │
      ▼
Health Check Storage
      │
      ▼
Frontend Status Updates
```

---

## Build Order

The project was developed incrementally in the following order:

1. Project structure
2. FastAPI setup
3. SQLite & SQLAlchemy
4. URL model
5. POST API
6. GET API
7. Frontend
8. Frontend ↔ Backend integration
9. Website ping implementation
10. Scheduler
11. Health Check table
12. Live status updates
13. Docker containerization

Each step was completed, tested, and verified before proceeding to the next.

---

## Dockerization

Once both the backend and frontend were functioning correctly, Docker support was added.
Prompt used:
> "For this project there is one task remaining: the entire environment must be orchestrated to spin up locally out-of-the-box with a single `docker compose up` command. Before generating code, explain each part."

For Docker-related issues, I primarily relied on:

- Docker Desktop
- Terminal error messages
- Incremental debugging

One issue encountered after containerization was a delay in updating the website health status. The frontend continued displaying an outdated "Last Checked" timestamp even after refreshing.

After reviewing the scheduler logs and frontend behavior, the issue was identified and corrected so that health checks update as expected.

---

# System Verification

The application has been verified end-to-end.

## Run the project

```bash
docker compose up
```

No additional setup is required.

---

## Features Verified

- Backend starts successfully
- Frontend loads correctly
- URL registration works
- Periodic health checks execute automatically
- Response time is stored
- HTTP status codes are stored
- Health check history persists in SQLite
- Frontend automatically displays updated website status
- Entire application runs through Docker Compose

---

# Screenshots

## Backend Running

<p align="center">
<img src="https://github.com/user-attachments/assets/8aca2d2d-7936-4a22-be39-91bbc6ef0531" width="900">
</p>

---

## Docker Containers

<p align="center">
<img src="https://github.com/user-attachments/assets/39c87180-6011-40e8-a58d-f39a3e4488c2" width="900">
</p>

---

## Frontend

<p align="center">
<img src="https://github.com/user-attachments/assets/89a39650-2ce1-428d-84f6-20347f15521b" width="900">
</p>

---

## Health Check Updates

<p align="center">
<img src="https://github.com/user-attachments/assets/6bd6dbc2-cfc6-4cc3-92aa-04c762fe3e37" width="900">
</p>

---

# Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- SQLite
- APScheduler
- httpx

### Frontend

- HTML
- CSS
- Vanilla JavaScript
- Fetch API

### Docker

- Docker
- Docker Compose

---

# Deployment Sketch (AWS)

## Cloud Architecture

For production deployment, I would host this application on **AWS** using an **EC2 instance**. The application is already containerized with Docker Compose, making it straightforward to deploy on a virtual machine.

```text
                Internet
                    │
                    ▼
          AWS Security Group
          (Allow HTTP:80, HTTPS:443)
                    │
                    ▼
              Amazon EC2
        Ubuntu + Docker + Docker Compose
                    │
      ┌─────────────┴─────────────┐
      │                           │
      ▼                           ▼
 FastAPI Backend            Frontend
   (Container)              (Container)
      │
      ▼
 SQLite Database
 (Docker Volume)
      │
      ▼
 APScheduler
 Periodically checks
 registered websites
```
## Breif Explaination of implementation
1. Launch an Amazon EC2 instance (Ubuntu).
2. Install:
   - Docker
   - Docker Compose
3. Clone the GitHub repository.
4. Run the application using:

```bash
docker compose up -d
```
5. Give a certain port.
6. And then generate a public ip.
