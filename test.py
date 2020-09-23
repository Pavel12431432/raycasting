from PIL import Image
from PIL import ImageEnhance
img = Image.open("wall.png")

print(img.format, img.size, img.mode)

'''for i in range(0, 260, 5):
	box = (i, 0, i + 5, 120)
	region = img.crop(box)
	region.save('pics/' + str(i / 5) + '.png')'''

box = (0, 0, 5, 120)
region = img.crop(box)
region.show()
region = region.resize((5, 60))
region.show()