import matplotlib.pyplot as plt
from IPython.display import Image
import os
import cv2
from sklearn.cluster import KMeans
from matplotlib.pyplot import imshow
import skimage
import numpy as np
from pathlib import Path
import configparser
import csv

def count(image):
    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    edges = cv2.Canny(img,25,250)
    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    img_name = image.split('/')[-1]

    output_folder = 'annotated/' + img_name
    output_filename = 'a_' + img_name

    path = Path(output_folder)
    path.mkdir(parents=True, exist_ok=True)
    plt.savefig(os.path.join(output_folder, output_filename), format='tif')

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    folder_path = config.get('ImageSettings', 'folder_path')
    file_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.tif'): 
            image_path = os.path.join(folder_path, filename)
            num_chroms = count(image_path)

            file_data.append({'filename': filename, 'num_chromosomes': num_chroms})

    
    csv_file_path = 'output.csv'

    with open(csv_file_path, 'w', newline='') as csv_file:
        fieldnames = ['filename', 'num_chromosomes']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        writer.writerows(file_data)



