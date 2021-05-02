import os

from dotenv import load_dotenv

load_dotenv()

HIDDEN_GROUPS = os.environ['HIDDEN_GROUPS'].split(',')
ICON_BACKGROUND = 0xe5e5ea
ICON_DEFAULT = 'default'
ICON_DPI = 150
ICON_EXTENSION = '.svg'
ICON_SCALE = 1.5
ICON_TRANSLATE = 9
ICONS_PATH = 'icons/'
ICONS8_PLATFORM = 'color'
ICONS8_TOKEN = os.environ['ICONS8_TOKEN']
