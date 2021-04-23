import base64
import io

from fastapi import FastAPI
from reportlab.graphics import renderPM
from starlette.responses import FileResponse
from svglib.svglib import svg2rlg

CARD = '''BEGIN:VCARD
VERSION:3.0
N:{}
TITLE:{}
LABEL;TYPE=HOME:{}
PHOTO;ENCODING=b;TYPE=image/png:{}
END:VCARD'''

FILENAME='response.vcf'
PNG_FORMAT='PNG'
ROUTE='/vcard'

class Vcard:
    def __init__(self, fastapi: FastAPI, base64_icons: dict):
        self.fastapi = fastapi
        self.base64_icons = base64_icons

        self.create_file()
        self.set_route()

    def create_file(self):
        with open(FILENAME, 'w') as f:
            f.write(''.join([CARD.format(route.name, route.path, list(route.methods)[0], self.get_icon(route.path)) for route in self.fastapi.router.routes if route.include_in_schema]))

    def get_icon(self, route_path):
        try:
            return self.base64_icons[route_path]
        except:
            return ''

    def set_route(self):
        self.fastapi.add_route(ROUTE, FileResponse(FILENAME), include_in_schema=False)

def svg_to_png_base64(path, scale, tranlsate, dpi, bg):
    drawing = svg2rlg(path)
    drawing.scale(scale, scale)
    drawing.translate(tranlsate, tranlsate)
    io_file = io.BytesIO()
    renderPM.drawToFile(drawing, io_file, dpi=dpi, fmt=PNG_FORMAT, bg=bg)
    return base64.b64encode(io_file.getvalue()).decode()