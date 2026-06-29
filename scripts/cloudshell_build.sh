#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

sudo apt-get update
sudo apt-get install -y git zip unzip openjdk-17-jdk autoconf automake libtool pkg-config zlib1g-dev libffi-dev libssl-dev build-essential

python3 -m pip install --user --upgrade pip setuptools wheel
python3 -m pip install --user --upgrade buildozer cython virtualenv

export PATH="$HOME/.local/bin:$PATH"

buildozer -v android debug

ls -la bin
