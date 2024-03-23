#!/bin/sh
source venvtest/bin/activate
export $(grep -v '^#' .env | xargs)
echo $api_key
python3 -m unittest swagger_server/test/test_general_stock_info_controller.py
