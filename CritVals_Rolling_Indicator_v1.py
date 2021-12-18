#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 12:59:55 2021

@author: andrewhill
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS


def rolling_indicator (nsims, maxtime, a1, a2, t1, t2,
                       roll_size):
    
    tlists = []
    plists = []
    
    for j in range(0, nsims):
    
        price_path = [0]
    
        for t in range(0, maxtime+1):
        
            if t < t1:
                alpha = a1
            elif t > t2:
                alpha = a1
            else:
                alpha = a2
     
            price_path[t] = alpha*price_path[t-1] + np.random.normal(loc=0, scale=1.0)
            price_path.append(price_path[t])
    
        path = pd.DataFrame(price_path)
        path.columns = ['Yt']
        path['Yt_1'] = path['Yt'].shift(1)
        path['dYt'] = path['Yt'].diff()

        simdat = path.dropna()

        rolldat = simdat.dropna()
        rollX = rolldat['Yt_1']
        rollY = rolldat['dYt']

        mod = RollingOLS(rollY, rollX, window=roll_size)
        rolling_res = mod.fit()

        tval = rolling_res.tvalues
        tval[j] = tval.dropna()
        tlists.append(tval[j])
        
        parms = rolling_res.params
        parms[j] = parms.dropna()
        plists.append(parms[j])
        
    df1 = pd.DataFrame(tlists)
    pctls = df1.quantile([0.10, 0.05, 0.025, 0.01])
    
    return pctls;
