# function pile for Paper_plot notebook
import sys
import os
import time
import datetime as dt
import math
import numpy as np 
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json 
import librosa
from IPython.display import Audio
import mir_eval.sonify
import pingouin as pg

from scipy.signal import butter, filtfilt, argrelextrema
from scipy import interpolate
from scipy.interpolate import interp1d

# from Laughter/Linedancing/Analysis/LineDancing_talk2.ipynb
def xcov(datax, datay,maxlag=10):
    # https://stackoverflow.com/questions/33171413/cross-correlation-time-lag-correlation-with-pandas
    rs = []
    for i in range(-maxlag,maxlag):
        rs.append(datax.corr(datay.shift(i)))
    return rs


def annat_shade(ax,laughs,colour,hatching=None,face_alpha = 0.2):
    # shading plots
    for i,r in laughs.iterrows():
        ax.axvspan(r['TIME'],r['TIME']+r['DURATION'], facecolor=colour,hatch=hatching,edgecolor="w",alpha = face_alpha)
    return

def resp_shade(ax,breaths,cat,colour):
    # shading plots
    resps_to_shade = breaths.query('Categories==@cat')
    for i,r in resps_to_shade.iterrows():
        ax.axvspan(r['In'],r['In']+r['Period_T'], facecolor=colour,alpha = 0.2)
    return

def resp_shaded(ax,breaths,cat,colour):
    # shading plots
    resps_to_shade = breaths.query('Categories==@cat')
    for i,r in resps_to_shade.iterrows():
        ax.axvspan(r['In'],r['In']+r['Insp_T'], facecolor=colour,alpha = 0.4)
        ax.axvspan(r['Ex'],r['Ex']+r['Exp_T'], facecolor=colour,alpha = 0.2)

    return


def Sectioning(sections_dict,pallet_dict,colIDs):

    player_pallet = {}
    collist = []
    sectag = []
    seccount = []
    sectick = []
    alist = []
    i=0
    for k in sections.keys():
    #     print(sections[k])
        c = np.array(section_pallet[k])
        d_c = c/(1.25*len(sections[k])) #n_c = len(sections[k])
        c_i = 0
        sublist = []
        for s in sections[k]:
            if s in colIDs: 
                sublist.append(s)
                alist.append(s)
                player_pallet[s] = c - c_i*d_c # np.power(c,c_i/2)
                c_i+=1
    #     print(sublist)
        if len(sublist)>0:
            sectick.append(i)
            sectag.append(k)
            i += len(sublist)/2
            seccount.append(i)
            i += len(sublist)/2
            i+=1
            for s in sublist: collist.append(s)
            collist.append(' ')
    
        sect_dets = {}
        sect_dets['Sections'] = sections_dict
        sect_dets['Colours'] = pallet_dict
        sect_dets['Col_pallet'] = player_pallet
        sect_dets['Cols_in'] = alist
        sect_dets['Spaced_cols'] = collist
        sect_dets['Section_tags'] = sectag
        sect_dets['Section_ticks_mid'] = seccount
        sect_dets['Section_ticks_low'] = sectick
    return sect_dets
# print([sectag,seccount,collist])