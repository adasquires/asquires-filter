"""

@author: adasquires

Script for filtering points from cells.xml based on proximity to other points.

"""

import xml.etree.ElementTree as ET
import time
from datetime import timedelta
import os.path
import sys


def create_filtered_lists(x, y, z, filter_size):
    #Zip through list of points and add to new filtered list if it isn't within a distance d of any other points within filtered lists.
    
    filtered_x, filtered_y, filtered_z = get_empty_lists(x, y, z)

    for p in range(len(x)):
        for i, j, k in zip(x[p], y[p], z[p]):
            add = True
            for l, m, n in zip(filtered_x[p], filtered_y[p], filtered_z[p]):
            
                if distance(i, j, k, l, m, n) < filter_size:
                    add = False
                    break
            
                else:
                    continue
                break
            
            if add:
                filtered_x[p].append(i)
                filtered_y[p].append(j)
                filtered_z[p].append(k)
            
    return filtered_x, filtered_y, filtered_z


def create_output_file(x, y, z, filter_size, filename):
    #Write new lists from filter function into new file.
    
    output_file_destination, output_filename = get_output_file(filename)
    output_filename = os.path.join(output_file_destination, output_filename)
    
    try:
        xml = open(output_filename, "w")
    except:
        print("Error in finding directory.")
        
    xml = open(output_filename, "w")
    xml.write('<?xml version="1.0" encoding="UTF-8"?>' + "\n")
    xml.write("<CellCounter_Marker_File>" + "\n")
    xml.write("  <Image_Properties>" + "\n")
    xml.write("    <Image_Filename>placeholder.tif</Image_Filename>" + "\n")
    xml.write("  </Image_Properties>" + "\n")
    xml.write("  <Marker_Data>" + "\n")
    xml.write("    <Current_Type>1</Current_Type>" + "\n")
    xml.write("    <Marker_Type>" + "\n")
    xml.write("      <Type>1</Type>" + "\n")
    
    for p in range(len(x)):
        for i, j, k in zip(x[p], y[p], z[p]):
            xml.write("      <Marker>" + "\n")
            xml.write("        <MarkerX>" + str(i) + "</MarkerX>" + "\n")
            xml.write("        <MarkerY>" + str(j) + "</MarkerY>" + "\n")
            xml.write("        <MarkerZ>" + str(k) + "</MarkerZ>" + "\n")
            xml.write("      </Marker>" + "\n")
            
    xml.write("    </Marker_Type>" + "\n")
    xml.write("  </Marker_Data>" + "\n")
    xml.write("</CellCounter_Marker_File>")
    
    return


def distance(x1, y1, z1, x2, y2, z2):
    #Calculate distance for filter function.
    
    return ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)**0.5


def get_output_file(filename):
    
    output_file_destination = filename.split("/cells.xml")[0]
    output_filename = "asquires-filtered-cells-f" + str(filter_size) + "-s" + str(split) + ".xml"
    
    return output_file_destination, output_filename


def get_empty_lists(x, y, z):
    
    empty_x = [[] for p in range(len(x))]
    empty_y = [[] for p in range(len(y))]
    empty_z = [[] for p in range(len(z))]
        
    return empty_x, empty_y, empty_z


def split_list(in_list, n=100):
    #Create a list of lists of length n.
    
    split_list = []
   
    for i in range(0, len(in_list), n):
        split_list.append(in_list[i:i+n])
        
    return split_list


for arg in sys.argv[1:]:

    try:
        name, value = arg.split('=',1)
    
    except:
        print("Error parsing.")

    if name.lower() == "--file":
        filename = value

    elif name.lower() == "--filter":
        # d in distance function to compare values. higher value, more filtering. 7–10 seems to work okay.
        filter_size = value
        
    elif name.lower() == "--split":
        # length of the lists used in split_list function. higher value, more precise filtering, but the script takes longer.
        split = value
        
    elif name.lower() == "--output-destination":
        output_file_destination = value
    
    
output_filename = get_output_file(filename)

    
tree = ET.parse(filename)
root = tree.getroot()
a = root.find("Marker_Data")
b = a.find("Marker_Type")

x_points = []
y_points = []
z_points = []

for i in b.findall("Marker"):
    x = int(i.find("MarkerX").text)
    y = int(i.find("MarkerY").text)
    z = int(i.find("MarkerZ").text)
    x_points.append(x)
    y_points.append(y)
    z_points.append(z)

x_points = split_list(x_points, int(split))
y_points = split_list(y_points, int(split))
z_points = split_list(z_points, int(split))
 
    
start = time.time()


filtered_x, filtered_y, filtered_z = create_filtered_lists(x_points, y_points, z_points, int(filter_size))


print("Writing new file...")


create_output_file(filtered_x, filtered_y, filtered_z, filter_size, filename)


count_x_points = 0
for i in x_points:
    for j in i:
        count_x_points += 1

count_x = 0
for i in filtered_x:
    for j in i:
        count_x += 1

filtered = count_x_points - count_x


print("Complete. {} filtered in {}.".format(filtered, timedelta(seconds=time.time() - start)))
