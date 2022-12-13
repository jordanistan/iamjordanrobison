#!/bin/bash

set -eu

BASEURL="https://santa-staging.firebaseapp.com/"

# move to the root directory of santa-tracker-web
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAGING_ROOT="$ROOT/staging"
cd $ROOT/..

# build!
node ./release.js --baseurl=$BASEURL --minify=false

# move prod to GaE skeleton
rm -rf $STAGING_ROOT/appengine/prod
mv dist/prod $STAGING_ROOT/appengine/prod

# move static to firebase
# Note that when we deploy, we clobber the "old" deploy. People mucking with the staging site will
# be suddenly surprised when they can't load content!
mkdir -p $STAGING_ROOT/firebase/public
mv dist/_static/* $STAGING_ROOT/firebase/public
