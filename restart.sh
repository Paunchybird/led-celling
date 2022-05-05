#!/bin/bash


sudo docker stop ceiling-led-panel
sudo docker rm ceiling-led-panel
sudo docker-compose build
sudo docker-compose up -d
