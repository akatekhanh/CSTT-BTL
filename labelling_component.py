# MATHEMATICAL FOUNDATION FOR COMPUTER SCIENCE (055263)_TRAN TUAN ANH
# CSTH-ABC: Labeling connected-component problem.
# Members:
    # Le Phuong Nam - 2170545
    # Ngo Quoc Khanh - 1812593
    # Lam Phung Phuoc Vinh - 2270093
    # Nguyen Quoc Anh - 2270074
# Import neccesery library
from PIL import Image, ImageOps
from traitlets import default
from numpy import *
import csv

#function to convert img to binary
def image_to_binary(img):
    col = img #read image 
    gray = col.convert('L')  #conversion to gray scale 
    bw = gray.point(lambda x: 0 if x<128 else 255, '1')  #binarization 
    return bw
# function to indicate index of element in list w condition
def find_indices(lst, condition):
    return [i for i, elem in enumerate(lst) if condition(elem)]

# Import binary image.
#path = "D:/Desktop/Document/XDATA/PracticePython/Learn/test_bw.png"
#img_orig = Image.open(path)
#label
tag = 0
#dictionary
dictionary = {}
#1. Reading the image , padding image and first passed

#-----------Using image to demo
#w, h = img_orig.size
# Padding image with border of 1
#image1 = ImageOps.pad(img_orig,(w+1,h+1))
#image_binary = image_to_binary(image1)
#im = asarray(image_binary, dtype = int)

#-------------Using a 9x17 matrix to demo
test_array = loadtxt('test.txt')
im =  test_array.astype(int)
w = 17
h = 9
#----------------------------
label = {}
#Create a new array to store pixel label
im_labelled = zeros(shape=(h,w)).astype(int)
with open('initial_array.txt', 'w') as f:
    csv.writer(f, delimiter=' ').writerows(im)
for row in range(0,h):
    for col in range(0, w):
        # Scan pixel if it is not equal to 0 (not background)
        if im[row,col] == 1:
            # Neighbours-4
            #neighbours = [im[row-1,col], im[row+1,col], im[row,col-1], im[row,col+1]]
            #neighbours_labelled = [im_labelled[row-1,col], im_labelled[row+1,col], im_labelled[row,col-1], im_labelled[row,col+1]]
            #neighbours-8
            neighbours = [im[row-1,col], im[row+1,col], im[row,col-1], im[row,col+1],im[row-1,col-1], im[row+1,col+1], im[row+1,col-1], im[row-1,col+1]]
            neighbours_labelled = [im_labelled[row-1,col], im_labelled[row+1,col], im_labelled[row,col-1], im_labelled[row,col+1],im_labelled[row-1,col-1], im_labelled[row+1,col+1], im_labelled[row+1,col-1], im_labelled[row-1,col+1]]
            #If all neighbours are not zero
            if neighbours.count(0) == 8:
                tag = tag + 1
                im_labelled[row,col] = tag
            #If there is only 1 neighbour is non-Zero
            elif neighbours.count(0) == 7:
                index =  find_indices(neighbours, lambda e: e != 0 ) #get index of non-zero n
                #Two pixel are connect, so label curren pixel as its neighbour's label
                if neighbours_labelled[index[0]] == 0:
                    tag = tag + 1
                    im_labelled[row,col] = tag
                else:
                    im_labelled[row,col] = neighbours_labelled[index[0]]
            #If there are more than 1 neighbour is non-zero - tricky part
            else:
                #There are 2 situations: all neighbours have the same label ; neighbours have different labels
                #Get non-zero index
                indices = find_indices(neighbours, lambda e: e != 0 ) 
                list(map(int, indices))
                # Get all label of current pixel's neighbours
                list_neighbours = []
                for i in indices:
                    list_neighbours.append(neighbours_labelled[i])
                same_label = True
                #Check if neightbours have labels.
                if  not any(list_neighbours):
                    tag = tag+1
                    im_labelled[row,col] = tag
                else:
                    l = min(list(filter(lambda a: a != 0, list_neighbours)))
                    #Check if all neighbours have same labels
                    for label in list_neighbours:
                        if l != label:
                            same_label = False
                    #Situation 1: Same label, label current pixel as same as its neighbour 
                    if same_label:
                        im_labelled[row,col] = l
                    #Situation 2: different labels, label current pixel as same as its neighbour.
                    else:
                        im_labelled[row,col] = l
                    # record equivalence classes
                        for i in indices:
                            temp1 = neighbours_labelled[i]
                            s = str(l)
                            if temp1 != l:
                                if s in dictionary:
                                # Get unique value with the key 's'
                                    dictionary[s] += str(temp1)
                                else: 
                                    dictionary[s] = str(temp1)
                            for key in dictionary:
                                dictionary[key] = list(filter(lambda a: a != '0', dictionary[key]))
                                dictionary[key] = list(set(dictionary[key]))
print(dictionary)
#----------------------------------------------2. Restructing hash map / dict
dictionary_restructed = dictionary
for key in dictionary:
    for key2 in dictionary:
        if key in dictionary.get(key2):
             dictionary_restructed[key2] += dictionary[key]
             dictionary_restructed[key] = 'null'
for key in dictionary_restructed:
    dictionary[key] = list(filter(lambda a: a != 'null', dictionary[key]))
print(dictionary_restructed)
#-----------------------------------------------3. Second pass.-----------------------------------
for row in range(0,h):
    for col in range(0, w):
        p = im_labelled[row,col]
        p_str = str(p)
        for key in dictionary:
            if p_str in dictionary.get(key):
            #Relabel all pixels have equivalence classes
                p_str = key
        q = int(p_str)
        im_labelled[row,col] = q
#Export file matrix
with open('labelled_array.txt', 'w') as f:
     csv.writer(f, delimiter=' ').writerows(im_labelled)
        
            

