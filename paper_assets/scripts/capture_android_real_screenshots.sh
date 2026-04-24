#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT:-/opt/homebrew/share/android-commandlinetools}"
ADB_BIN="$ANDROID_SDK_ROOT/platform-tools/adb"
APK_PATH="$ROOT_DIR/mobile-app/app/build/outputs/apk/debug/app-debug.apk"
OUTPUT_DIR="$ROOT_DIR/paper_assets/figures/android"

if [[ ! -x "$ADB_BIN" ]]; then
  echo "adb not found at $ADB_BIN" >&2
  exit 1
fi

if [[ ! -f "$APK_PATH" ]]; then
  echo "APK not found. Run ./gradlew :app:assembleDebug first." >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

"$ADB_BIN" wait-for-device
"$ADB_BIN" install -r "$APK_PATH" >/dev/null
"$ADB_BIN" shell settings put global window_animation_scale 0
"$ADB_BIN" shell settings put global transition_animation_scale 0
"$ADB_BIN" shell settings put global animator_duration_scale 0
"$ADB_BIN" shell am force-stop com.lxy.antiaddiction
"$ADB_BIN" shell am start -n com.lxy.antiaddiction/.ui.SplashActivity >/dev/null
sleep 4
"$ADB_BIN" exec-out screencap -p > "$OUTPUT_DIR/10_android_login_real.png"

"$ADB_BIN" shell input tap 540 956
sleep 6
"$ADB_BIN" exec-out screencap -p > "$OUTPUT_DIR/11_android_permission_real.png"

"$ADB_BIN" shell appops set com.lxy.antiaddiction GET_USAGE_STATS allow
"$ADB_BIN" shell input tap 540 718
sleep 6
"$ADB_BIN" exec-out screencap -p > "$OUTPUT_DIR/12_android_dashboard_real.png"

"$ADB_BIN" shell input tap 540 1318
sleep 4
"$ADB_BIN" exec-out screencap -p > "$OUTPUT_DIR/13_android_settings_real.png"

echo "Captured Android screenshots under $OUTPUT_DIR"
