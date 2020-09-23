from PIL import Image
img = Image.open("wall.png")

print(img.format, img.size, img.mode)

for i in range(0, 26):
	print(i)
	box = (i, 0, i + 1, 96)
	region = img.crop(box)
	region.save('pics/' + str(i) + '.png')
