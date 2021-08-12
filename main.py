import os
import subprocess

from builder import Builder
from models import Group

OK = 'OK'

backup = Group('Backup')
git = Group('Git')
kodi = Group('Kodi')
pi = Group('Pi', 'raspberrypi')
raspotify = Group('Raspotify', 'spotify')
services = Group('Services')

groups = [backup, git, kodi, pi, raspotify, services]

@backup.router.get("/execute", name="Backup")
async def backup_execute():
    os.system("cd /root/git/db-backup && python3 main.py")
    return OK

@backup.router.get("/database/init", name="Database Init")
async def backup_database_init():
    os.system("cd /root/git/db-backup && python3 create.py")
    return OK

@backup.router.get("/restore", name="Backup Restore")
async def backup_restore():
    os.system("cd /root/git/db-backup && python3 restore.py")
    return OK
    
@git.router.get("/pull", name="Git Pull")
async def git_pull():
    os.system('cd /root/git/db-backup && git pull')
    os.system('cd /root/git/forward-ports && git pull')
    os.system('cd /root/git/pi-remote && git pull')
    return OK  

@kodi.router.get("/debug", name="Kodi Debug")
async def kodi_debug():
    os.system('kodi-send --action="PlayerDebug"')
    return OK

@kodi.router.get("/kill", name="Kodi Kill")
async def kodi_kill():
    os.system('pkill -9 kodi')
    return OK

@kodi.router.get("/pause", name="Kodi Pause")
async def kodi_pause():
    os.system('kodi-send --action="Pause"')
    return OK

@kodi.router.get("/quit", name="Kodi Quit")
async def kodi_quit():
    os.system('kodi-send --action="Quit"')
    return OK

@kodi.router.get("/start", name="Kodi Start")
async def kodi_start():
    subprocess.Popen(["kodi"], start_new_session=True)
    return OK

@kodi.router.get("/update", name="Kodi Update")
async def kodi_update():
    os.system('kodi-send --action="UpdateLibrary(video)"')
    os.system('kodi-send --action="CleanLibrary(video)"')
    return OK

@kodi.router.get("/zoom/in", name="Kodi Zoom In")
async def kodi_zoom_in():
    for _ in range(12):
        os.system('kodi-send --action="ZoomIn"')
    return OK

@kodi.router.get("/zoom/out", name="Kodi Zoom Out")
async def kodi_zoom_out():
    for _ in range(12):
        os.system('kodi-send --action="ZoomOut"')
    return OK

@pi.router.get("/free", name="Free memory")
async def pi_free():
    os.system('echo 3 > /proc/sys/vm/drop_caches && swapoff -a && swapon -a')
    return OK

@pi.router.get("/shutdown", name="Shutdown")
async def pi_shutdown():
    os.system("shutdown -r now")
    return OK
    
@raspotify.router.get("/restart", name="Raspotify Restart")
async def raspotify_restart():
    os.system("dietpi-services restart raspotify")
    return OK

@services.router.get("/start", name="Services Start")
async def services_start():
    os.system("dietpi-services start")
    return OK

@services.router.get("/stop", name="Services Stop")
async def services_stop():
    os.system("dietpi-services stop")
    return OK


app = Builder(groups).app
