#!/bin/bash
# install_ffmpeg.sh

# Przejście do katalogu domowego
cd ~

echo "Pobieranie statycznej kompilacji FFmpeg..."
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz

echo "Wypakowywanie archiwum..."
tar -xf ffmpeg-release-amd64-static.tar.xz

echo "Konfiguracja plików binarnych..."
mkdir -p ~/bin
mv ffmpeg-*-amd64-static/ffmpeg ~/bin/
mv ffmpeg-*-amd64-static/ffprobe ~/bin/

echo "Czyszczenie przestrzeni dyskowej..."
rm -rf ffmpeg-release-amd64-static.tar.xz ffmpeg-*-amd64-static

echo "Nadawanie uprawnień..."
chmod +x ~/bin/ffmpeg
chmod +x ~/bin/ffprobe

echo "Eksportowanie ścieżki środowiskowej..."
export PATH="$HOME/bin:$PATH"

echo "Weryfikacja instalacji:"
ffmpeg -version