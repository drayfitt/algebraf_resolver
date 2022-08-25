import os
from PIL import Image

# prepare samples from algebraf backgrounds
alg_PATH = "../model/img_algebraf/"

directions = [
    (208, 66, 238, 96),
    (208, 153, 238, 183),
    (208, 241, 238, 271),
    (164, 109, 194, 139),
    (341, 109, 371, 139),
    (561, 109, 591, 139)
    ]

counter = 0

for image in os.listdir(alg_PATH):
    im = Image.open(alg_PATH + image)
    for direction in directions:
        im.crop(direction).save("../model/img_train/sign"+str(counter)+".png")
        counter += 1
        print("sign"+str(counter)+".png saved")
        
print("EOF")
