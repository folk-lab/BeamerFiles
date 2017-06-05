import re

######################### USER INPUTS #########################

doc_name = "top_gates_v1.DC2" # name of document to edit
new_name = "new top_gates_v1.DC2" # new name after edits
dose_file = "mesa_design_v2_PEC.LDT" # name of document with doses by layer

###############################################################

# converts file mapping layers to doses into list of doses
def dose_map(file):
    doc = open(file,'r') # opens the file in read mode
    doses = re.findall("\( \d+\, (.*?) \)", doc.read()) # finds occurrences of ( number, number )
                                                        # and extracts the second number
    for i in range(len(doses)):
        doses[i] = float(doses[i]) # converts the numbers into floats
    return doses

# fixes shape header lines
def swap(line, layer, doses, dose_max):
    line = line.split(" ") # separates line into list of numbers
    line[2] = "100" # replaces 3rd number with 100

    line[9] = str(255-round(255/(len(doses)-1) * layer)) # changes RGB values by layer: red goes from 255 to 0,
    line[10] = str(round(255/dose_max * doses[layer]))   # green is calculated from the layer's dose, and blue
    line[11] = str(round(255/(len(doses)-1) * layer))    # goes from 0 to 255

    line[12] = "0" # replaces 13th number with 0
    return " ".join(line) # convert list of numbers back to string

doses = dose_map(dose_file)
dose_max = max(doses) # finds max value in list of doses
regex = re.compile("\n21 \d+ ") # regular expression corresponding to start of layer lines
doc = open(doc_name,'r') # open file in read mode

layers = regex.split(doc.read()) # separate document into a list of layers
for i in range(1, len(layers)): # skips first element, which is the document header
    shapes = layers[i].split("\n") # makes list of lines in each layer
    for j in range(1,len(shapes)): # skips first element, which is the layer header
        if re.match("\d ", shapes[j]): # matches lines that begin with a one-digit number and a space
            shapes[j] = swap(shapes[j], i-1, doses, dose_max) # alters shape header line
                                                              # note: ith line is layer i-1
    shapes = "\r\n".join(shapes) # joins lines into string
    layers[i] = shapes # updates index in layer list

new_file = open(new_name,'w+') # make new file in write mode
new_file.write("\r\n21 0 ".join(layers)) # convert list of layers back to string
new_file.close()