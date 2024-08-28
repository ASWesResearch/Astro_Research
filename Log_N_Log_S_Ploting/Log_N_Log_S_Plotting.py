import numpy as np
import matplotlib.pyplot as plt

def Giacconi_Background_Source_Density(Flux,Hardness_Str="S"): # GIACCONI
    if(Hardness_Str=="S"):
        #Soft Equation
        N=370.0*((Flux/(2.0E-15))**(-0.85)) #In sources per deg^2
    if(Hardness_Str=="H"):
        #Hard Equation
        N=1200.0*((Flux/(2.0E-15))**(-1.0)) #In sources per deg^2
    return N

def Standard_Derivative_Form(S,K,B,S_ref=1E-14):
    dN_dS=K*((S/S_ref)**(-B))
    return dN_dS

def Standard_Integral_Form(S,K,B,S_ref=1E-14):
    if(B<=1):
        return np.nan
    N=(-K/(1.0-B))*((S/S_ref)**(1.0-B))
    return N

def Broken_Derivative_Form(S,K,B1,B2,f_b,S_ref=1E-14):
    f_b=f_b*(1E-15)
    #K=K*(1E14)
    #print("S: ", S)
    #print("f_b: ", f_b)
    if(S<=f_b):
        #print("Break")
        dN_dS=K*((S/S_ref)**(-B1))
    if(S>f_b):
        dN_dS=K*((f_b/S_ref)**(B2-B1))*((S/S_ref)**(-B2))
    return dN_dS

def Broken_Integral_Form(S,K,B1,B2,f_b,S_ref=1E-14):
    if((B1<=1) or (B2<=1)):
        return np.nan
    f_b=f_b*(1E-15)
    #K=K*(1E14)
    if(S<=f_b):
        N=(-K/(1.0-B1))*((S/S_ref)**(1.0-B1))
    if(S>f_b):
        N=(-K*((f_b/S_ref)**(B2-B1))/(1.0-B2))*((S/S_ref)**(1.0-B2))
    return N

def Standard_Form_Wrap(Func, S, Tuple):
    return Func(S,Tuple[0],Tuple[1])

def Broken_Form_Wrap(Func, S, Tuple):
    return Func(S,Tuple[0],Tuple[1],Tuple[2],Tuple[3], S_ref=1E-14)

def Key_Query(Key, Hardness_Str):
    if(Hardness_Str=="S"):
        #Soft Equation
        Dict={"AGN":(161.96, 1.52, 2.45, 7.1), "Gal":(2.01, 2.24), "Star":(4.14, 1.45)}
    if(Hardness_Str=="H"):
        #Hard Equation
        Dict={"AGN":(453.70, 1.46, 2.72, 8.9), "Gal":(0.75, 2.56), "Star":(0.73, 1.88)}
    Paramter_Tuple=Dict[Key]
    return Paramter_Tuple

def Key_Based_Derivative_Form(S, Key, Hardness_Str):
    Tuple=Key_Query(Key, Hardness_Str)
    #print(Tuple)
    if(Key=="AGN"):
        dN_dS=Broken_Form_Wrap(Broken_Derivative_Form, S, Tuple)
    else:
        dN_dS=Standard_Form_Wrap(Standard_Derivative_Form, S, Tuple)
    return dN_dS

def Key_Based_Integral_Form(S, Key, Hardness_Str):
    Tuple=Key_Query(Key, Hardness_Str)
    #print(Tuple)
    if(Key=="AGN"):
        N=Broken_Form_Wrap(Broken_Integral_Form, S, Tuple)
    else:
        N=Standard_Form_Wrap(Standard_Integral_Form, S, Tuple)
    return N

def Derivative_Plot(Hardness_Str):
    #S_A=np.linspace(1E-17, 1E-13, num=2000)
    S_A=np.linspace(2E-18, 1E-13, num=2000)
    #dN_dS_AGN_Soft_A=Key_Based_Derivative_Form(S_A, "AGN", "S")
    #Lum_A=np.vectorize(Luminosity_Calc)(Flux_A,Dist_A)
    #dN_dS_AGN_Soft_A=np.vectorize(Key_Based_Derivative_Form,excluded=["AGN", "S"])(S_A, "AGN", "S")
    dN_dS_Soft_AGN_A=np.vectorize(Key_Based_Derivative_Form,excluded=["AGN", Hardness_Str])(S_A, "AGN", Hardness_Str)
    dN_dS_Soft_Gal_A=np.vectorize(Key_Based_Derivative_Form,excluded=["Gal", Hardness_Str])(S_A, "Gal", Hardness_Str)
    dN_dS_Soft_Star_A=np.vectorize(Key_Based_Derivative_Form,excluded=["Star", Hardness_Str])(S_A, "Star", Hardness_Str)
    dN_dS_Soft_A=dN_dS_Soft_AGN_A+dN_dS_Soft_Gal_A+dN_dS_Soft_Star_A
    plt.loglog(S_A,dN_dS_Soft_AGN_A,label="AGN", color="red")
    plt.loglog(S_A,dN_dS_Soft_Gal_A,label="Gal", color="blue")
    plt.loglog(S_A,dN_dS_Soft_Star_A,label="Star", color="green")
    plt.loglog(S_A,dN_dS_Soft_A,label="Total BG", color="black")
    plt.legend(loc="upper right")
    Hardness_Dict={"S":"Soft","H":"Hard"}
    plt.title("Derivative Log(N)-Log(S) "+str(Hardness_Dict[Hardness_Str]))
    plt.xlabel("S (erg cm^-2 s^-1)")
    plt.ylabel("dN/dS")
    plt.savefig("Derivative_Log_N_Log_S_"+str(Hardness_Dict[Hardness_Str])+".pdf")
    plt.cla()
    plt.clf()

def Integral_Plot(Hardness_Str):
    #S_A=np.linspace(1E-17, 1E-13, num=2000)
    S_A=np.linspace(2E-18, 1E-13, num=2000)
    #S_A=np.linspace(6.5E-17, 1E-13, num=2000)
    #dN_dS_AGN_Soft_A=Key_Based_Derivative_Form(S_A, "AGN", "S")
    #Lum_A=np.vectorize(Luminosity_Calc)(Flux_A,Dist_A)
    #dN_dS_AGN_Soft_A=np.vectorize(Key_Based_Derivative_Form,excluded=["AGN", "S"])(S_A, "AGN", "S")
    N_Soft_AGN_A=np.vectorize(Key_Based_Integral_Form,excluded=["AGN", Hardness_Str])(S_A, "AGN", Hardness_Str)
    N_Soft_Gal_A=np.vectorize(Key_Based_Integral_Form,excluded=["Gal", Hardness_Str])(S_A, "Gal", Hardness_Str)
    N_Soft_Star_A=np.vectorize(Key_Based_Integral_Form,excluded=["Star", Hardness_Str])(S_A, "Star", Hardness_Str)
    Alt_N=Giacconi_Background_Source_Density(S_A,Hardness_Str)
    N_Soft_A=N_Soft_AGN_A+N_Soft_Gal_A+N_Soft_Star_A
    plt.loglog(S_A,N_Soft_AGN_A,label="AGN", color="red")
    plt.loglog(S_A,N_Soft_Gal_A,label="Gal", color="blue")
    plt.loglog(S_A,N_Soft_Star_A,label="Star", color="green")
    plt.loglog(S_A,Alt_N,label="Giacconi", color="orange")
    plt.loglog(S_A,N_Soft_A,label="Total BG", color="black")
    #plt.vlines(2.5E-16, 0, 1E5, colors="grey", linestyles="dashed")
    plt.legend(loc="upper right")
    Hardness_Dict={"S":"Soft","H":"Hard"}
    plt.title("Integral Log(N)-Log(S) "+str(Hardness_Dict[Hardness_Str]))
    plt.xlabel("S (erg cm^-2 s^-1)")
    plt.ylabel("N(>S) (deg^-2)")
    plt.savefig("Integral_Log_N_Log_S_"+str(Hardness_Dict[Hardness_Str])+".pdf")
    plt.cla()
    plt.clf()

#print(Key_Based_Derivative_Form(1E-15, "AGN", "S"))
#print(Key_Based_Derivative_Form(1E-15, "Gal", "S"))
#print(Key_Based_Derivative_Form(1E-16, "AGN", "S"))
Integral_Plot("S")
Derivative_Plot("S")
Integral_Plot("H")
Derivative_Plot("H")
