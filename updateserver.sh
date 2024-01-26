#!/bin/sh
cd /home/ubuntu/stock-indicator-backend/
echo "Pulling Updates ************"
git pull
echo "Finished Pulling Updates ************"
echo "Restart Server ************"
sudo systemctl daemon-reload
sudo systemctl restart StockIndicatorAnalysis
echo "Finished Restart Server ************"
echo "Get Server Status ************"
sudo systemctl status my_service
echo "Finished Server Status ************"
