def fname_to_counts(fname_L_H):
    """
    fname_L_H:-List, A list of filename lists, called a high list. The filenames are those of the counts files from the 4D interperlation plot, the filenames are strings.
    returns: C_L_L- A list of count lists grouped by which graph they came from.

    This function take the string filenames of the count graphs for the 4D interperlation and modifies them to get the string value of the counts in the name and then turns that
    string value for counts into a float value for counts. The output is a list of a list of counts with each count list coming from a sperate plot.
    """
    C_L_L=[] # Count List List, A high list of filename lists
    for fname_L in fname_L_H: #Selects each filename list from the high list and sets it equal to fname_L
        C_L=[] # Count List, a list of count values form a single plot
        for fname in fname_L: # Selects each filename from the filename list
            C_Str=fname.split(' ')[2] #Count String, Splits the filename string and selcts the string count value and sets it equal to C_Str assuming that the filename follows the correct standard, Example filename: 'Graph 1 8.4 counts.csv'
            C_Num=float(C_Str) # Count Number, an float number of counts, Converts the Count String to a float number and sets it equal to Count Number
            C_L.append(C_Num) # Appends the current Count Number to the current Count List
        C_L_L.append(C_L) # Appends the current Count List to the Count List List
    return C_L_L # Returns the Count List List
Counts= fname_to_counts([['Graph 1 3.0 counts.csv','Graph 1 8.4 counts.csv','Graph 1 22 counts.csv'],['Graph 2 2.8 counts.csv','Graph 2 8.3 counts.csv','Graph 2 22 counts.csv'],['Graph 3 2.4 counts.csv','Graph 3 7.0 counts.csv','Graph 3 18 counts.csv','Graph 3 23 counts.csv','Graph 3 91 counts.csv'],['Graph 4 3.7 counts.csv','Graph 4 11 counts.csv','Graph 4 29 counts.csv','Graph 4 36 counts.csv','Graph 4 110 counts.csv']])
#print Counts
Counts_L_H=[[10,20,70,70],[20,20,70,100],[20,20,70,100],[20,20,70,70]]
Fluxes_10_Cnts_L=[4.49E-15,1.13E-15,2.81E-15,2.44E-15]

def Counts_To_Flux_Converter(C_L_H,F_K_L,C_K=10):
    """
    C_L_H:-List, Count List High, This is a list of count lists, each count list is the count list associated with the background used to calculate it, In each count list is a list of the minimum number of counts at which dectection probablity of an object is 90 Percent for each interpolated offaxis angel in order of increasing interpolated offaxis angle, For example, for the interpolated offaxis angles [1,3,4,9] the associated minimum number of counts is [12,17,31,61].
    C_K:-Float or Int,Counts Known, This is the number of counts for which the equivalent flux is known
    F_K_L:-List, Flux Known List, This is a high list of all the known fluxes for the known amount of counts Counts Known, grouped by what plot they are being associated with.
    n:-int the total number of count lists in the high list, Note: this will be replaced by len(C_L_H)

    This function takes the observered number of counts in the form of a high list and known amount of counts for a certain known flux, that known flux and the number of lists in the high list
    and returns a high list of the observered fluxes grouped by what plot they are associated with. The plots MIGHT be associated with the off-axis angle
    """
    F_U_L_H=[] # high list,Flux Unknown List High, A high list if the clacluated fluxes, grouped by the plots they came from
    #for i in range(0,n): # n, is the total number of plots? #Note: It is actually the total number of backgrounds but it does not matter because that is allways equal to len(C_L_H)
    for i in range(0,len(C_L_H)): # Indexes through each background
        F_U_L=[] # list,Flux Unknown List, an emtpy list that is to be filled with the observered (calculated) fluxes
        Cur_Counts_L=C_L_H[i] # List, Current Count List, This selects the each count list in the high count list
        #for j in range(0,4): # Note, the range might not go to 4 but instead an arbitary variable
        for j in range(0,len(Cur_Counts_L)): # Note, the range might not go to 4 but instead an arbitary variable Note: That "arbitary variable" is actually the amount of interpolated offaxis angles in a given Count list which is just equal to the number of counts in the count list which in turn is just equal to the len(Cur_Counts_L) and thus will be replaced by len(Cur_Counts_L)
            C=Cur_Counts_L[j] # C:-float, Counts, This selects the each count in the current count list
            F_K=Fluxes_10_Cnts_L[i] #This selects the current known flux associated with 10 counts
            F_U=F_K*(float(C)/C_K) # F_U:-float, Flux Unknown, This converts the current count value to the current flux value by assuming a linear relationship bewteen counts and flux, F_U is the calculated flux
            F_U_L.append(F_U) # This appends the current calculated flux to the Flux Unknown List (The list of calculated IE. observered fluxes)
        F_U_L_H.append(F_U_L) # This appends the current Flux Unknown List to the Flux Unknown High List
    return F_U_L_H # This returns the Flux Unknown High List

#print Counts_To_Flux_Converter(Counts_L_H,10,Fluxes_10_Cnts_L,4) # Note: This is a test
#print Counts_To_Flux_Converter(Counts,10,Fluxes_10_Cnts_L,4) # Note: There is an index error I need to figure out here, Why are the counts grouped wrong? Are the counts grouped wrong?
#print Counts_To_Flux_Converter(Counts_L_H,10,Fluxes_10_Cnts_L) # Note: This is a test #Note: The input of the function has changed from Counts_To_Flux_Converter(C_L_H,C_K,F_K_L) to Counts_To_Flux_Converter(C_L_H,F_K_L,C_K=10)
#Counts_L_H_2=[[12,17,31,61]] #From Detection_Probability_Calc_7.py using "D_P_C_Big_Input_90_Per_Check([0.0411256372949457],2,110,[1,3,4,9])" Note: Detection_Probability_Calc_7 is not outputing the high list yet, it is only printing the values which I manually copy and paste them, This will be fixed to output later
#Fluxes_10_Cnts_L_2=[7.633e-14] #From Known_Flux_Finder.py using Known_Flux_Finder('NGC2403','acisf02014_repro_evt2.fits','PIMMS_Data.csv') Note: Known_Flux_Finder.py is not outputing yet, it is only printing the value for the flux which I manually copy and paste, This will be fixed to output later
#print Counts_To_Flux_Converter(Counts_L_H_2,Fluxes_10_Cnts_L_2)
