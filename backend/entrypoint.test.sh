#!/bin/sh
poetry run wait-for
exec "$@"
