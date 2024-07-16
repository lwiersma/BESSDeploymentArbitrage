import matplotlib.pyplot as plt
import matplotlib as mpl

def visualise_monthly_simulation(df_analysis):
    mpl.rcParams["figure.figsize"] = [12,8]
    mpl.rcParams.update({"font.size":11})
    monthly_profit = df_analysis['Profit (EUR)'].resample('M').sum()
    ax = monthly_profit.plot(kind='bar')
    ax.set_ylabel('Total monthly profit (EUR)')
    annual_profit = df_analysis['Profit (EUR)'].sum()
    ax.get_legend().set_bbox_to_anchor((0.3, 
                                        1))
    ax.set_xticks(range(len(monthly_profit.index)))
    ax.set_xticklabels([date.strftime('%b') for date in monthly_profit.index], rotation=0)
    ax.text(0.05, 
            0.95, 
            f'Annual Profit: {annual_profit:.2f} EUR', 
            transform = ax.transAxes,
            verticalalignment = 'top', 
            bbox = dict(facecolor = 'white', 
                      alpha = 0.5))
    plt.savefig('visualise_monthly_simulation.png', 
            dpi=450)