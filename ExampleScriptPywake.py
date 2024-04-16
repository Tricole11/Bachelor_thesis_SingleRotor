from py_wake.site import UniformWeibullSite
import numpy as np
from py_wake import NOJ
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
from py_wake.wind_turbines import WindTurbine, WindTurbines
import matplotlib.pyplot as plt


u = [0,3,12,25,30]
ct= [0,8/9,8/9,.3,0]
power= [0,0,2000,2000,0]


my_wt = WindTurbine(name='Ramis superturbin',
                   diameter=235,
                   hub_height=320,
                   powerCtFunction=PowerCtTabular(u,power,'kW',ct))



f= [0.036,0.039,0.052,0.07,0.084,0.064,0.086,0.118,0.152,0.147,0.1,0.052]
A= [9.177,9.782,9.532,9.91,10.043,9.594,9.584,10.515,11.399,11.687,11.637,10.088]
k= [2.393,2.447,2.412,2.592,2.756,2.596,2.584,2.549,2.471,2.607,2.627,2.326]
wd=np.linspace(0,36,len(f),endpoint=False)
ti=.1


site=UniformWeibullSite(p_wd=f,a=A,k=k,ti=0.1)


def generate_turbine_positions(num_turbines,spacing=400):
    xs= []
    ys= []
    for i in range(num_turbines):
        xs.append((i%3)*spacing+1)
        ys.append((i//3)*spacing+1)
    return xs, ys


num_turbines=30 
xs, ys = generate_turbine_positions(num_turbines)


noj=NOJ(site,my_wt)


simulationResult=noj(xs,ys)


plt.figure()
aep=simulationResult.aep()
my_wt.plot(x=xs,y=ys)
c=plt.scatter(x=xs,y=ys,c=aep.sum(['wd','ws']))
plt.colorbar(c,label='AEP[GWh]')
plt.title('AEP of each turbine')
plt.xlabel('x [m]')
plt.ylabel('[m]')


plt.figure()
aep.sum(['wt','wd']).plot()
plt.xlabel("Wind speed [m/s]")
plt.ylabel("AEP [GWh]")
plt.title('AEP vs wind speed')


plt.figure()
aep.sum(['wt','ws']).plot()
plt.xlabel("Wind direction [deg]")
plt.ylabel("AEP [GWh]")
plt.title('AEP vs wind direction')


wind_speed = 10
wind_direction = 0


plt.figure()
flow_map = simulationResult.flow_map(ws=wind_speed, wd=wind_direction)
plt.figure(figsize=(18, 10))
flow_map.plot_wake_map()
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title(f'Wake map for {wind_speed} m/s and {wind_direction} deg')


plt.show()
