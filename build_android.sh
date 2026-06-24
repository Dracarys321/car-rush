#!/usr/bin/env bash
# Build Car Rush APK for Android (requires Linux or WSL on Windows).
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v buildozer >/dev/null 2>&1; then
  echo "Installing buildozer..."
  python3 -m pip install --user --upgrade pip buildozer cython
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "Installing Linux build dependencies (Ubuntu/Debian)..."
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y \
    git zip unzip openjdk-17-jdk python3-pip autoconf libtool \
    pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 \
    cmake libffi-dev libssl-dev
fi

echo "Building Android APK..."
buildozer -v android debug

APK_PATH=$(find bin -name '*.apk' | head -n 1)
if [[ -n "$APK_PATH" ]]; then
  echo ""
  echo "SUCCESS: $APK_PATH"
  echo "Upload this .apk to itch.io as the Android download."
else
  echo "Build finished but no APK was found in bin/"
  exit 1
fi
