import pickle
from PIL import Image, ImageChops

def find_chapter_number(filename):
    print(int(filename.split("-")[-1].split(".")[0]))
    try:
        print(int(filename.split("-")[0].split(" ")[-2]))
        return int(filename.split("-")[0].split(" ")[-2])
    except:
        return 100000

def find_chapter_number_alt(filename):
    try:
        return int(filename.split("-")[-1].split(".")[0])
    except:
        return 100000

def load_file(chapter_name):
    # load latest pickle
    difference = 10000000
    starting_number = int(chapter_name.split("-")[0])
    min_file_name = ''
    for file in (os.listdir("storage")):
        if starting_number - int(file.split("_")[0]) < difference:
            difference = starting_number - int(file.split("_")[0]) 

    file_name = "storage/%s_stats.pickle" % (starting_number - difference)
    try:
        with open(file_name, 'rb') as file:
            persistant_stats = pickle.load(file) 
    except FileNotFoundError:
        print("pickle not found")
        return -1

    return persistant_stats

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def crop(image_filename):
    im = Image.open(image_filename)
    im = trim(im)
    im = im.convert('RGBA')
    pixdata = im.load()

    width, height = im.size
    for y in range(height):
        for x in range(width):
            # check for background color defined in css used.
            if pixdata[x, y] == (10, 10, 10, 255):
                pixdata[x, y] = (255, 255, 255, 0)

    im.save(image_filename, "PNG")

def save_file(stats, chapter_name):
    chapter_counter = int(chapter_name.split("-")[0])
    file_name = "storage/%s_stats.pickle" % chapter_counter
    with open(file_name, 'wb') as file:
        pickle.dump(stats, file) 
    print(file_name)
    print("PICKLE")
    return 0

def calculate_stats_based_on_message(stat_message):
    stats = [0,0,0,0,0,0,0,0]

    list_of_stat_increases = stat_message.split(",")
    for i in list_of_stat_increases:
        if i.find("STR") != -1:
            if i.find("-") != -1:
                stats[0] -= i.split("-").split(" ")[0]
            else:
                stats[0] += i.split("+").split(" ")[0]
            continue
        if i.find("DEX") != -1:
            if i.find("-") != -1:
                stats[1] -= i.split("-").split(" ")[0]
            else:
                stats[1] += i.split("+").split(" ")[0]
            continue
        if i.find("INT") != -1:
            if i.find("-") != -1:
                stats[2] -= i.split("-").split(" ")[0]
            else:
                stats[2] += i.split("+").split(" ")[0]
            continue
        if i.find("VIT") != -1:
            if i.find("-") != -1:
                stats[3] -= i.split("-").split(" ")[0]
            else:
                stats[3] += i.split("+").split(" ")[0]
            continue
        if i.find("CHA") != -1:
            if i.find("-") != -1:
                stats[4] -= i.split("-").split(" ")[0]
            else:
                stats[4] += i.split("+").split(" ")[0]
            continue
        if i.find("MAX HP") != -1:
            if i.find("-") != -1:
                stats[5] -= i.split("-").split(" ")[0]
            else:
                stats[5] += i.split("+").split(" ")[0]
            continue
        if i.find("MAX MP") != -1:
            if i.find("-") != -1:
                stats[6] -= i.split("-").split(" ")[0]
            else:
                stats[6] += i.split("+").split(" ")[0]
            continue
        if i.find("MAX STA") != -1:
            if i.find("-") != -1:
                stats[7] -= i.split("-").split(" ")[0]
            else:
                stats[7] += i.split("+").split(" ")[0]
            continue
    
    return stats