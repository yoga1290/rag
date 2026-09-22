FROM python:3.12-slim-bookworm

EXPOSE 9273
EXPOSE 8000
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY . .

RUN apt-get update
RUN apt-get install -y gcc build-essential

# SEE https://docs.influxdata.com/telegraf/v1/install/#download-and-install-telegraf
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl --silent --fail --location \
        -o /tmp/influxdata-archive.key \
        https://repos.influxdata.com/influxdata-archive.key \
    && gpg --dearmor \
        -o /etc/apt/keyrings/influxdata-archive.gpg \
        /tmp/influxdata-archive.key \
    && echo "deb [signed-by=/etc/apt/keyrings/influxdata-archive.gpg] https://repos.influxdata.com/debian stable main" \
        > /etc/apt/sources.list.d/influxdata.list \
    && rm /tmp/influxdata-archive.key \
    && apt-get update \
    && apt-get install -y --no-install-recommends telegraf \
    && rm -rf /var/lib/apt/lists/*

# System dependencies + Telegraf
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        telegraf \
        curl \
        procps \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

RUN chmod +x entrypoint.sh
CMD ["entrypoint.sh"]