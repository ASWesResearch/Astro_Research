def Galaxy_Name_Reducer(Gname):
    """
    Gname:-str, Galaxy_Name, The "queriedName" name of the galaxy from the SQL_Standard_File
    """
    #print "Hello_World"
    Gname_R=Gname
    #print "Gname : ",Gname
    Space_Included_Bool=(" " in Gname)
    #print "Space_Included_Bool : ", Space_Included_Bool
    Underscore_Included_Bool=("_" in Gname)
    #print "Underscore_Included_Bool : ", Underscore_Included_Bool
    if(Underscore_Included_Bool):
        Gname_R_L=Gname_R.split("_")
        Gname_R_Left=Gname_R_L[0]
        #print "Gname_R_L : ", Gname_R_L
        #print "Gname_R_Left : ", Gname_R_Left
        Gname_R_Right=Gname_R_L[1]
        #print "Gname_R_Right : ", Gname_R_Right
        #print type(Gname_R_Right)
        if((Gname_R_Left=="NGC") and (Gname_R_Right[0]=="0")):
            Gname_R_Right_No_0=Gname_R_Right.replace("0","",1)
            #print "Popped_Number : ", Popped_Number
            #print "Gname_R_Right : ", Gname_R_Right
            Gname_R=Gname_R_Left+"_"+Gname_R_Right_No_0
        return Gname_R
    if(" " in Gname):
        Gname_R=Gname.replace(" ","_")
        Gname_R_L=Gname_R.split("_")
        Gname_R_Left=Gname_R_L[0]
        #print "Gname_R_L : ", Gname_R_L
        #print "Gname_R_Left : ", Gname_R_Left
        Gname_R_Right=Gname_R_L[1]
        #print "Gname_R_Right : ", Gname_R_Right
        #print type(Gname_R_Right)
        if((Gname_R_Left=="NGC") and (Gname_R_Right[0]=="0")):
            Gname_R_Right_No_0=Gname_R_Right.replace("0","",1)
            #print "Popped_Number : ", Popped_Number
            #print "Gname_R_Right : ", Gname_R_Right
            Gname_R=Gname_R_Left+"_"+Gname_R_Right_No_0
        return Gname_R
    elif(Underscore_Included_Bool==False):
        i=0
        j=0
        #print "Gname : ", Gname
        while(i<len(Gname)-1):
            i=i+1
            Cur_Sym=Gname[i]
            Pre_Sym=Gname[j]
            #print "Cur_Sym : ", Cur_Sym
            #print "Pre_Sym : ", Pre_Sym
            Cur_Num_B=Cur_Sym.isdigit()
            Pre_Num_B=Pre_Sym.isdigit()
            #print "Cur_Num_B : ", Cur_Num_B
            #print "Pre_Num_B : ", Pre_Num_B
            Gname_Length=len(Gname)
            #print "type(Gname_Length)", type(Gname_Length)
            if((Cur_Num_B==True) and(Pre_Num_B==False)):
                Gname_Letters=Gname[0:i]
                Gname_Numbers=Gname[i:Gname_Length]
                #print "Gname_Letters : ", Gname_Letters
                #print "Gname_Numbers : ", Gname_Numbers
                if((Gname_Letters=="NGC") and (Gname_Numbers[0]=="0")):
                    #Popped_Number=Gname_Numbers.pop(i)
                    #print "Popped_Number : ", Popped_Number
                    Gname_Numbers_No_0=Gname_Numbers.replace("0","",1)
                    #print "Gname_Numbers_No_0 : ", Gname_Numbers_No_0
                    Gname_R=Gname_Letters+"_"+Gname_Numbers_No_0
                    return Gname_R
                Gname_R=Gname_Letters+"_"+Gname_Numbers
                return Gname_R
            j=j+1
    return Gname_R

#print Galaxy_Name_Reducer("NGC4258")
#print Galaxy_Name_Reducer("NGC 346")
#print Galaxy_Name_Reducer("IRAS08572+3915")
#print Galaxy_Name_Reducer("VIRGO CLUSTER")
#print Galaxy_Name_Reducer("3C 299")
#print Galaxy_Name_Reducer("Willman 1")
#print Galaxy_Name_Reducer("M31")
#print Galaxy_Name_Reducer("NGC_4258")
#print Galaxy_Name_Reducer("Sombrero")
#print Galaxy_Name_Reducer("NGC 0346")
#print Galaxy_Name_Reducer("NGC0346")
#print Galaxy_Name_Reducer("NGC_0346")
#NGC 891
print Galaxy_Name_Reducer("NGC 891")
