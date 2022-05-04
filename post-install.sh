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
##################################################################################################################
FILE=/usr/share/applications/google-chrome.desktop
if [ -f "$FILE" ]; then
if ! grep -qF 'google-chrome-stable --force-renderer-accessibility' /usr/share/applications/google-chrome.desktop; then
    echo "done"
    sudo sed -i s/"google-chrome-stable"/"google-chrome-stable --force-renderer-accessibility"/g /usr/share/applications/google-chrome.desktop
fi
else
    echo "Not Found"
fi
##################################################################################################################
FILE1=/usr/share/applications/firefox.desktop
if [ -f "$FILE1" ]; then
if ! grep -qF 'firefox --force-renderer-accessibility' /usr/share/applications/firefox.desktop; then
    echo "done"
    sudo sed -i s/"firefox"/"firefox --force-renderer-accessibility"/g /usr/share/applications/firefox.desktop
fi
else
    echo "Not Found"
fi
##################################################################################################################
FILE2=/usr/share/applications/chromium-browser.desktop
if [ -f "$FILE2" ]; then
if ! grep -qF 'chromium-browser --force-renderer-accessibility' /usr/share/applications/chromium-browser.desktop; then
    echo "done"
    sudo sed -i s/"chromium-browser"/"chromium-browser --force-renderer-accessibility"/g /usr/share/applications/chromium-browser.desktop
fi
else
    echo "Not Found"
fi
