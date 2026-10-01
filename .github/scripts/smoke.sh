#!/bin/bash
set -x
mkdir -p smoke
adb install -r app/build/outputs/apk/debug/app-debug.apk 2>&1 | tee smoke/install.txt
adb logcat -c
adb shell am start -W -n fr.lanterne.d20/.MainActivity 2>&1 | tee smoke/start.txt
sleep 8
adb exec-out screencap -p > smoke/1_titre.png
# Nouvelle partie (bouton au centre-bas de l'écran)
adb shell input tap 540 1650; sleep 3
adb exec-out screencap -p > smoke/2_tap.png
adb shell pidof fr.lanterne.d20 > smoke/pid.txt || echo "PAS DE PROCESSUS" > smoke/pid.txt
adb logcat -d > smoke/logcat.txt
grep -A 40 "FATAL EXCEPTION" smoke/logcat.txt > smoke/crash.txt || echo "aucun crash" > smoke/crash.txt
echo "===== CRASH ====="; cat smoke/crash.txt
echo "===== PID ====="; cat smoke/pid.txt
echo "::notice title=Installation::$(tr '\n' ' ' < smoke/install.txt | tail -c 200)"
echo "::notice title=Processus::$(cat smoke/pid.txt)"
echo "::notice title=Crash::$(head -12 smoke/crash.txt | tr '\n' ' ' | tail -c 900)"
exit 0
