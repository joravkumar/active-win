#!/bin/bash

PROFILE="$(eval echo ~$USER)/.profile"

# Create a profile file if it does not exist
if [ ! -f "${PROFILE}" ] ; then
    touch "${PROFILE}"
    chown ${USER}:${USER} "${PROFILE}"
fi

# Enable accessibility for gnone session
if ! grep -qxF 'export ACCESSIBILITY_ENABLED=1' $PROFILE ; then
    echo 'export ACCESSIBILITY_ENABLED=1' >> ${PROFILE}
fi

if ! grep -qF 'google-chrome-stable --force-renderer-accessibility' /usr/share/applications/google-chrome.desktop; then
    sudo sed -i s/"google-chrome-stable"/"google-chrome-stable --force-renderer-accessibility"/g /usr/share/applications/google-chrome.desktop
fi
