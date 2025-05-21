#!/bin/bash
cd /var/www/vhosts/fgtwelve.ltd/httpdocs/marketing
streamlit run app.py --server.port=8501 --server.baseUrlPath=/marketing --server.enableCORS=false