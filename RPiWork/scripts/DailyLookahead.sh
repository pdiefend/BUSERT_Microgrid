#! /bin/bash
cd /home/pi/BUSERT_Microgrid/RPiWork
DATE=`date +%Y-%m-%d`
/usr/local/bin/python3 DailyLookahead.py >> ~/datalogs/$DATE.txt
