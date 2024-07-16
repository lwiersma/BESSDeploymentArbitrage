import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from functions.clean_ember_data import *
from functions.simulate_battery import *
from functions.analyse_simulation import *

filename = 'C:\\Users\\WiersmaL\\OneDrive - AECOM\\Projects\\ember-wholesaleprices-allcountries.csv'
country_of_interest = 'Germany'
start_time = pd.Timestamp(year=2023, 
                          month=1, 
                          day=1, 
                          hour=10)

max_discharge_power_capacity = 1000 #(kW)
max_charge_power_capacity = 1000 #(kW)
discharge_energy_capacity = 2000 #(kWh)

max_discharge_cycles = 2.0 #(-)
fraction_initial_state_of_charge = 0.5 #(-)
efficiency = 0.95 #(-)
time_horizon = 24 #(h)

all_hourly_charges, \
all_hourly_discharges, \
all_hourly_state_of_energy, \
all_daily_discharge_throughput = simulate_battery(initial_level = (discharge_energy_capacity * fraction_initial_state_of_charge),
                                                  price_data = clean_ember_data(filename, 
                                                                                country_of_interest),
                                                    max_discharge_power_capacity = max_discharge_power_capacity,
                                                    max_charge_power_capacity = max_charge_power_capacity,
                                                    discharge_energy_capacity = discharge_energy_capacity,
                                                    efficiency = efficiency,
                                                    max_daily_discharged_throughput = (max_discharge_cycles * discharge_energy_capacity),
                                                    time_horizon = time_horizon,
                                                    start_day = start_time)

df_analysis = analyse_simulation(filename = filename,
                                 country_of_interest = country_of_interest, 
                                 start_time = start_time, 
                                 all_hourly_charges = all_hourly_charges, 
                                 all_hourly_discharges = all_hourly_discharges, 
                                 all_hourly_state_of_energy = all_hourly_state_of_energy,
                                 all_daily_discharge_throughput = all_daily_discharge_throughput,
                                 discharge_energy_capacity = discharge_energy_capacity,
                                 fraction_initial_state_of_charge = fraction_initial_state_of_charge)

print(df_analysis['Profit (EUR)'].sum())

mpl.rcParams["figure.figsize"] = [8,6]
mpl.rcParams["figure.dpi"] = 150
mpl.rcParams.update({"font.size":14})
profit_week_start = pd.Timestamp(year=2023, month=7, day=17)
ax = df_analysis[profit_week_start:profit_week_start+pd.Timedelta(weeks=1)]\
[['State of Energy (kWh)', 'Price (EUR/kWh)']].plot(secondary_y='Price (EUR/kWh)', mark_right=False)
ax.set_ylabel('State of energy (kWh)')
ax.right_ax.set_ylabel('Price (EUR/MWh)')
ax.get_legend().set_bbox_to_anchor((0.3, 1))
plt.savefig('State_of_charge_selected_week.png', 
            dpi=450)
print(profit_week_start)