#!/bin/bash
HOME=/home/gnv
AI_HOME=$HOME/AI
VENV=$AI_HOME/venv
PY=$VENV/bin/python
DIR=$AI_HOME/webscrape
URL="http://dl.22m22.ru/"
PROMPT="Получить список наименований файлов, которые можно скачать"
nohup $PY ./sgai2.py "$URL" "$PROMPT" &
