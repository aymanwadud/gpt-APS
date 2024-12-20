#!/bin/bash

echo "Updating SQLite to version 3.35.0+"

# Install prerequisites
sudo apt update
sudo apt install -y build-essential libsqlite3-dev

# Download and build SQLite 3.35.0+
wget https://www.sqlite.org/2024/sqlite-autoconf-3420000.tar.gz
tar -xzf sqlite-autoconf-3420000.tar.gz
cd sqlite-autoconf-3420000
./configure
make
sudo make install

# Verify the version
sqlite3 --version
