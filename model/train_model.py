import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron
from PIL import Image
import pickle

signs = ['add', 'div', 'multi', 'subs']
samples_PATH = "model/img_train/"
labels = []
dataset = []

# transform images to array
for sign in signs:
    print("Getting data for: ", sign)
    # iterate through each file in the folder
    for path in os.listdir(samples_PATH + sign):
        # add the image to the list of images
        image = np.asarray(Image.open(samples_PATH + sign + '/' + path).convert('RGB'))
        image = image.reshape(2700)
        dataset.append(image)
        labels.append(signs.index(sign))

# show random images
# index = np.random.randint(0, len(dataset) - 1, size= 20)
# plt.figure(figsize=(5,7))
#
# for i, ind in enumerate(index, 1):
#     img = dataset[ind].reshape((30, 30, 3))
#     lab = signs[labels[ind]]
#     plt.subplot(4, 5, i)
#     plt.title(lab)
#     plt.axis('off')
#     plt.imshow(img)

X = np.array(dataset)
y = np.array(labels)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

perceptron = Perceptron(max_iter=100, shuffle=True)
perceptron.fit(X_train, y_train)
print("Model score:", perceptron.score(X, y))

filename = 'finalized_model.sav'
pickle.dump(perceptron, open(filename, 'wb'))
print("Model saved: finalized_model.sav")
print("EOF")
