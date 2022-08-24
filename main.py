# import the necessary packages
from PIL import Image
import cv2
import imutils
import math
import numpy as np
import imagehash as hsh
import timeit
import ntpath
from sys import argv
import os
import csv

# Timer of the script start
start_time = timeit.default_timer()

hashes_per_video = ()  # List of files and hashes
result_hashes = ()  # Result list of hashes lists


# Arguments
def read_source_folder(argument):
    return argument[1]


# Extract file name and file path
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail


# Get file path from Argument, custom function
source_path = read_source_folder(argv)
#   Build GUI to choose folder
#   root = tk.Tk()
#   root.withdraw()
#   source_path = filedialog.askdirectory()


# Get all files from the folder
source_video_files = os.listdir(source_path)
# print(source_video_files)  # Debug

# Write files to CSV with numbering, in order to prevent changes
file_num = 0
with open(source_path + '/List of Files.csv', 'w') as result:
    writer = csv.writer(result, delimiter=",")
    writer.writerow(('Number', 'FileName'))
    for row in source_video_files:
        if '.jpg' in row:
            file_num += 1
            row = str(file_num) + ',' + row
            columns = [c.strip() for c in row.strip(', ').split(',')]
            writer.writerow(columns)
        elif '.mp4' in row:
            file_num += 1
            row = str(file_num) + ',' + row
            columns = [c.strip() for c in row.strip(', ').split(',')]
            writer.writerow(columns)

# For source video files
for (root, dirs, file) in os.walk(source_path):
    for f in file:

        if ".DS_S" in f:
            continue
        if ".mp4" in f:
            # Prepare category name and create category
            jpg_category_name = f'{f[0:-4]}'
            if not os.path.exists(f'./jpg/{jpg_category_name}'):
                os.mkdir(f'./jpg/{jpg_category_name}')

            # Capturing the video from the given path
            cap = cv2.VideoCapture(source_path + '/' + f)
            frameRate = cap.get(5)  # frame rate
            print(f'FILE : {f} _FrameRate: ' + str(frameRate))

            # print(path_leaf(cap))
            # print(frameRate)  # debug red frame rate
            count = 0
            frameId = 1
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                if frameId % math.floor(frameRate) == 0:
                    frameId = cap.get(1)
                    # print(frameId) # DEBUG
                    filepath = f'./jpg/{jpg_category_name}/{f}_{count}.jpg'
                    count += 1
                    cv2.imwrite(filepath, frame)

                    # Read image and define high and width
                    img = cv2.imread(filepath)
                    h, w = int(img.shape[0]), int(img.shape[1])

                    # Resize image
                    w = w // 3
                    h = h // 3
                    resized_size = (w, h)
                    resized_img = cv2.resize(img, resized_size, interpolation=cv2.INTER_CUBIC)
                    cv2.imwrite(filepath,
                              cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)[int(h * 0.333):int(h * 0.666), 0:w]) # Write & convert to grayscale, speed up

                cv2.destroyAllWindows()
                frameId += 1
            cap.release()


batch_start_item = 0
print('batch_start_item : ' + str(batch_start_item))
batch_end_item = 0
print('batch_end_item : ' + str(batch_end_item))
hashes_per_batch = []  # Final hashes for searching batch
batch_length = 4
for (root, dirs, files) in os.walk('./jpg'):
    for _dir in dirs:
        path = './jpg/' + _dir  # Extract category name to build a path to file without _1 at the end
        sorted_list_jpg = sorted(next(os.walk(path))[2])
        # Filter Temp/hidden files
        filtered_obj_jpg = filter(lambda _dir: _dir != ".DS_Store", sorted_list_jpg)
        filtered_list_jpg = list(filtered_obj_jpg)
        # print('FILTER :' + str(list(filtered_list_jpg)[0:2]))
        sorted_list_len = len(list(filtered_list_jpg))
        print('LEN :' + str(sorted_list_len))
        start_item = sorted_list_len // 2 - batch_length // 2
        end_item = sorted_list_len // 2 + batch_length // 2
        # print(start_item)
        # print(end_item)
        batch_to_compare = list(filtered_list_jpg)[start_item:end_item]
        print('batch_to_compare ' + str(batch_to_compare))

        Build a XX length hash for image Batch
        for _file in batch_to_compare:

            img_path = path + '/' + _file
            print('img_path : ' + img_path)
            img = cv2.imread(img_path)
            im_pil = Image.fromarray(
                img)  # Takes the array object as the input and returns the image object made from the array object.

            hshperceptual = hsh.phash(im_pil, 20)
            # print('hshperceptual :' + str(hshperceptual))
            hashes_per_batch.append(hshperceptual)  # Tuple concatenation
            full_list_of_taga = '\n'.join(map(str, hashes_per_batch))  # Debug

            print(full_list_of_taga)

batch_start_item += batch_length
batch_end_item += batch_length





# For extracted pictures (JPG)


# DEBUG print(len(hashes_per_video))
# hshdiff = hashes_per_video[2] - hashes_per_video[2]
# print(str(hshdiff))

time = timeit.default_timer() - start_time

print(" ")
print("DONE ! Took: ", time)
