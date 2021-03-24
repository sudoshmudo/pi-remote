import os
import subprocess
import sys

from fastapi import APIRouter, FastAPI
import requests

OK = 'OK'

class Group:
    def __init__(self, tag):
        self.prefix = '/{}'.format(tag.lower())
        self.router = APIRouter()
        self.tags = [tag]
        
app = FastAPI()

fin = Group('Fin')
git = Group('Git')
kodi = Group('Kodi')
pi = Group('Pi')
raspotify = Group('Raspotify')
resilio = Group('Resilio')
services = Group('Services')
transmission = Group('Transmission')

groups = [fin, git, kodi, pi, raspotify, resilio, services, transmission]

def free_memory():
    os.system('echo 3 > /proc/sys/vm/drop_caches && swapoff -a && swapon -a')

@fin.router.get("/start")
async def fin_start():
    os.system("cd /root/git/fin && docker-compose start")
    return OK

@fin.router.get("/stop")
async def fin_stop():
    os.system("cd /root/git/fin && docker-compose stop")
    return OK
    
@git.router.get("/pull")
async def git_pull():
    os.system('cd /root/git/db-backup && git pull')
    os.system('cd /root/git/fin && git pull')
    os.system('cd /root/git/openapi-to-vcard && git pull')
    os.system('cd /root/git/pi-remote && git pull')
    return OK    
    
@kodi.router.get("/kill")
async def kodi_kill():
    os.system('pkill -9 kodi')
    return OK

@kodi.router.get("/quit")
async def kodi_quit():
    os.system('kodi-send --action="Quit"')
    return OK

@kodi.router.get("/start")
async def kodi_start():
    subprocess.Popen(["kodi"], start_new_session=True)
    return OK

@kodi.router.get("/update")
async def kodi_update():
    free_memory()
    os.system('kodi-send --action="UpdateLibrary(video)"')
    return OK

@pi.router.get("/free")
async def pi_free():
    free_memory()
    return OK

@pi.router.get("/shutdown")
async def pi_shutdown():
    os.system("shutdown -r now")
    return OK
    
@raspotify.router.get("/restart")
async def raspotify_restart():
    os.system("dietpi-services restart raspotify")
    return OK

@resilio.router.get("/start")
async def resilio_start():
    os.system("cd /root/Desktop/resilio && docker-compose start")
    return OK

@resilio.router.get("/stop")
async def resilio_stop():
    os.system("cd /root/Desktop/resilio && docker-compose stop")
    return OK

@services.router.get("/start")
async def services_start():
    os.system("dietpi-services start")
    return OK

@services.router.get("/stop")
async def services_stop():
    os.system("dietpi-services stop")
    return OK

@transmission.router.get("/start")
async def transmission_start():
    os.system("cd /root/Desktop/transmission && docker-compose start")
    return OK

@transmission.router.get("/stop")
async def transmission_stop():
    os.system("cd /root/Desktop/transmission && docker-compose stop")
    return OK

for group in groups:
    app.include_router(
        group.router,
        prefix=group.prefix,
        tags=group.tags,
    )
