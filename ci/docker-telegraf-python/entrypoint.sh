#!/bin/bash
set -e

# Start Telegraf in the background
telegraf --config /etc/telegraf/telegraf.conf &

# Start application
# exec python3 -m application