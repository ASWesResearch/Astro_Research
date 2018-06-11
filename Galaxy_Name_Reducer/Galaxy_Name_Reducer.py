def Galaxy_Name_Reducer(Gname):
    """
    Gname:-str, Galaxy_Name, The "queriedName" name of the galaxy from the SQL_Standard_File
    """
    Gname_R=Gname
    #print "Gname : ",Gname
    Space_Included_Bool=(" " in Gname)
    #print "Space_Included_Bool : ", Space_Included_Bool
    Underscore_Included_Bool=("_" in Gname)
    #print "Underscore_Included_Bool : ", Underscore_Included_Bool
    if(" " in Gname):
        Gname_R=Gname.replace(" ","_")
        return Gname_R
    elif(Underscore_Included_Bool==False):
        i=0
        j=0
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
