import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

def visualise_weekly_simulation(df_analysis):
    mpl.rcParams["figure.figsize"] = [10,
                                      7]
    mpl.rcParams.update({"font.size":14})
    profit_week_start = pd.Timestamp(year=2023, 
                                     month=7, 
                                     day=17)
    ax = df_analysis[profit_week_start:profit_week_start + pd.Timedelta(weeks=1)]\
    [['State of Energy (kWh)', 'Price (EUR/kWh)']].plot(secondary_y='Price (EUR/kWh)', mark_right=False)
    ax.set_ylabel('State of energy (kWh)')
    ax.right_ax.set_ylabel('Price (EUR/kWh)')
    ax.get_legend().set_bbox_to_anchor((0.3, 
                                        1))
    plt.savefig('visualise_weekly_simulation.png', 
            dpi=450)