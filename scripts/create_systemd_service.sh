#!/bin/bash
cat << EOF > /etc/systemd/system/stockbot.service
[Unit]
Description=Stock Bot

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/Stock-bot
ExecStart=/usr/bin/python3 bot.py
Restart=always
RestartSec=10
KillMode=process
KeepAlive=on

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable stockbot.service