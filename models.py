import os

from fastapi import APIRouter

import config

class Group:
    def __init__(self, name, icon_keyword=None):
        self.icon_path = os.path.join(config.ICONS_PATH, '{}.svg'.format(name.lower()))
        self.name = name
        self.prefix = '/{}'.format(name.lower())
        self.router = APIRouter()
        self.tags = [name]

        if (icon_keyword is not None):
            self.icon_keyword = icon_keyword
        else:
            self.icon_keyword = name

    def get_openapi_tag(self):
        return { 'name': self.name }