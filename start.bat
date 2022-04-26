@echo off
python -m pip install -i http://mirrors.aliyun.com/pypi/simple --upgrade pip
python -m pip install -i http://mirrors.aliyun.com/pypi/simple -r requirements.txt
python webp2jpg.py
pause
