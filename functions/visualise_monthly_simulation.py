import matplotlib.pyplot as plt
import matplotlib as mpl

def visualise_monthly_simulation(df_analysis):
    mpl.rcParams["figure.figsize"] = [10,7]
    mpl.rcParams.update({"font.size":12})
    df_analysis['Profit (EUR)'].resample('M').sum().plot(kind='bar')
    plt.ylabel('Total monthly profit (EUR)')
    plt.savefig('Monthly_profit.png', 
            dpi=450)
    
#print(df_analysis['Profit (EUR)'].sum())