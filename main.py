import csv
import os
import pandas as pd
from functions.clean_ember_data import *
from functions.simulate_battery import *

filename = 'C:\\Users\\WiersmaL\\OneDrive - AECOM\\Projects\\ember-wholesaleprices-allcountries.csv'
country_of_interest = 'Germany'
start_time = pd.Timestamp(year=2023, 
                          month=1, 
                          day=1, 
                          hour=10)
end_time = pd.Timestamp(year=2024, 
                        month=1, 
                        day=1, 
                        hour=10)

max_discharge_power_capacity = 1000 #(kW)
max_charge_power_capacity = 1000 #(kW)
discharge_energy_capacity = 5000 #(kWh)
#max_daily_discharged_throughput = 200  #(kWh)

max_discharge_cycles = 2.0 #(-)
fraction_initial_state_of_charge = 0.5 #(-)
efficiency = 0.90 #(-)

all_hourly_charges, all_hourly_discharges, all_hourly_state_of_energy,\
all_daily_discharge_throughput = \
simulate_battery(initial_level = (discharge_energy_capacity * fraction_initial_state_of_charge),
                 price_data = clean_ember_data(filename, 
                                               country_of_interest),
                 max_discharge_power_capacity = max_discharge_power_capacity,
                 max_charge_power_capacity = max_charge_power_capacity,
                 discharge_energy_capacity = discharge_energy_capacity,
                 efficiency = efficiency,
                 max_daily_discharged_throughput = (max_discharge_cycles * discharge_energy_capacity),
                 time_horizon = 24,
                 start_day = start_time)
