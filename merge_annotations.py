import xml.etree.ElementTree as ET
import os
import pandas as pd
from csv import reader


def generate_csv():
    row_list = []
    for file in os.listdir(os.getcwd()):
        if file.endswith(".xml"):
            tree = ET.parse(file)
            root = tree.getroot()
            for obj in root.findall('object'):
                row = {'Filename': root.find("filename").text,
                       'Directory': "/".join(list(root.find("path").text.split('/')[0:-1])),
                       'Camera': root.find("path").text.split('/')[-1].split('_')[0],
                       'Object Class': obj.find("name").text,
                       'x_min': obj.find("bndbox")[0].text,
                       'y_min': obj.find("bndbox")[1].text,
                       'x_max': obj.find("bndbox")[2].text,
                       'y_max': obj.find("bndbox")[3].text,
                       'Image Width': root.find("size")[0].text,
                       'Image Height': root.find("size")[1].text
                       }
                row_list.append(row)
    data_frame = pd.DataFrame(row_list)
    data_frame.to_csv("./fieldtest_annotations.csv", sep=',', index=False)


def generate_class_id(class_name):
    with open('detect_classes.txt') as f:
        for (i, line) in enumerate(f):
            if class_name in line:
                return i


def generate_text():
    with open('annotations_for_training.txt', 'w') as txt:
        with open('fieldtest_annotations.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            next(csv_reader)
            for row in csv_reader:
                line1 = row[1] + '/' + row[0] + " " + row[4] + "," + row[5] + "," + row[6] + "," + row[7] \
                        + "," + str(generate_class_id(row[3]))
                print(line1)
                txt.write(line1+"\n")


if __name__ == '__main__':
    generate_csv()
    generate_text()
