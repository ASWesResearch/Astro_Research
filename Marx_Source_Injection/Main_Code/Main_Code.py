from sherpa.astro.ui import *
from matplotlib import pyplot as plt
import numpy as np
import os
from os import system
import sys
from ciao_contrib.runtool import *
from multiprocessing import Pool

dir = os.path.dirname(__file__)
path=os.path.realpath('../')
#print "Path=",path
#system('pwd')
sys.path.append(os.path.abspath(path))

from Background_Generator import Background_Generator
from Source_Generator import Source_Generator

"""
def Synthetic_Background_Generator_Wrapper(Input_L):
    #Cur_Run_L=[Cur_Outpath, Cur_Background_Counts, Cur_Parameter_Outpath]
    Outpath=Input_L[0]
    Background_Counts=Input_L[1]
    Parameter_Outpath=Input_L[2]
    Seed_Biased=Input_L[4]
    Synthetic_Background_Generator(Outpath, Background_Counts, Parameter_Outpath, Seed_Biased)

def Synthetic_Background_Generator_Driver():
    Input_L=Synthetic_Background_Generator_Big_Input_Generator()
    Driver(Synthetic_Background_Generator_Wrapper, Input_L)
"""

def Driver(Func, Array):
    if __name__ == '__main__':
        P = Pool()
        P.map(Func, Array)

def Main_Wrapper(Input_L):
    #Cur_Run_L=[Cur_Outpath, Cur_Background_Counts, Cur_Parameter_Outpath]
    Outpath=Input_L[0]
    Background_Counts=Input_L[1]
    Parameter_Outpath=Input_L[2]
    Seed_Biased=Input_L[4]
    Main_Generator(Outpath, Background_Counts, Parameter_Outpath, Seed_Biased)

def Main_Driver():
    Input_L=Main_Big_Input_Generator()
    Driver(Main_Wrapper, Input_L)

def Main():
    Synthetic_Background_Generator_Driver()
    Main_Driver()
