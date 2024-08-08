#!/bin/sh

set -e  # exit if some command fails

envsubst < /etc/nginx/default.config.tpl > /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'  # run nginx in foreground to see logs on screen