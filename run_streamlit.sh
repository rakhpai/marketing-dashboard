#!/bin/bash
cd /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing
streamlit run app.py --server.port=9005 --server.baseUrlPath=/marketing --server.enableCORS=false --server.enableWebsocketCompression=true --server.headless=true --server.address=0.0.0.0