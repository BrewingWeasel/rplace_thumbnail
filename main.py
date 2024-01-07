from PIL import Image, ImageColor, ImageDraw
import youtube
import update_thumbnail

SCALE = 10

def parse_goal(inp: str) -> tuple[tuple[int, int], str]:
    (position, color) = [f.strip() for f in inp.lower().split()]
    (x_pos, y_pos) = position.split(",")
    color_representation = color
    return ((int(x_pos), int(y_pos)), color_representation)

file_name = "/home/weasel/python/youtube_thumbnail/f.jpg"
img = Image.new('RGB', (1280, 720))
#img = Image.new('RGB', (100, 100))
img_draw = ImageDraw.Draw(img)

comments = youtube.retrieve_comments()

for comment in comments:
    print(comment)
    try:
        ((x, y), color) = parse_goal(comment)
        new_x, new_y = x * SCALE, y * SCALE
        shape = (new_x, new_y, new_x + SCALE, new_y + SCALE)
        img_draw.rectangle(shape, fill=ImageColor.getrgb(color), outline=None)
    except ValueError:
        print("invalid comment:", comment)
        continue

file_name = "/home/weasel/python/youtube_thumbnail/f.jpg"
img.save(file_name)

update_thumbnail.set_thumbnail(file_name)
