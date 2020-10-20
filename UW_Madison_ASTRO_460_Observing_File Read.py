#NOTE: THIS SCRIPT CAN ONLY BE USED FOR .rad FILES THAT ONLY HAVE ONE OBSERVING FREQUENCY AND ONLY FOR ONE LOCATION

#import statements
import numpy as np

#parameters and initialization
full_spectra_range = 1.21875 #MHz
half_range = full_spectra_range/2
calibration = [] #where the calibration spectra will be stored
spectra = [] #All the spectra. This list contains lists which are the individual spectra
x_freq = [] #contains the frequencies for each measurement for the spectra

#User input prompts
year = str(input("What is the observing year? (yyyy):"))
file_path = r""
file_path += str(input("What is the full file path? (C:/users/<user>/Documents/filename.rad)"))
if file_path == " ":
    #for testing purposes
    file_path = r"/home/pigaral0298/Downloads/Pigarelli_29_15oct20.rad"
print("What mode? (0= keep in list variables for JupyterNotebooks, 1= Write to output files")
mode = int(input("If using a JupyterNotebook, you'll probably want to choose mode 0, if working as a script/in an IDE, you'll probably want to choose mode 1"))
if mode == 1:
    output_file_path = str(input("Where do you want to keep the output files? (specify folder path without end slash):"))
int_time = int(input("Integration time (s):"))
int_time_str = ":" + str(int_time)

#reading the data file and putting all data into lists
with open(file_path,'r') as infile:
    counter = 0
    trigger = 0
    t_sys_trigger = 0
    int_time_str_trigger = 0
    noisecal_trigger = 0
    t_sys_trigger = 0
    for line in infile:
        counter += 1
        if int_time_str in line:
            int_time_str_trigger = 1
        if "noisecal" in line:
            noisecal_trigger = 1
        if "freq" in line:
            line_list = line.strip().split()
            ind = line_list.index("freq")
            freq_index = ind+1
            frequency = float(line_list[freq_index])
            lower = frequency - half_range
            upper = frequency + half_range
            x_axis_frequencies = np.arange(start=lower,stop=upper,step=0.0078125)
            x_freq = x_axis_frequencies
        if line[:4] == year and trigger == 0 and noisecal_trigger == 1:
            trigger = 1
            line_list = line.strip().split()
            str_spec = line_list[-156:]
            for item in str_spec:
                calibration.append(float(item))
        if "tsys" in line:
            line_list = line.strip().split()
            print("Tsys =",str(line_list[2]))
            print("Calcons =",str(line_list[4]))
            print("Trecvr = ",str(line_list[6]))
            print("tload = ", str(line_list[8]))
            print("tspill =", str(line_list[10]))
            t_sys_trigger = 1
        if line[:4] == year and trigger == 1 and int_time_str_trigger == 1 and noisecal_trigger == 1 and t_sys_trigger == 1:
            specific_spec = []
            line_list = line.strip().split()
            str_spec = line_list[-156:]
            for item in str_spec:
                specific_spec.append(float(item))
            spectra.append(specific_spec)
infile.close()

#if user chooses, calibration, spectra, and x_freq can be written to files
#This block asks for a folder and outputs two types of documents: 1. Calibration file 2.Spectra files
#Both have the same format, a frequency followed by a space and then measured intensity and an end of line "\n"
#This block creates a new spectrum file for every spectrum included in the inital document
#Output ".dat" file works just the same as reading any other text file (use: open(filename,mode))        

last_calibration = calibration[-156:]

if mode == 1:
    num_files = len(spectra)
    c = output_file_path + "/calibration.dat"
    with open(c,'w') as outfile:
        for i in range(len(x_freq)):
            str_to_write = ""
            str_to_write += str(x_freq[i]) + " " + str(last_calibration[i]) + "\n"
            outfile.write(str_to_write)
    outfile.close()
    for j in range(num_files):
        s = output_file_path + "/spectra_" + str(j) + ".dat"
        with open(s,'w') as outfile:
            for k in range(len(x_freq)):
                str_to_write = ""
                str_to_write += str(x_freq[k]) + " " + str(spectra[j][k]) + "\n"
                outfile.write(str_to_write)
        outfile.close()
print("Done")
