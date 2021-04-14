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

    def asdict(self):
        return { 'name': self.tags[0] }

backup = Group('Backup')
fin = Group('Fin')
git = Group('Git')
kodi = Group('Kodi')
pi = Group('Pi')
raspotify = Group('Raspotify')
resilio = Group('Resilio')
services = Group('Services')

groups = [backup, fin, git, kodi, pi, raspotify, services]

app = FastAPI(openapi_tags=[group.asdict() for group in groups])

def free_memory():
    os.system('echo 3 > /proc/sys/vm/drop_caches && swapoff -a && swapon -a')

@backup.router.get("/execute")
async def backup_execute():
    os.system("cd /root/git/db-backup && python3.7 main.py")
    return OK

@backup.router.get("/restore")
async def backup_restore():
    os.system("cd /root/git/db-backup && python3.7 restore.py")
    return OK
    
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
    os.system('cd /root/git/forward-ports && git pull')
    os.system('cd /root/git/icons && git pull')
    os.system('cd /root/git/openapi-to-vcard && git pull')
    os.system('cd /root/git/pi-remote && git pull')
    return OK    
    
@kodi.router.get("/kill")
async def kodi_kill():
    os.system('pkill -9 kodi')
    return OK

@kodi.router.get("/pause")
async def kodi_pause():
    os.system('kodi-send --action="Pause"')
    return OK

@kodi.router.get("/quit")
async def kodi_quit():
    os.system('kodi-send --action="Quit"')
    return OK

@kodi.router.get("/start")
async def kodi_start():
    free_memory()
    subprocess.Popen(["kodi"], start_new_session=True)
    return OK

@kodi.router.get("/update")
async def kodi_update():
    free_memory()
    os.system('kodi-send --action="UpdateLibrary(video)"')
    return OK

@kodi.router.get("/zoom/in")
async def kodi_zoom_in():
    for _ in range(6):
        os.system('kodi-send --action="ZoomIn"')
    return OK

@kodi.router.get("/zoom/out")
async def kodi_zoom_out():
    for _ in range(6):
        os.system('kodi-send --action="ZoomOut"')
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

for group in groups:
    app.include_router(
        group.router,
        prefix=group.prefix,
        tags=group.tags,
    )
