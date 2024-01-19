#!/bin/sh
cd /home/ubuntu/stock-indicator-backend/
echo "Pulling Updates ************"
git pull
echo "Finished Pulling Updates ************"
echo "Restart Server ************"
sudo systemctl restart StockIndicatorAnalysis
echo "Finished Restart Server ************"
