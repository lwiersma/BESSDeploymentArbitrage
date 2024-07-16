import numpy as np
import pulp

class Battery():
    
    def __init__(self,
                 time_horizon,
                 max_discharge_power_capacity,
                 max_charge_power_capacity):
        #Set up decision variables for optimization.
        #These are the hourly charge and discharge flows for
        #the optimization horizon, with their limitations.
        self.time_horizon = time_horizon
    
        self.charge = \
        pulp.LpVariable.dicts(
            "charging_power",
            ('c_t_' + str(i) for i in range(0,time_horizon)),
            lowBound=0, 
            upBound=max_charge_power_capacity,
            cat='Continuous')

        self.discharge = \
        pulp.LpVariable.dicts(
            "discharging_power",
            ('d_t_' + str(i) for i in range(0,time_horizon)),
            lowBound=0, 
            upBound=max_discharge_power_capacity,
            cat='Continuous')

    def set_objective(self, prices):
        #Create a model and objective function.
        #This uses price data, which must have one price
        #for each point in the time horizon.
        try:
            assert len(prices) == self.time_horizon
        except:
            print('Error: need one price for each hour in time horizon')
        
        #Instantiate linear programming model to maximize the objective
        self.model = pulp.LpProblem("Energy arbitrage", 
                                    pulp.LpMaximize)
    
        #Objective is profit
        #This formula gives the daily profit from charging/discharging
        #activities. Charging is a cost, discharging is a revenue
        self.model += \
        pulp.LpAffineExpression(
            [(self.charge['c_t_' + str(i)],
              -1*prices[i]) for i in range(0,self.time_horizon)]) +\
        pulp.LpAffineExpression(
            [(self.discharge['d_t_' + str(i)],
              prices[i]) for i in range(0,self.time_horizon)])
        
    def add_storage_constraints(self,
                                efficiency,
                                min_capacity,
                                discharge_energy_capacity,
                                initial_level):
        #Storage level constraint 1
        #This says the battery cannot have less than zero energy, at
        #any hour in the horizon
        #Note this is a place where round-trip efficiency is factored in.
        #The energy available for discharge is the round-trip efficiency
        #times the energy that was charged.       
        for hour_of_sim in range(1,self.time_horizon+1):     
            self.model += \
            initial_level \
            + pulp.LpAffineExpression(
                [(self.charge['c_t_' + str(i)], efficiency)
                 for i in range(0,hour_of_sim)]) \
            - pulp.lpSum(
                self.discharge[index]
                for index in('d_t_' + str(i)
                             for i in range(0,hour_of_sim)))\
            >= min_capacity
            
        #Storage level constraint 2
        #Similar to 1
        #This says the battery cannot have more than the
        #discharge energy capacity
        for hour_of_sim in range(1,self.time_horizon+1):
            self.model += \
            initial_level \
            + pulp.LpAffineExpression(
                [(self.charge['c_t_' + str(i)], efficiency)
                 for i in range(0,hour_of_sim)]) \
            - pulp.lpSum(
                self.discharge[index]
                for index in ('d_t_' + str(i)
                              for i in range(0,hour_of_sim)))\
            <= discharge_energy_capacity
            
    def add_throughput_constraints(self,
                                   max_daily_discharged_throughput):
        #Maximum discharge throughput constraint
        #The sum of all discharge flow within a day cannot exceed this
        #Include portion of the next day according to time horizon
        #Assumes the time horizon is at least 24 hours
        
        self.model += \
        pulp.lpSum(
            self.discharge[index] for index in (
                'd_t_' + str(i) for i in range(0,24))) \
        <= max_daily_discharged_throughput
        
        self.model += \
        pulp.lpSum(
            self.discharge[index] for index in (
                'd_t_' + str(i) for i in range(25,self.time_horizon))) \
        <= max_daily_discharged_throughput \
        *float(self.time_horizon-24)/24
        
    def solve_model(self):
        #Solve the optimization problem
        self.model.solve()
        
        #Show a warning if an optimal solution was not found
        if pulp.LpStatus[self.model.status] != 'Optimal':
            print('Warning: ' + pulp.LpStatus[self.model.status])
            
    def collect_output(self):  
        #Collect hourly charging and discharging rates within the
        #time horizon
        hourly_charges =\
            np.array(
                [self.charge[index].varValue for
                 index in ('c_t_' + str(i) for i in range(0,24))])
        hourly_discharges =\
            np.array(
                [self.discharge[index].varValue for
                 index in ('d_t_' + str(i) for i in range(0,24))])

        return hourly_charges, hourly_discharges