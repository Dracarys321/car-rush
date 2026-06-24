#!/usr/bin/env bash
# Build Car Rush for iOS (requires macOS with Xcode installed).
set -euo pipefail
cd "$(dirname "$0")"

if [[ "$(uname)" != "Darwin" ]]; then
  echo "iOS builds must run on a Mac with Xcode."
  echo "Use a Mac, or a macOS CI runner (e.g. GitHub Actions macos-latest)."
  exit 1
fi

if ! command -v buildozer >/dev/null 2>&1; then
  python3 -m pip install --user --upgrade pip buildozer
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "Building iOS app..."
buildozer ios debug

IPA_PATH=$(find bin -name '*.ipa' 2>/dev/null | head -n 1)
if [[ -n "$IPA_PATH" ]]; then
  echo ""
  echo "SUCCESS: $IPA_PATH"
  echo "Distribute via TestFlight or Apple Developer; itch.io cannot install iOS apps directly."
else
  echo "Check bin/ for the Xcode project (.app bundle)."
fi
