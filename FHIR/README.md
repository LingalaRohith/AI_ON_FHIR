# AI on FHIR – Natural Language Patient Query System

This project enables users to query a patient dataset using natural language like:

> “Show me all diabetic patients over 50”

It parses the query using NLP, maps it to a FHIR-like patient query, and returns structured results (table + chart) in a clean web UI.

---

## Features

- Natural Language Query Parsing (spaCy)
- Simulated FHIR-compliant Patient API (FastAPI)
- Next.js Frontend with Live Search
- Pie Chart Visualization of Conditions
- Filter by Age and Condition
- Export Results (CSV, JSON)
- Full Docker Support (Frontend + Backend)

---

## Tech Stack

| Layer     | Tools                                      |
|-----------|---------------------------------------------|
| Frontend  | React, TypeScript, Next.js, Tailwind CSS    |
| Backend   | Python, FastAPI, spaCy                      |
| Charting  | Chart.js (via react-chartjs-2)              |
| Docker    | Docker, Docker Compose                      |

---

## Getting Started

### Run with Docker

```bash
git clone https://github.com/LingalaRohith/AI_ON_FHIR.git
cd FHIR
docker-compose up --build
