def Area_Calc_2(xc,yc,ploystring_L,inner_r,rchange,outer_r):
    cur_r=inner_r
    n=1
    a_L=[]
    while((cur_r)<=outer_r):
        cur_r=(n*rchange) + inner_r
        shape1 ='circle(' + str(xc) +','+ str(yc)+','+ str(cur_r)+')'
        r1 = regParse(shape1)
        for s in ploystring_L:
            shape2 =s
            r2 = regParse(shape2)
            r3 = regParse(shape2 + "-" + shape1)
            cur_a= regArea(r2) - regArea(r3)
            a_L.append(cur_a)
        n=n+1
    return a_L
