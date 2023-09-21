FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y nmap && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir python-libnmap==0.7.3 requests

COPY boefje.py /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/python3", "/usr/local/bin/boefje.py"]
