@echo off
call venv\Scripts\activate
pip install -r requirements.txt
pip install frozendict==2.3.0
python main.py
pause
