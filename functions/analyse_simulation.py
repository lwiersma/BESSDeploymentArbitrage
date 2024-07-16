import pandas as pd
import numpy as np
from functions.clean_price_data import *

def analyse_simulation(filename, 
                       country_of_interest, 
                       start_time, 
                       all_hourly_charges, 
                       all_hourly_discharges, 
                       all_hourly_state_of_energy, 
                       all_daily_discharge_throughput,
                       discharge_energy_capacity,
                       fraction_initial_state_of_charge):
    df_analysis = clean_price_data(filename, 
                                   country_of_interest)
    end_time = start_time + pd.Timedelta(hours=(8760-1))
    df_analysis = df_analysis[start_time:end_time]
    #These indicate flows during the hour of the datetime index
    df_analysis['Charging power (kW)'] = all_hourly_charges
    df_analysis['Discharging power (kW)'] = all_hourly_discharges
    df_analysis['Power output (kW)'] = all_hourly_discharges - all_hourly_charges
    #This is the state of power at the beginning of the hour of the datetime index 
    df_analysis['State of Energy (kWh)'] = np.append((discharge_energy_capacity * fraction_initial_state_of_charge), 
                                                     all_hourly_state_of_energy[0:-1])
    df_analysis['Revenue generation (EUR)'] = df_analysis['Discharging power (kW)'] * df_analysis['Price (EUR/kWh)']
    df_analysis['Charging cost (EUR)'] = df_analysis['Charging power (kW)'] * df_analysis['Price (EUR/kWh)']
    df_analysis['Profit (EUR)'] = df_analysis['Revenue generation (EUR)'] - df_analysis['Charging cost (EUR)']
    return df_analysis