def Area_Calc_2(xc,yc,ploystring_L,inner_r,rchange,outer_r):
    cur_r=inner_r
    n=1
    a_tot=0
    a_L=[]
    while((cur_r)<=outer_r):
        cur_r=(n*rchange) + inner_r
        shape1 ='circle(' + str(xc) +','+ str(yc)+','+ str(cur_r)+')'
        r1 = regParse(shape1)
        a_tot=0
        for s in ploystring_L:
            shape2 =s
            r2 = regParse(shape2)
            r3 = regParse(shape2 + "-" + shape1)
            cur_a= regArea(r2) - regArea(r3)
            a_tot=a_tot+cur_a
        a_L.append(a_tot)
        n=n+1
    return a_L
