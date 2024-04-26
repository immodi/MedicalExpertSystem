@echo off
call venv\Scripts\activate
cd api && uvicorn app:app --reload  