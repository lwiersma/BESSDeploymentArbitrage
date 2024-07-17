import pandas as pd
import time
from functions.simulate_battery import *
from functions.analyse_simulation import *
from functions.visualise_weekly_simulation import *
from functions.visualise_monthly_simulation import *

#Track simulation time
tic = time.time()

filename = 'C:\\Users\\WiersmaL\\OneDrive - AECOM\\Projects\\ember-wholesaleprices-allcountries.csv'
country_of_interest = 'Germany'
start_time = pd.Timestamp(year=2023, 
                          month=1, 
                          day=1, 
                          hour=10)

max_discharge_power_capacity = 750 #(kW)
max_charge_power_capacity = 750 #(kW)
discharge_energy_capacity = 2000 #(kWh)

max_discharge_cycles = 2.0 #(-)
fraction_initial_state_of_charge = 0.5 #(-)
efficiency = 0.95 #(-)
time_horizon = 24 #(h)

all_hourly_charges, all_hourly_discharges, all_hourly_state_of_energy, all_daily_discharge_throughput = simulate_battery(
    initial_level = (discharge_energy_capacity * fraction_initial_state_of_charge),
    filename = filename,
    country_of_interest = country_of_interest,
    max_discharge_power_capacity = max_discharge_power_capacity,
    max_charge_power_capacity = max_charge_power_capacity,
    discharge_energy_capacity = discharge_energy_capacity,
    efficiency = efficiency,
    max_daily_discharged_throughput = (max_discharge_cycles * discharge_energy_capacity),
    time_horizon = time_horizon,
    start_day = start_time)

df_analysis = analyse_simulation(
    filename = filename,
    country_of_interest = country_of_interest, 
    start_time = start_time, 
    all_hourly_charges = all_hourly_charges, 
    all_hourly_discharges = all_hourly_discharges, 
    all_hourly_state_of_energy = all_hourly_state_of_energy,
    all_daily_discharge_throughput = all_daily_discharge_throughput,
    discharge_energy_capacity = discharge_energy_capacity,
    fraction_initial_state_of_charge = fraction_initial_state_of_charge)

visualise_weekly_simulation(df_analysis)
visualise_monthly_simulation(df_analysis)

toc = time.time()
print('Total simulation time: ' + str(toc-tic) + ' seconds')