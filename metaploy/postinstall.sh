#!/bin/bash

cleanup() {
    echo "Container stopped. Removing nginx configuration."
    rm /etc/nginx/sites-enabled/gyft-api.metaploy.conf
}

trap 'cleanup' SIGQUIT SIGTERM SIGHUP

"${@}" &

cp ./gyft-api.metaploy.conf /etc/nginx/sites-enabled

wait $!