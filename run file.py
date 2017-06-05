import re

######################### USER INPUTS #########################

doc_name = "top_gate_run.txt" # name of document to edit
new_name = "new top_gate_run.rf6" # new name after edits
dose_file = "mesa_design_v2_PEC.LDT" # name of document with doses by layer

dose_scale = 100 # scale factor applied to dosages in dose_file

###############################################################

# converts file mapping layers to doses into list of doses
def dose_map(file):
    doc = open(file,'r') # open file in read mode
    doses = re.findall("\( \d+\, (.*?) \)", doc.read()) # finds occurrences of ( number, number )
                                                        # and extracts the second number
    for i in range(len(doses)):
        doses[i] = float(doses[i]) # converts the numbers into floats
    return doses

# replaces old dosage with a new dosage
# fixes rounding error and calculates differently
def swap(line, layer, doses, dose_scale):
    line = line.split(" ") # separates line into list of numbers
    line[5] = str(round(doses[layer]*dose_scale,3)) # replaces 6th number (the dosage) with the corresponding
                                                    # dose for that layer times a scale factor
    return " ".join(line) # converts the list back to a string

doses = dose_map(dose_file)
regex = re.compile("\ncol ") # regular expression corresponding to the start of layer lines
doc = open(doc_name,'r') # open file in read mode

layers = regex.split(doc.read()) # separate document into a list of layers

for i in range(1,len(layers)): # skips first element, which is the document header
    layers[i] = swap(layers[i], i-1, doses, dose_scale) # applies new dosage
                                                        # note: ith line is layer i-1

new_file = open(new_name,'w+') # make new file in write mode
new_file.write("\ncol ".join(layers)) # convert list of layers back to string
new_file.close()