#!/bin/bash

if [ $(systemctl is-enabled wildfly.service) == "enabled" ]; then
  echo "systemd service 'wildfly.service' enabled. Starting wildfly.service."
  sudo systemctl start wildfly
else
  echo "systemd service 'wildfly.service' not enabled. Try to start manual."
  source wildfly.env
  ./service.sh stopApp
  ./service.sh stop
fi
echo "Done."
