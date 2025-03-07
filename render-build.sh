#!/bin/bash
sudo apt-get update
sudo apt-get install -y cmake libopenblas-dev liblapack-dev libx11-dev
pip install -r requirements.txt
