import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import interp1d
import astropy.io.ascii as ascii
import os
from os import system
import glob
def Detection_Probability_Calc_3(B,C,OFF,fname_L_H=[['Graph 1 3.0 counts.csv','Graph 1 8.4 counts.csv','Graph 1 22 counts.csv'],['Graph 2 2.8 counts.csv','Graph 2 8.3 counts.csv','Graph 2 22 counts.csv'],['Graph 3 2.4 counts.csv','Graph 3 7.0 counts.csv','Graph 3 18 counts.csv','Graph 3 23 counts.csv','Graph 3 91 counts.csv'],['Graph 4 3.7 counts.csv','Graph 4 11 counts.csv','Graph 4 29 counts.csv','Graph 4 36 counts.csv','Graph 4 110 counts.csv']]):
    """
    fname_L_H:-hlist, Filename High List, a high list of the filenames of the files contianing the data from the 4D dectection probablity plot, The filenames must in in the form of 'Graph 1 3.0 counts.csv'
    B:-float, Background, The background of the observation
    C:-float, Counts, The amount of counts in an observation
    OFF:-float, Offaxis angle, The offaxis angle at which objects are trying to be detected
    Returns: P_Off_N:-float, Probablity as a function of Offaxis Number, The probablity of detecting an object given the background, number of counts and offaxis angle

    This funtion takes the names of datafiles contianing data
    """
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import interpolate
    from scipy.interpolate import interp1d
    import astropy.io.ascii as ascii
    import os
    from os import system
    """
    C_L=[] # Count List, A list of float count values
    P_L=[] # A list of the probabilities as a function of the background
    P_C_L=[] # P_C_L:-list, Probablity as a function of Counts List, The Probablity as a function of the user given background and user given count value in a list, with each value and the order of the list associated with a list of offaxis anlges Off_T_L=[0,2,5,10], Example The first probablity in the list is associated with 0'
    Off_L=[] # A list of graph numbers, ie. graph 1, graph 2, graph 3, graph 4
    Off_T_L=[0,2,5,10] # A list of the known offaxis angles in minutes in the order of the graphs associated with each graph number. For example Graph 1 = 0', Graph 2 = 2'
    for fname_L in fname_L_H:
        C_L=[] # Count List, A list of float count values
        P_L=[] # A list of the probabilities as a function of the background
        for fname in fname_L: # Selects each filename from the high filename list
            #data = ascii.read('/home/asantini/Desktop/Background_Graph_Data_2/' + str(fname)) # Reads in the data from the current filename's file
            dir = os.path.dirname(__file__)
            #filename= os.path.join(dir, '~','Desktop','SQL_Standard_File',)
            #filepath=os.path.abspath("~/Desktop/SQL_Standard_File")
            #print "Filepath =",filepath
            #path= os.path.join(dir,'~','Desktop','SQL_Standard_File',)
            #path=os.path.realpath('~/Desktop/SQL_Standard_File/SQL_Sandard_File.csv')
            path=os.path.realpath('../Background_Graph_Data_2/' + str(fname))
            #print "Path=",path
            #os.chdir(path)
            #os.chdir('~/Desktop/SQL_Standard_File/')
            #system('cd ~/Desktop/Big_Object_Regions/')
            #system('cd ../SQL_Standard_File/')
            #system('pwd')
            #system('ls')
            #data = ascii.read("SQL_Sandard_File.csv") #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
            #data = ascii.read(filename) #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
            #data = ascii.read(filepath) #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
            data = ascii.read(path) #data:-astropy.table.table.Table, data, The data from the SQL_Standard_File
            #data = ascii.read('~/asantini/Desktop/Background_Graph_Data_2/' + str(fname)) # Reads in the data from the current filename's file
            B_A=data['col1'] # B_A:-array, Background Array, The array contianing the background data from the current data file, in order of increasing background
            P_A=data['col2'] # P_A:-array, Probablity Array, The array of probabilities in the order of the increasing backgrounds they are associated with
            P_Check=False
            #print "B: ", B
            #print "B_A: ", B_A
            #print "P_A: ", P_A
            #print "len(B_A) is ", len(B_A)
            #print fname
            for i in range(0,len(B_A)-1): # Choses every background vaule in the background array Note:This might be wrong, NEED to FIX !!!
                #print "i is ", i
                B_S=B_A[i] # B_S:-numpy.float64, Background Small, The smaller background used to find the probablity to background slope
                B_Lg=B_A[i+1] # B_Lg:-numpy.float64, Background Large, The Larger background used to find the probablity to background slope
                #print "B_S is ", B_S
                #print "B_Lg is ",B_Lg
                #print "B: ", B
                #print B_A
                """
                This apoximates a linear relationship between any 2 points in a file (the fname file) and uses it to find a probablity as a function of background value inbetween the points
                """
                if((B>=B_S) and (B<=B_Lg)): # Checks to see if the input background is in between the Background Small value and the Background Large value
                    #print "Interpolation Conditions Satisfied"
                    slope=(P_A[i+1]-P_A[i])/(B_A[i+1]-B_A[i]) # slope:-numpy.float64, slope, Slope formula m=(y2-y1)/(x2-x1), given that y2=P_A[i+1]=Probablity Large, y1=P_A[i]=Probablity Small
                    P_B=(slope*(B-B_S))+P_A[i] #P_B:- Probablity as a function of Background, Solved Point Slope Formula y=m(x-x1)+y1
                    #print "P_B before is ", P_B
                    B_P=((P_B+(slope*B_S)-P_A[i]))/slope #B_P:-numpy.float64, Background as a function of Probablity, The inverse function of P_B
                    #print "The slope is ",slope
                    #print "i is ",i
                    #print "i+1 is ",i+1
                    #print "P_A[i+1] is ",P_A[i+1]
                    #print "P_A[i] is ",P_A[i]
                    #print "B_A[i+1] is ",B_A[i+1]
                    #print "B_A[i] is ", B_A[i]
                    #print "P_B is ",((P_B+(slope*B_S)-P_A[i]))/slope
                    #print B_S
                    #print B_Lg
                    #print "P_B is ", P_B
                    #print "B_P: ", B_P
                    P_L.append(P_B) #P_L:-list, Probablity List, appends the current Probablity as a function of Background onto the Probablity List
                    P_Check=True
                    #print "P_L is ", P_L
            #print "P_Check: ", P_Check #Checks to see if the observered input background is within the interpolation range of  the 4D Graph Data. If False then the observation input background is out of range
            if(P_Check==False):
                return False
            C_Str=fname.split(' ')[2] #C_Str:-str, Count String, The string value of the current count value, the filename is spilt inorder to get the string, the filename must be in the standard form 'Graph 2 8.3 counts'
            C_Num=float(C_Str) #C_Num:-float, Count Number, The float value of the current count
            C_L.append(C_Num) # Appends the current float count value to the count list
            #print P_Check
        #print "P_L : ", P_L
        #print "C_L : ", C_L
        #print "P_L Length : ",len(P_L)
        #print "C_L Length : ",len(C_L)
        P_C_f=interpolate.interp1d(C_L,P_L,bounds_error=0,fill_value=(float("NaN"),1.0)) #P_C_f:-scipy.interpolate.interpolate.interp1d, Probablity Count Function, This is a function that interpolates the probablity and count arrays and returns the probablity as a function of counts #Note: May have to remove bounds_error variable, it also might make the data for C=30 counts wrong
        #P_C_f=interpolate.interp1d(C_L,P_L,bounds_error=1,fill_value=(float("NaN"),1.0)) #P_C_f:-scipy.interpolate.interpolate.interp1d, Probablity Count Function, This is a function that interpolates the probablity and count arrays and returns the probablity as a function of counts #Note: May have to remove bounds_error variable, it also might make the data for C=30 counts wrong
        #print "P_C_f", type(P_C_f)
        #print "C : ", C
        P_C=P_C_f(C) #P_C:-numpy.ndarray, Probablity as a function of Counts, The probablity of making a dectection for a given amount of counts, Counts is not any count but the User chosen amount of counts
        P_C_Str=str(P_C) #P_C_Str:-str, Probablity as a function of Counts String, The string value Probablity as a function of Counts
        P_C_N=float(P_C_Str) #P_C_N:-float, Probablity as a function of Counts Number, The float value of the Probablity as a function of Counts
        for fname in fname_L: #Note: All the outputs for this should be the same offaxis angle
            Off_Str=fname.split(' ')[1] #Off_Str:-string, Offaxis String, The string value of the graph number associated with the offaxis angle for that current graph
            Off_N=int(Off_Str) #Off_N:-int, Offaxis Number, The integer value of the of graph number. #Note: Maybe this should be a float value
        Off=Off_T_L[Off_N-1]# Off:-int, Offaxis angle, The current offaxis anlge in minutes for the current filename list, fname_L
        Off_L.append(Off) #Off_L:-list, Offaxis List, A list of all offaxis angles used in the high filename list in minutes
        P_C_L=P_C_L+[P_C_N] # Adds the calculated probablity for the current offaxis anlge to the Probablity as a function of Counts List. #Note: For some reason P_C is an Array,
        #print "P_C_L", P_C_L
    #print Off_L
    #print P_C_L
    P_Off_f=interpolate.interp1d(Off_L,P_C_L) # P_Off_f:-'scipy.interpolate.interpolate.interp1d', Probablity Offaxis Function, This is a a function that interpolates the Probablity Count List and the Offaxis List and retruns the probablity as a function of offaxis anlge #May be effected by the fact the the offaxis anlge values are integers
    #print "P_Off_f", type(P_Off_f)
    P_Off=P_Off_f(OFF) # P_Off:-numpy.ndarray, Probablity as a function of Offaxis, The clacluated probablity of finding an object given the background, number of counts and offaxis angle
    #print "P_Off", type (P_Off)
    P_Off_Str=str(P_Off) #P_Off_Str:-str, Probablity as a function of Offaxis String, The string value of the probablity of finding an object
    P_Off_N=float(P_Off_Str) #P_Off_N:-float, Probablity as a function of Offaxis Number, The float value of the probablity of a finding an object
    """
    This clipping has been added in to test the plotting. More work needs to be done to dertermine if it will be completely included
    """
    if(P_Off_N>1.0):
        P_Off_N=1.0
    if(P_Off_N<0.0):
        P_Off_N=0.0
    return P_Off_N # Returns the probablity of finding an object

#Detection_Probability_Calc_3([['Graph 1 3.0 counts.csv','Graph 1 8.4 counts.csv','Graph 1 22 counts.csv'],['Graph 2 2.8 counts.csv','Graph 2 8.3 counts.csv','Graph 2 22 counts.csv'],['Graph 3 2.4 counts.csv','Graph 3 7.0 counts.csv','Graph 3 18 counts.csv','Graph 3 23 counts.csv','Graph 3 91 counts.csv'],['Graph 4 3.7 counts.csv','Graph 4 11 counts.csv','Graph 4 29 counts.csv','Graph 4 36 counts.csv','Graph 4 110 counts.csv']],0.153680013049534,10.0,7.5)
#print Detection_Probability_Calc_3([['Graph 1 3.0 counts.csv','Graph 1 8.4 counts.csv','Graph 1 22 counts.csv'],['Graph 2 2.8 counts.csv','Graph 2 8.3 counts.csv','Graph 2 22 counts.csv'],['Graph 3 2.4 counts.csv','Graph 3 7.0 counts.csv','Graph 3 18 counts.csv','Graph 3 23 counts.csv','Graph 3 91 counts.csv'],['Graph 4 3.7 counts.csv','Graph 4 11 counts.csv','Graph 4 29 counts.csv','Graph 4 36 counts.csv','Graph 4 110 counts.csv']],0.153680013049534,10.0,7.5)
#print Detection_Probability_Calc_3([['Graph 1 3.0 counts.csv','Graph 1 8.4 counts.csv','Graph 1 22 counts.csv'],['Graph 2 2.8 counts.csv','Graph 2 8.3 counts.csv','Graph 2 22 counts.csv'],['Graph 3 2.4 counts.csv','Graph 3 7.0 counts.csv','Graph 3 18 counts.csv','Graph 3 23 counts.csv','Graph 3 91 counts.csv'],['Graph 4 3.7 counts.csv','Graph 4 11 counts.csv','Graph 4 29 counts.csv','Graph 4 36 counts.csv','Graph 4 110 counts.csv']],0.03,10.0,5) #According to Kim et al. 2004 this should have a dection probablity of about 50% and the actual output is 53.8% which is consistant.
#print Detection_Probability_Calc_3(0.03,10.0,5) #According to Kim et al. 2004 this should have a dection probablity of about 50% and the actual output is 53.8% which is consistant.
#print Detection_Probability_Calc_3(0.1,4.0,0)
#print Detection_Probability_Calc_3(0.0005,22,0)
#print Detection_Probability_Calc_3(0.26,22,0)
#print Detection_Probability_Calc_3(0.3,22,0)

def D_P_C_Big_Input(Backgrounds,counts,Off_Angs):
    #counts=[10,20]
    #Off_Angs=[0,2,5,10]
    """
    Backgrounds:-list, Backgrounds, A list of float value backgrounds
    counts:-list, counts, A list of the float value counts
    Off_Angs:-list, Offaxis Angles, A list of interger value offaxis angles in minutes

    This function takes in multiple values for backgrounds counts and offaxis angles and runs Detection_Probability_Calc_3 on all combonations and prints the results
    """
    for Background in Backgrounds: # Background:-float, Background, The current background (of one of multiple observations?)
        Prob_L=[] # Prob_L:-list, Probablity List, A list of the probablity of detecting an object given the background, counts and offaxis angle
        print '\n'+str(Background)+'\n' # Prints the current background
        for count in counts: #count:-float, Count, The current count value, Selects the current count value from the count list
            Prob_L=[] # Prob_L:-list, Probablity List, A list of the probablity of detecting an object given the background, counts and offaxis angle
            #print "count", count #Debug
            for Off_Ang in Off_Angs: # Off_Ang:-int, Offaxis Angle, The current offaxis angle
                #print "Off_Ang", Off_Ang
                #Cur_P= Detection_Probability_Calc_3([['Graph 1 3.0 counts.csv','Graph 1 8.4 counts.csv','Graph 1 22 counts.csv'],['Graph 2 2.8 counts.csv','Graph 2 8.3 counts.csv','Graph 2 22 counts.csv'],['Graph 3 2.4 counts.csv','Graph 3 7.0 counts.csv','Graph 3 18 counts.csv','Graph 3 23 counts.csv','Graph 3 91 counts.csv'],['Graph 4 3.7 counts.csv','Graph 4 11 counts.csv','Graph 4 29 counts.csv','Graph 4 36 counts.csv','Graph 4 110 counts.csv']],Background,count,Off_Ang) #Calculates the probablity of a detection based on all the current values
                Cur_P= Detection_Probability_Calc_3(Background,count,Off_Ang) #Calculates the probablity of a detection based on all the current values
                Cur_P_Str=str(Cur_P) # Cur_P_Str:-str, Current Probablity String, The current probablity value as a string
                Cur_P_N=float(Cur_P_Str) # Cur_P_N:-float, Current Probablity Number, The current probablity value as a float
                Prob_L.append(Cur_P_N)
                #if(len(Cur_P_Str)==3): # For debugging, when not debugging Prob_L.append(Cur_P_N) allways
                    #Prob_L.append(Cur_P_N) # Appends the current probablity to the probablity list
            print count # prints the current counts value
            print Prob_L # Prints the current probablity list

#D_P_C_Big_Input([0.0411256372949457,0.135727335468768,0.13725522292245054,0.153680013049534],[10,20],[0,2,5,10])

#print "Next"

#Counts_L=[0,10,20,30,40,50,60,70,80,90,100,110,120,130]
#D_P_C_Big_Input([0.0411256372949457,0.135727335468768,0.13725522292245054,0.153680013049534],Counts_L,[10])
#D_P_C_Big_Input([0.0411256372949457,0.135727335468768,0.13725522292245054,0.153680013049534],Counts_L,[0,2,5,10])

def D_P_C_Big_Input_90_Per_Check(Backgrounds,Off_Angs=[0,1,2,3,4,5,6,7,8,9,10],C_Min=2,C_Max=110):
    """
    Backgrounds:-list, Backgrounds, A list of backgrounds (from seperate observations?) that the detection probablity will be clacluated.
    C_Min:-int, Count Minimum, The minimum amount of counts for an observation
    C_Max:-int, Count Maximum, The maximum amount of counts for an observation
    Off_Angs:-list, Offaxis Angle, A list of the offaxis angles at which an objects are being detected

    This function takes the multiple backgrounds, the minimum counts in a series of observations, the maximum counts in a series of observations, and the offaxis angle at which
    an object is being detected and prints the probabilities of detecting an object at all combonations of the variables(?) (The amount of counts need for P>0.90 for each background and offaxis angle(?))
    """
    #counts=[10,20]
    #Off_Angs=[0,2,5,10]
    Count_90_Per_First_L_H=[] #Count_90_Per_First_L_H:-hlist,Counts 90 Percent First High List The list of Count_90_Per_First_L lists for each background in Backgrounds, This is the ultimate desired output of this Module
    for Background in Backgrounds: # Background:-float, Background, The current background (of one of multiple observations?)
        Prob_L=[] # Prob_L:-list, Probablity List, A list of the probablity of detecting an object given the background, counts and offaxis angle
        Count_90_Per_L=[] # Count_90_Per_L:-list, Count 90 Percent List, A list of all count vaules that give a detection probablity greater than 90% given the background and offaxis
        #print '\n'+str(Background)+'\n' # Prints the current background
        Count_90_Per_First_L=[] #Count_90_Per_First_L:-list, Counts 90 Percent First List, The list of the minimum amount of counts need to obtain a 90% probablity of detection for a given offaxis angle for each interpolated offaxis angle in the order of the offaxis angles in the Off_Angs input list
        for Off_Ang in Off_Angs: # Off_Ang:-int, Offaxis Angle, The current offaxis angle
            Prob_L=[] # Prob_L:-list, Probablity List, A list of the probablity of detecting an object given the background, counts and offaxis angle
            Count_90_Per_L=[] # Count_90_Per_L:-list, Count 90 Percent List, A list of all count vaules that give a detection probablity greater than 90% given the background and offaxis
            #print '\n'+str(Off_Ang)+'\n'
            #counts.sort() # sorts the counts list from the lowest amount of counts to the highest amount of counts #Note: Modfied after summer, I don't know if this is right
            #for count in counts: #count:-float, Count, The current count value, Selects the current count value from the count list
            Step_L=[10,5,1] # Step_L:-list, Step List, The list of steps to take in the count range when calculating the 90% probabilities, steps decrease in size until it can pinpoint the exact amount of counts, Ex. 60 counts<70 counts<80 counts, to 60 counts <65 counts <70 counts, to 60 counts < 63 counts <65 counts
            Count_Min=C_Min # Count_Min:-int, Count Minimum, The minimum count value used in the count range, This sets the the lower limit in the count range back to the original lower limit
            Count_Max=C_Max # Count_Max:-int, Count Maximum, The maximum count value used in the count range, This sets the the upper limit in the count range back to the original upper limit
            for step in Step_L: # step:-int, Step, The current step vaule from the Step List in counts
                Count_90_Per_L=[] # Count_90_Per_L:-list, Count 90 Percent List, A list of all count vaules that give a detection probablity greater than 90% given the background and offaxis, Resets the list for every new step vaule
                for count in range(Count_Min,Count_Max+1,step): # This finds the minimum value of counts for which
                    #print '\n'+str(count)+'\n'
                    #print "Background: ", Background
                    #Cur_P= Detection_Probability_Calc_3([['Graph 1 3.0 counts.csv','Graph 1 8.4 counts.csv','Graph 1 22 counts.csv'],['Graph 2 2.8 counts.csv','Graph 2 8.3 counts.csv','Graph 2 22 counts.csv'],['Graph 3 2.4 counts.csv','Graph 3 7.0 counts.csv','Graph 3 18 counts.csv','Graph 3 23 counts.csv','Graph 3 91 counts.csv'],['Graph 4 3.7 counts.csv','Graph 4 11 counts.csv','Graph 4 29 counts.csv','Graph 4 36 counts.csv','Graph 4 110 counts.csv']],Background,count,Off_Ang) #Calculates the probablity of a detection based on all the current values
                    Cur_P= Detection_Probability_Calc_3(Background,count,Off_Ang) #Calculates the probablity of a detection based on all the current values
                    if(Cur_P==False):
                        return False
                    Cur_P_Str=str(Cur_P) # Cur_P_Str:-str, Current Probablity String, The current probablity value as a string
                    Cur_P_N=float(Cur_P_Str) # Cur_P_N:-float, Current Probablity Number, The current probablity value as a float
                    Prob_L.append(Cur_P_N) # Appends the current probablity to the probablity list
                    #print "Cur_P_N is ", Cur_P_N
                    if (Cur_P_N>=0.90): # Filters out all variable combonations that do not give a detection probablity of at least 90%
                        Count_90_Per_L.append(count) # Appends the current count vaule to the list of count vaules with a 90% probablity
                        Count_90_Per_First=Count_90_Per_L[0] # Count_90_Per_First:-float or int, Count 90 Percent First, The lowest amount of counts that are required to get a 90% detection probablity given the current background and current offaxis angle
                        Count_Max=Count_90_Per_First # Sets the upper limit for the count range to the lowest count value to give a detection probablity over 90%, this is faster then going throgh all counts
                        Count_Min=Count_Max-step # Sets the lower limit for the count range to one step value less then the maximum, The correct count value must be inbetween the Count_Min count value and the Count_Max count value
                        if(Count_Min<0): # This makes sure that the lower limit is allways positive, if it is negitive then it sets the lower limit to 0 counts
                            Count_Min=0 # This sets the lower limit to 0 counts
                    #print Count_90_Per_L
            #print Count_90_Per_L
            #print Count_90_Per_First # Prints the minimum count value required to get 90% probablity
            Count_90_Per_First_L.append(Count_90_Per_First)
            #print Prob_L
        #print "Count_90_Per_First_L : ",Count_90_Per_First_L
        Count_90_Per_First_L_H.append(Count_90_Per_First_L)
    return Count_90_Per_First_L_H

#Counts_L=[10,20,30,40,50,60,70,80,90,100]
#D_P_C_Big_Input_90_Per_Check([0.0411256372949457,0.135727335468768,0.13725522292245054,0.153680013049534],[10,20,30,40,50,60,70,80,90,100],[0,2,5,10])

def Count_Range_Generator(C_Min,C_Max,Step):
    """
    C_Min:-int, Count Minimum, The minimum amount of counts
    C_Max:-int, Count Maximum, The maximum amount of counts
    Step:-int, Step, The size of steps to take in the count range
    Returns: Count_List:-list, Count List, a list of all counts to be tested
    """
    Count_List=[]
    for C in range(C_Min,C_Max+1,Step):
        Count_List.append(C)
    return Count_List

#print Count_Range_Generator(2,110,1)

def Contour_Map(x,y,f,V_min,V_max,Step,Colorbar_Label,*args):
    X, Y = np.meshgrid(x, y)
    print "x:\n", x
    print "y:\n", y
    print "X:\n", X
    print "Y:\n", Y
    print "args: ", args
    #Z = f(X, Y, args[0])
    Z=np.zeros((len(X),len(X)))
    for i in range(0,len(X)):
        for j in range(0,len(X)):
            Z[i][j]=f(X[i][j],Y[i][j],args[0])
    #Z = f(X, Y)
    print "Z:\n", Z
    #plt.contourf(X, Y, Z, 20, cmap='viridis')
    plt.xscale('log')
    plt.contourf(X, Y, Z, np.arange(V_min,V_max+Step,Step), cmap='viridis',vmin=V_min,vmax=V_max)
    #plt.contour(X, Y, Z, [0.9], colors='black',vmin=V_min,vmax=V_max)
    #plt.contourf(X, Y, Z, 20, cmap='Wistia',vmin=V_min,vmax=V_max)
    #plt.colorbar(ticks=np.arange(V_min,V_max))
    #plt.colorbar()
    Colorbar=plt.colorbar(ticks=np.arange(V_min,V_max+Step,Step))
    Colorbar.set_label(Colorbar_Label)
    plt.contour(X, Y, Z, [0.9], colors='black',vmin=V_min,vmax=V_max, linewidths=0.5, linestyles="dashed")
    #plt.show()
def Offaxis_to_Graph_Num(Off):
    Graph_Num_to_Off_HL=[[1,0],[2,2],[3,5],[4,10]]
    for Graph_Num_to_Off_L in Graph_Num_to_Off_HL:
        if(Graph_Num_to_Off_L[1]==Off):
            return Graph_Num_to_Off_L[0]

def Detection_Probability_Plot(F):
    #Off_A=np.linspace(0,10,100)
    #Fname_L=glob.glob("/Volumes/xray/anthony/Research_Git/Background_Graph_Data_2/"+)
    Off_Known_L=[0,2,5,10]
    #Off_A=[0]
    Off_A=range(0,11)
    for Off in Off_A:
        #Background_A=np.linspace(0.0005,0.5,10)
        #Background_A=np.linspace(0.0001,1,10)
        Background_A=np.geomspace(0.0001,1,200)
        #Background_A=np.logspace(0.0005,0.5,10)
        #Background_A=np.linspace(0.0005,0.2,10) #Weird bug here #Update: The bug was from undersamping the data it has nothing do do with this location
        #Counts_A=np.arange(0,10)
        Counts_A=np.linspace(0,115,200) #Update: The bug was from undersamping the data it has nothing do do with this location
        #Counts_A=np.linspace(0,5,10) #Weird bug here
        #Data=np.zeros((100,100))
        """
        for i in range(0,len(Off_A)):
            Cur_Row=[]
            Off=Off_A[i]
            for j in range(0,len(Counts_A)):
                Counts=Counts_A[j]
                Data[i][j]=Postion_Error_Calc(Off,Counts)
        """
        #print Data
        Contour_Map(Background_A,Counts_A,F,0,1,0.1,"Probability",Off)
        if(Off in Off_A):
            Graph_Num=Offaxis_to_Graph_Num(Off)
            Graph_Data_Fpath_L=glob.glob("/Volumes/xray/anthony/Research_Git/Background_Graph_Data_2/"+"Graph "+str(Graph_Num)+"*")
            print "Graph_Data_Fpath_L: ", Graph_Data_Fpath_L
            for Graph_Data_Fpath in Graph_Data_Fpath_L:
                data = ascii.read(Graph_Data_Fpath) #data:-astropy.table.table.Table, data, The graph data for the current offaxis angle and number of counts.
                B_A=data['col1'] # B_A:-array, Background Array, The array contianing the background data from the current data file, in order of increasing background
                B_A=np.array(B_A) #Converts B_A to a numpy array
                B_A_Length=B_A.size
                #P_A=data['col2'] # P_A:-array, Probablity Array, The array of probabilities in the order of the increasing backgrounds they are associated with
                Counts_Known=float(Graph_Data_Fpath.split(" ")[2])
                C_A=np.zeros(B_A_Length)
                C_A.fill(Counts_Known)
                #plt.plot([0.04],[4],".",color="red")
                plt.plot(B_A,C_A,".",color="red")
        plt.xlabel("Background")
        plt.ylabel("Counts")
        plt.title("Detection Probability  "+"["+str(Off)+"']")
        Outpath="/Volumes/xray/anthony/Research_Git/Detection_Probablity_Calc/Detection_Probability_Plots/"
        ##Fname=F.__name__+"_"+str(Off)+"_Arcmin_Plot.pdf"
        Fname=F.__name__+"_"+str(Off)+"_Arcmin_Test_Plot.pdf"
        print "Fname: ", Fname
        plt.savefig(Outpath+Fname)
        #plt.show()
        plt.close()

#D_P_C_Big_Input_90_Per_Check([0.0411256372949457,0.135727335468768,0.13725522292245054,0.153680013049534],Count_Range_Generator(2,110,1),[0,2,5,10])
#D_P_C_Big_Input_90_Per_Check([0.0411256372949457,0.135727335468768,0.13725522292245054,0.153680013049534],[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],[0,2,5,10])
#D_P_C_Big_Input_90_Per_Check([0.0411256372949457,0.135727335468768,0.13725522292245054,0.153680013049534],2,110,[0,2,5,10])
#D_P_C_Big_Input_90_Per_Check([0.0411256372949457],2,110,[1,3,4,9])
#D_P_C_Big_Input_90_Per_Check([0.0411256372949457],[1,3,4,9])
#D_P_C_Big_Input_90_Per_Check([0.0411256372949457]) #This is the current working version's input
#D_P_C_Big_Input_90_Per_Check([0.07]) #This is the current working version's input
#D_P_C_Big_Input_90_Per_Check([0.04]) #This is the current working version's input
#D_P_C_Big_Input_90_Per_Check([0.03]) #This is the current working version's input
#D_P_C_Big_Input_90_Per_Check([0.0005,0.0007,0.005,0.03,0.05,0.1]) #This is the current working version's input
#print D_P_C_Big_Input_90_Per_Check([0.0005,0.0007,0.001,0.002,0.005,0.03,0.05,0.1]) #This is the current working version's input
#print D_P_C_Big_Input_90_Per_Check([0.0005]) #This is the current working version's input
Detection_Probability_Plot(Detection_Probability_Calc_3)
