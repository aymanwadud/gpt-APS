#!/bin/bash

echo "Updating SQLite to version 3.35.0+"

# Install build tools and SQLite dependencies
sudo apt update
sudo apt install -y build-essential libsqlite3-dev wget

# Download and build the latest SQLite
wget https://www.sqlite.org/2024/sqlite-autoconf-3420000.tar.gz
tar -xzf sqlite-autoconf-3420000.tar.gz
cd sqlite-autoconf-3420000
./configure
make
sudo make install

# Verify SQLite version
sqlite3 --version

# Rebuild Python to link with the updated SQLite library
cd ..
pyenv install 3.12.0 --force
pyenv global 3.12.0
