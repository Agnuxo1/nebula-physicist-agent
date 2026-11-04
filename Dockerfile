# Project: Nebula Physicist Agent
# Author: Francisco Angulo de Lafuente
# ORCID: https://orcid.org/0009-0001-1634-7063
# Copyright (c) 2026 Francisco Angulo de Lafuente
# Attribution record: 2026-11-04

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV AGENT_ID=nebula-physicist-agi \
    AGENT_NAME="Nebula Physicist" \
    P2P_API_BASE=https://api-production-ff1b.up.railway.app

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

CMD ["python", "agent_physicist.py"]
