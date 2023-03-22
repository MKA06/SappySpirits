import random
import numpy as np
from PIL import Image
from collections import Counter
import json

# ##################################################################
classnum = 6
imgnum = 444
weights2 = np.array([
    [20, 20, 20, 20, 15, 5],  # class1
    [25, 20, 20, 20, 9, 6],  # class2
    [15, 25, 15, 5, 15, 25],  # class3
    [5, 10, 25, 25, 20, 15],  # class4
    [5, 10, 15, 30, 25, 15],  # class5
    [25, 5, 20, 15, 25, 10],  # class
])
# #################################################################
description = "A free, peaceful and sappy spirit #{0}, just vibing."
ipfsc = "ipfs://"

def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros
# simple function to make a list of zeros


def percenterror(accepted, experimental):
    per_error = (abs(accepted - experimental) / accepted) * 100
    return per_error
# simple function to find percent error


def error(condition):
    if condition == 1:
        text = """
        #########################################################
        -- ErrorCode 1 --
        
        Rarity is lost
        
        Causes: 
            1: Random error
            2: Low number of output that cancels rarity
            
        Solutions: 
            1: rerun
            2: increase the number of output (imgnum)
        
        #########################################################

        """
        print(text)
        quit()


def generate():
    arr_img = list()
    classlist = list(range(1, classnum+1))
    comb = np.zeros(shape=(1, classnum))

    while len(arr_img) != imgnum:
        for i in range(classnum):
            ran = random.choices(classlist, weights=weights2[i])[0]
            comb[0, i] = ran
        comb_arr = comb.tolist()

        if comb_arr not in arr_img:
            arr_img.append(comb_arr)
        else:
            continue
    return arr_img
# creates an array of values by using initial weights


def combine(arr_img_t):

    for i in range(imgnum):
        imglist = list()
        comblist = zerolistmaker(6)
        for j in range(classnum):
            img = Image.open(fr"./classes/class{j+1}/class{j+1}_{int(arr_img_t[i][0][j])}.png")
            imglist.append(img)

        comblist[0] = Image.alpha_composite(imglist[0], imglist[1])

        for j in range(classnum-2):
            comblist[j+1] = Image.alpha_composite(comblist[j], imglist[j+2])
        comblist[4] = comblist[4].resize((1240, 1240), Image.NEAREST)
        comblist[4].save(fr"./images/SappySpirit-{i+1}.png")
# creates images according to given array of values.


def applied_rarity(arr_img_t):

    rarity_dict = list()
    for j in range(classnum):
        temp_class_list = list()
        for i in arr_img_t:
            temp_class_list.append(i[0][j])
        rarity_dict.append(Counter(temp_class_list))
    # rarity dict containing numbers of items

    for j in rarity_dict:
        for i in j:
            j[i] = round(((j[i] / imgnum) * 100), 0)
    # rarity dict values turned into percent

    for j in range(len(rarity_dict)):
        items = rarity_dict[j].items()
        rarity_dict[j] = sorted(items)
    # rarity dict sorted

    percent_list = list()
    for j in rarity_dict:
        values = list()
        for i in range(classnum):
            try:
                values.append(j[i][1])
            except:
                error(1)
        percent_list.append(values)
    percent_list_np = np.array(percent_list)
    # converts rarity dict values into a list for each class

    for i in range(len(percent_list)):
        percent_list[i] = [round(x) for x in percent_list[i]]
    # rounds percent list

    percent_difference_foreachitem = (np.round(percenterror(weights2, percent_list_np))).tolist()
    percent_difference_foreachclass = ((np.sum(percent_difference_foreachitem, axis=1)) / classnum).tolist()
    percent_difference_total = (sum(percent_difference_foreachclass)/6)
    # calculates percent differences for items, classes and total

    return percent_list, percent_difference_foreachitem, \
           percent_difference_foreachclass, percent_difference_total
# returns the percentage errors and applied weights of an array of values


def pricing(arr_img_t, pclist):
    coefficient_arr = [ [] for _ in range(imgnum) ]
    for i in range(len(arr_img_t)):
        price_val = 1
        for j in range(len(arr_img_t[i][0])):
            price_val = (pclist[j][int(arr_img_t[i][0][j]-1)]) / 10
        coefficient_arr[i].append(price_val)

    sumval = 0
    for i in coefficient_arr:
        for j in i:
            sumval = sumval +  j
    avgco = (sumval / imgnum)

    return coefficient_arr, avgco,


def writejson(path,filename,data):
    filepath  =  path + filename + ".json"
    with open(filepath, "w") as fp:
        json.dump(data, fp, indent=1)


background = ["background","blue", "green", "pink", "yellow", "layers of joy", "beauty of night"]
breed = ["breed" , "regular", "blueberryish" , "avocadoish", "cottoncandyish" , "smoke of the volcano", "shadow of the night"]
accessory = [ "accessory", "golden chain", "golden rosette", "tie", "scout sash", "name tag", "coal choker"]
mouthpiece = ["mouthpiece", "pipe", "cigar", "lipstick", "fangs", "haunted tongue", "gum"]
eyepiece = ["eyepiece","sunglasses", "3d glasses", "regular glasses", "blushes*", "eyeshadow", "scar"]
hat = ["headpiece" , "band", "crown", "cat ears", "horns", "doomer beanie", "haunted peppito hat"]
propertyvaluelist= [background, breed, accessory, mouthpiece, eyepiece, hat]

# create a list of 6 dictionaries with values of the class values and keys as numbers.

def metadataSelection(arr_img_t):
    propertyDictList = list()
    for i in range(classnum):
        propertyDict = dict()
        for j in range(classnum):
            propertyDict[j+1] = propertyvaluelist[i][j+1]
        propertyDictList.append(propertyDict)

    c= 0
    for object in arr_img_t:
        object = object[0]
        c += 1
        proplist = list()
        for classnumber in range(len(object)):
            proplist.append(propertyDictList[classnumber][int(object[classnumber])])
        data = {
             "description": description.format(c),
             "image": f"{ipfsc}",
             "name": f"Sappy Spirit #{c}",
             "external_url": "http://sappyspiritsnft.com",
             "attributes": [
                 {
                     "trait_type": propertyvaluelist[0][0],
                     "value": proplist[0]
                 },
                 {
                     "trait_type": propertyvaluelist[1][0],
                     "value": proplist[1]
                 },
                 {
                     "trait_type": propertyvaluelist[2][0],
                     "value": proplist[2]
                 },
                 {
                     "trait_type": propertyvaluelist[3][0],
                     "value": proplist[3]
                 },
                 {
                     "trait_type": propertyvaluelist[4][0],
                     "value": proplist[4]
                 },
                 {
                     "trait_type": propertyvaluelist[5][0],
                     "value": proplist[5]
                 }
             ]
            }
        writejson(path="./jsonfiles/", filename=f"{c}", data=data)
    return propertyDictList

def run():
    print("""
    ################################################
    Running Program...
    
    """)

    print("#outputs :" , imgnum)
    print("#classes :", classnum)
    n = 1
    print("Generating .... \n")
    print("iteration " + str(n))
    arr_img= generate()
    combine(arr_img)
    plist, pdiff, pdiffc, ptotal = applied_rarity(arr_img)
    print("percent error: " , ptotal )
    coeffs, avcoeffs = pricing(arr_img, plist)
    metadataSelection(arr_img)
    print(plist)


    while ptotal > 11:
        print("optimizing percent error...\n")
        n += 1
        print("iteration " + str(n))
        arr_img= generate()
        combine(arr_img)
        plist, pdiff, pdiffc, ptotal = applied_rarity(arr_img)
        print("percent error: " , ptotal , "\n")
        coeffs, avcoeffs = pricing(arr_img, plist)
        metadataSelection(arr_img)
        print(plist)

    print("\nSuccesfully generated " + str(imgnum) + "  images\n")
    print("################################################")




run()