import os
import matplotlib.pyplot as plt
import cv2

folder = "lab8"

#plot in subplots

lenght = len(os.listdir(folder))

fig, axs = plt.subplots(3, lenght//3)

i = 0
j = 0

for file in os.listdir(folder):
    if file.endswith(".png"):
        img = cv2.imread(os.path.join(folder, file))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        axs[i, j].imshow(img)
        axs[i, j].set_title(file)
        axs[i, j].axis('off')
        j += 1
        if j == lenght//3:
            i += 1
            j = 0
        
        
        
plt.show()