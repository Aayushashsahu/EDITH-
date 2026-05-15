#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# E.D.I.T.H. V8 — WSL Audio Fix
# Run if you have no sound or mic issues in WSL2
# bash scripts/fix_audio.sh
# ─────────────────────────────────────────────────────────────────────────────
G='\033[92m'; Y='\033[93m'; B='\033[0m'

printf "${Y}Fixing WSL2 audio...${B}\n"

# Install ALSA + PulseAudio
sudo apt-get install -y -q \
  alsa-utils \
  pulseaudio \
  libportaudio2 \
  libasound2-dev \
  ffmpeg \
  portaudio19-dev

# For WSLg (Windows 11 - usually works out of the box)
if [ -e /mnt/wslg ]; then
  printf "${G}WSLg detected — audio should work automatically.${B}\n"
  # Set ALSA to use the WSLg pulse backend
  mkdir -p ~/.config/pulse
  echo "default-server = unix:/mnt/wslg/PulseServer" > ~/.config/pulse/client.conf
  echo "autospawn = no" >> ~/.config/pulse/client.conf
  echo "daemon-binary = /bin/true" >> ~/.config/pulse/client.conf
  echo "enable-shm = false" >> ~/.config/pulse/client.conf
  printf "${G}✓ WSLg PulseAudio configured.${B}\n"
else
  # WSL2 without WSLg — manual PulseAudio TCP
  printf "${Y}Non-WSLg WSL2 detected.\n"
  printf "Install PulseAudio on Windows: https://www.freedesktop.org/wiki/Software/PulseAudio/Ports/Windows/${B}\n"
  grep -q "PULSE_SERVER" ~/.bashrc || echo 'export PULSE_SERVER=tcp:$(grep nameserver /etc/resolv.conf | awk "{print \$2}"):4713' >> ~/.bashrc
  printf "${G}✓ PULSE_SERVER added to ~/.bashrc${B}\n"
fi

printf "\n${G}Done. Restart your terminal and try: aplay /usr/share/sounds/alsa/Front_Left.wav${B}\n"
