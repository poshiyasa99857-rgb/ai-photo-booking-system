#!/bin/bash
# 定时任务执行脚本
# 可以添加到 crontab 或作为 Docker 的定时任务

cd /app

# 执行定时任务
python manage.py run_scheduled_tasks
