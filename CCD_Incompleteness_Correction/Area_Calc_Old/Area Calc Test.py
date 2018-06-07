def Area_Calc_Test(ploystring_L):
    a_tot=0
    for s in ploystring_L:
        r_cur= regParse(s)
        a_cur= regArea(r_cur)
        a_tot=a_tot + a_cur
    return a_tot
