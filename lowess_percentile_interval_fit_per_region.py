import pandas as pd
import numpy as np
import xarray as xr
import os
# this is the LOWESS fitting library that we use ... 
from moepy import lowess, eda

from sklearn.preprocessing import MinMaxScaler

from scipy.optimize import curve_fit
import sys
import oggm
# load global mean temperature change files 
# note that the global mean temperature (GMT) changes have been computed by using the assumption that GMT changed from 1850-1900 to 1986-2005 by 0.63°C 
# (this is the assumption used by the IPCC SROCC -> --> https://www.ipcc.ch/srocc/chapter/summary-for-policymakers/
# IPCC, 2019: Summary for Policymakers. In: IPCC Special Report on the Ocean and Cryosphere in a Changing Climate [H.-O. Pörtner, D.C. Roberts, V. Masson-Delmotte,
# P. Zhai, M. Tignor, E. Poloczanska, K. Mintenbeck, A. Alegría, M. Nicolai, A. Okem, J. Petzold, B. Rama, N.M. Weyer (eds.)]. In press.
# -> future follow-up studies should use the updated estimates (e.g. IPCC AR6 WG1 updated the methods and found a GMT change of 0.69°C from 1850-1900 and 1986-2005)
_file_cmip5 = '/home/www/oggm/oggm-standard-projections/analysis_notebooks/Global_mean_temp_deviation_2071_2100_2081_2100_2271_2300_2281_2300_rel_1850_1900_cmip5_gcms.csv'
pd_cmip5_temp_ch_2100 = pd.read_csv(_file_cmip5, index_col=0)
pd_cmip5_temp_ch_2100['cmip'] = 'CMIP5'
_file_cmip6 = '/home/www/oggm/oggm-standard-projections/analysis_notebooks/Global_mean_temp_deviation_2071_2100_2081_2100_2271_2300_2281_2300_rel_1850_1900_cmip6_gcms.csv'
# these files are also available under: 
# https://cluster.klima.uni-bremen.de/~oggm/oggm-standard-projections/analysis_notebooks/Global_mean_temp_deviation_2071_2100_2081_2100_2271_2300_2281_2300_rel_1850_1900_cmip5_gcms.csv'
# https://cluster.klima.uni-bremen.de/~oggm/oggm-standard-projections/analysis_notebooks/Global_mean_temp_deviation_2071_2100_2081_2100_2271_2300_2281_2300_rel_1850_1900_cmip6_gcms.csv'

pd_cmip6_temp_ch_2100 = pd.read_csv(_file_cmip6, index_col=0)
pd_cmip6_temp_ch_2100['cmip'] = 'CMIP6'

# change this path to your local path 
pd_cmip_temp_ch_2100 = pd.concat([pd_cmip6_temp_ch_2100, pd_cmip5_temp_ch_2100])
pd_cmip_temp_ch_2100 = pd_cmip_temp_ch_2100.loc[pd_cmip_temp_ch_2100.ssp != 'ssp534-over']

pd_cmip_temp_ch_2100_gcm_until_2300 = pd_cmip_temp_ch_2100.loc[pd_cmip_temp_ch_2100['global_temp_ch_2271-2300_preindustrial'].dropna().index]
data_temp = pd_cmip_temp_ch_2100_gcm_until_2300['global_temp_ch_2071-2100_preindustrial'].values.reshape(1,-1).T
scaler = MinMaxScaler()
scaler.fit(data_temp)
t_min, t_max = pd_cmip_temp_ch_2100_gcm_until_2300['global_temp_ch_2071-2100_preindustrial'].min(), pd_cmip_temp_ch_2100_gcm_until_2300['global_temp_ch_2071-2100_preindustrial'].max()
print(t_min, t_max)


def exponential_decay(x, a, b):
    # avoid overflow -> does not work ... 
    exp_values = -b * x
    #exp_values = np.clip(exp_values, -709, 709)  # Clip values to avoid overflow
    return a * np.exp(exp_values) #+ c * np.exp(-d * x**2)#**c  ### SIMPLE is BETTER
param_bounds = ([0, 0], [2000, 5])

rgi_regs_global = ['global','01', '02', '03', '04', '05', '06', '07',
                   '08', '09', '10', '11', '12', '13', '14', '15',
                   '16', '17', '18', '19', '13-14-15']
pd_fit_data_all = pd.read_csv(f'/home/www/lschuster/glacier-model-standard-projections_cluster/fit_data_temp_evol_global_regional_oggm_pygem_glogem_oct182023.csv', index_col=0)


r = int(sys.argv[1])
it = int(sys.argv[2])

_rgi_reg = rgi_regs_global[r]
for sim_year in [2100, 2300]:

    if _rgi_reg !='global':
        region = f'RGI{_rgi_reg}'
    else:
        region = _rgi_reg 

    r_pd_fit_stats = pd.DataFrame(columns=['region','year', 'fit_opt' ,'deltaTemp', 'frac','it','N', 'q50', 'q05', 'q25', 'q75', 'q95'],
                             index = np.arange(0,30000,1))
    
    # this is the data we want to fit
    data = pd_fit_data_all.loc[(pd_fit_data_all.year==sim_year) & (pd_fit_data_all.region==region)]
    x = data['global_temp_ch_2071-2100_preindustrial'].values
    y = data['rel_ice_%_2020'].values

    eval_x =np.arange(x.min().round(1), x.max()*1.001, 0.05)
    # just for comparison, also compute the exponential fit
    r_pd_fit_stats.loc[:len(eval_x)-1,'deltaTemp'] = eval_x
    popt, pcov = curve_fit(exponential_decay, x,y,
                       loss='soft_l1', f_scale=0.1, bounds = param_bounds) 
    a_opt, b_opt = popt
    y_fitted_exp = exponential_decay(eval_x, a_opt, b_opt)
    r_pd_fit_stats.loc[:len(eval_x)-1,'fit_opt'] = 'exp'
    r_pd_fit_stats.loc[:len(eval_x)-1, 'q50'] = y_fitted_exp


    jj = 0
    for N in [1000]:
        for _,frac in enumerate(np.arange(0.3, 1,
                                          0.01)):
            # Compute the median,IQR, 95% percentile interval
            ind_start = (len(eval_x)-1) + (len(eval_x)-1)*jj
            ind_end = ind_start + len(eval_x)-1
            r_pd_fit_stats.loc[ind_start:ind_end,'deltaTemp'] = eval_x
            df_quantiles = lowess.quantile_model(x, y, x_pred=eval_x, frac=frac, num_fits=N, robust_iters=it,
                                 qs=[0.5,0.05,0.25,0.75,0.95])
            r_pd_fit_stats.loc[ind_start:ind_end,'deltaTemp'] = eval_x
            j= 0
            # compute some statistics (do the quantiles go below zero, are the monotonoically decreasing???)
            for s,q in zip(['q50', 'q05', 'q25', 'q75', 'q95'], [0.5,0.05,0.25,0.75,0.95]):
                r_pd_fit_stats.loc[ind_start:ind_end,s] = df_quantiles[q].values
                r_pd_fit_stats.loc[ind_start:ind_end,f'min_{s}_diff'] = (df_quantiles[q].iloc[:-1].values - df_quantiles[q].iloc[1:].values).min()
                r_pd_fit_stats.loc[ind_start:ind_end,f'min_{s}'] = df_quantiles[q].min()
                j+=1

            r_pd_fit_stats.loc[ind_start:ind_end,'frac'] = frac
            r_pd_fit_stats.loc[ind_start:ind_end,'it'] = it
            r_pd_fit_stats.loc[ind_start:ind_end,'N'] = N
            r_pd_fit_stats.loc[ind_start:ind_end,'fit_opt'] = 'lowess_predi'
            jj +=1
            print(frac)


    r_pd_fit_stats = r_pd_fit_stats.dropna(how='all')
    r_pd_fit_stats['region'] = region
    r_pd_fit_stats['year'] = sim_year
    r_pd_fit_stats[r_pd_fit_stats.columns[3:]] = r_pd_fit_stats[r_pd_fit_stats.columns[3:]].astype(float)
    r_pd_fit_stats.to_csv(f'/home/www/lschuster/glacier-model-standard-projections_cluster/fits_lowess_predi/fit_stats_oct29_predi_{region}_{sim_year}_{it}.csv')
