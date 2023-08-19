
#########################################################################################################

#   This is a small code for converting the Instances of Eglese into a structured table                 #
#   They are available, like many other instances, on this website                                      #
#   http://dimacs.rutgers.edu/programs/challenge/vrp/carp/ for evaluating CARP models.                  #
#   This convert a .dat instance into a .csv instance wich is readable from our instancereader in GAMS  #

#########################################################################################################

#   We first import the Pandas module.
#   We need this module to format our Table and to convert it into Cascading spreadsheet

import pandas as pd

# The data will be stored in this DataFrame

df = pd.DataFrame(columns=['-i-', '-j-', 'cost','demand'])

# Name of the file on the root

file_name = "egl-e1-B.dat"


with open(file_name,'r+') as file:
    for line in file:
        values = line.split()
        if values[0].startswith('VERTICES'):
            node_numb =  int(values[2][:])            # We store the number of Node for the next Step
        elif values[0].startswith('VEHICULOS'):
            veh_numb =  int(values[2][:])             # We store the number of Vehicle for the next Step
        elif values[0].startswith('CAPACIDAD'):
            capacity =  int(values[2][:])             # We store the capacity of the vehicle for the next Step
        elif values[0] == "(" and len(values) >0:     
            if len(values) > 5:
                values2 = [values[1][:-1], values[2][:-1], values[4], values[6]]

                df = df.append({'-i-': int(values2[0]),'-j-': int(values2[1]),'cost': float(values2[2]), 'demand': float(values2[3])},ignore_index=True)
            else :
                values2 = [values[1][:-1], values[2][:-1], values[4]]
                df = df.append({'-i-': int(values2[0]),'-j-': int(values2[1]),'cost': float(values2[2])},ignore_index=True)

file.close()

#   Convert DataFrame into csv file

df.to_csv(file_name[:-4]+'.csv')

#   We can now use this csv file as Input with our Instancereader in GAMS

print(df)
