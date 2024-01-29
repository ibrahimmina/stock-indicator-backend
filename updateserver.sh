#!/bin/sh
cd /home/ubuntu/stock-indicator-backend/
echo "Pulling Updates ************"
git pull
echo "Finished Pulling Updates ************"
echo "Restart Server ************"
sudo sudo systemctl daemon-reload
sudo sudo systemctl restart StockIndicatorAnalysis
echo "Finished Restart Server ************"
echo "Get Server Status ************"
sudo sudo systemctl status StockIndicatorAnalysis
echo "Finished Server Status ************"
