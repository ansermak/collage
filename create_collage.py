import os
from config import spacing, images_in_row
from PIL import Image

images = []
image_dir = os.getcwd() + "/images/"
os.chdir(image_dir)
result_width = 0
result_height = spacing


def get_sizes(images):
    global result_width, result_height

    height = min(im.size[1] for im in images)
    if result_width == 0:
        new_height = height % 100 + 200
        new_sizes = [(int(image.size[0] * new_height * 1.0 / image.size[1]),
                     new_height) for image in images]
        result_width = sum(size[0] for size in new_sizes)
    else:
        sizes = [(int(image.size[0] * 1.0 * height / image.size[1]),
                 int(image.size[1] * 1.0 * height / image.size[1]))
                 for image in images]
        ratio = result_width * 1.0 / sum(size[0] for size in sizes)

        new_sizes = [(int(size[0] * ratio), int(size[1] * ratio))
                     for size in sizes]
    result_height += new_sizes[0][1] + spacing
    return new_sizes


image_files = [image for image in os.listdir(image_dir)
               if os.path.isfile("{}{}".format(image_dir, image))]
for im_f in image_files:
    im = Image.open(im_f)
    images.append(im)

n = 0
new_sizes = []
while n < len(images):
    new_sizes += get_sizes(images[n:n+images_in_row])
    n += images_in_row


result_width += spacing * images_in_row

for n in range(len(images)):
    images[n] = images[n].resize(new_sizes[n])

image_result = Image.new('RGB', (result_width, result_height))
x = spacing
y = spacing
n = 0

for n in range(len(images)):
    image_result.paste(images[n], (x, y))
    if (n + 1) % images_in_row == 0:
        x = spacing
        y += images[n].size[1] + spacing
    else:
        x += images[n].size[0] + spacing


image_result.save("ready/collage.jpg")
