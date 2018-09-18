#!/bin/sh

docker run -t -e GITHUB_TOKEN=$GITHUB_TOKEN \
    -v issuecounter_cache:/cachedir \
    -v $(pwd):/runctx joffrey/issuecounter \
    "$@"
