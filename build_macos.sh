# !/bin/bash

# Clean
test -r dist/MailHelperGUI && rm -rf dist/MailHelperGUI
test -r dist/MailHelperGUI.app && rm -rf dist/MailHelperGUI.app

# Package .app
pyinstaller --windowed \
  --name "MailHelperGUI" \
  --icon="MailHelperGUI.icns" \
  --noconsole \
  main.py

# Fix .app
# https://github.com/pyinstaller/pyinstaller/issues/5154
mv dist/MailHelperGUI.app/Contents/MacOS/MailHelperGUI dist/MailHelperGUI.app/Contents/MacOS/MailHelperGUI.orig
echo "#!/bin/bash" >> dist/MailHelperGUI.app/Contents/MacOS/MailHelperGUI
echo "dir=\$(dirname \$0)" >> dist/MailHelperGUI.app/Contents/MacOS/MailHelperGUI
echo "open -a Terminal \"file://\${dir}/MailHelperGUI.orig\"" >> dist/MailHelperGUI.app/Contents/MacOS/MailHelperGUI
chmod +x dist/MailHelperGUI.app/Contents/MacOS/MailHelperGUI

# Create a DMG installer
mkdir -p dist/dmg
rm -r dist/dmg/*
create-dmg dist/MailHelperGUI.app dist/dmg
mv dist/dmg/MailHelperGUI*.dmg dist/dmg/MailHelperGUI.dmg