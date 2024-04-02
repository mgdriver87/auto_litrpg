from lib.misc.imgbb import upload_image
from lib.gen.sysmsg import generate_sysmsg_line
from lib.RPG.stats import Stats
from lib.misc.helper_functions import trim
from html2image import Html2Image
from PIL import Image, ImageChops
import os

base=os.path.dirname(os.path.abspath(__file__))
css = open(base + "\\lib\\gen\\templates\\css\\smythe.css", "r").read()
print(css)
tablestring = """MG404: [Title Obtained | Arcia Engraver (Basic) | Those scribbles look like they might blow up anytime soon. | +5 INT, +3 DEX, +10% chance at improving quality of final Arctech Equipment.]"""

hti = Html2Image(output_path=base)
output_string = generate_sysmsg_line(tablestring)
print(output_string)
#output_string = open(base +"\\lib\\gen\\templates\\html\\stat_table\\stat_table.html", "r").read()
hti.screenshot(html_str=output_string, css_str=css, save_as="test.png", size=(1200,1200))
im = Image.open("test.png")

im = im.convert('RGBA')
pixdata = im.load()

width, height = im.size
for y in range(height):
    for x in range(width):
        if pixdata[x, y] == (10, 10, 10, 255):
            pixdata[x, y] = (255, 255, 255, 0)

im = trim(im)
im.save("test2.png", "PNG")
#upload_image("Chapter-5-image2-jpg")