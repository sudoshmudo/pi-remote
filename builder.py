import os

from fastapi import FastAPI

import config
from fastapi_vcard import svg_to_png_base64, Vcard
from icons8 import Icons8Api
from models import Group

class Builder:
    def __init__(self, groups: [Group]):
        self.app = FastAPI(openapi_tags=[group.get_openapi_tag() for group in groups])
        self.base64_icons = {}
        self.groups = groups
        
        self.create_missing_icons()
        self.get_base64_icons()
        self.add_routers()

        Vcard(self.app, self.base64_icons)

    def add_routers(self):
        for group in self.groups:
            self.app.include_router(
                group.router,
                prefix=group.prefix,
                tags=group.tags,
            )

    def create_icon(self, group: Group):
        icons8_api = Icons8Api(config.ICONS8_TOKEN)
        try:
            icon_id = icons8_api.search(group.icon_keyword, config.ICONS8_PLATFORM)
            icon_svg = icons8_api.get(icon_id)
        except:
            with open(os.path.join(config.ICONS_PATH, '{}.svg'.format(config.ICON_DEFAULT)), 'r') as f:
                icon_svg = f.read()

        with open(group.icon_path, 'w') as f:
            f.write(icon_svg)

    def create_missing_icons(self):
        for group in self.groups:
            if not os.path.isfile(group.icon_path):
                self.create_icon(group)

    def get_base64_icons(self):
        for group in self.groups:
            paths = [group.prefix + route.path for route in group.router.routes]
            base64_icon = svg_to_png_base64(group.icon_path, config.ICON_SCALE, config.ICON_TRANSLATE, config.ICON_DPI, config.ICON_BACKGROUND)
            self.base64_icons.update({path: base64_icon for path in paths})
