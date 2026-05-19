#!/bin/bash
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
