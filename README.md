API for bash scripts and commands.

## Getting Started

Install requirements, python, FastAPI and uvicorn.
```
pip3 install -r requirements.txt
```

Additional dependency, Image module:
```
apt-get install libopenjp2-7
```

## Running it as a service

```
nano /etc/systemd/system/pi-remote.service
```

```
[Unit]
Description=pi-remote API for bash scripts
After=network.target
[Service]
User=root
Group=root
WorkingDirectory=/root/git/pi-remote
ExecStart=uvicorn main:app --reload --port 5009 --host 0.0.0.0
[Install]
WantedBy=multi-user.target
```

```
systemctl enable pi-remote
systemctl start pi-remote
systemctl restart pi-remote
systemctl status pi-remote
```

## Why not Docker?

* some commands require root permissions, so bare-metal code seems more appropriate
* the service works even when killing all dietpi services (including Docker)
* instant changes on code update
