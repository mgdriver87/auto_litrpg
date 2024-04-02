from lib.gen.sysmsg import generate_sysmsg_line
from lib.RPG.stats import Stats
from lib.misc.helper_functions import trim
from html2image import Html2Image
from PIL import Image, ImageChops
import os

persistent = Stats()
base=os.path.dirname(os.path.abspath(__file__))
css = open(base + "\\lib\\gen\\templates\\css\\smythe.css", "r").read()
print(css)
killstring = """MG404: [Item | Ancient Exosuit Spine | Lost technology created in the Galactic Era, unusable without thorough refurbishment. | Active Skill: Nerval Jack – Enables an exosuit pilot to wield a suit through a nerval distribution network. Requires an operational exosuit.]"""
#killstring ="""MG404: [ Level Up: 1 - 2 | All Stats Increased | Bonus Points Granted ] """
#killstring ="""MG404: [Title Obtained | Former Crime Lord | A bigshot in your previous life, so much for that, huh? | +10 INT, +10 CHA]"""

hti = Html2Image(output_path=base)
output_string = generate_sysmsg_line(killstring)
print(output_string)

#output_string = open(base +"\\lib\\gen\\templates\\html\\stat_table\\stat_table.html", "r").read()
hti.screenshot(html_str=output_string, css_str=css, save_as="test.png")
im = Image.open("test.png")
im = im.convert('RGBA')
pixdata = im.load()

width, height = im.size
for y in range(height):
    for x in range(width):
        if pixdata[x, y] == (10, 10, 10, 255):
            pixdata[x, y] = (255, 255, 255, 0)

im.save("test2.png", "PNG")



