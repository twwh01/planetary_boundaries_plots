#%% import modules
from planetary_boundary_classes import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os import path

#%% set file paths and parameters
dir_data = path.join('data')
dir_plots = path.join('plots')
save_plot = True

#%% load datasets
indata = pd.read_excel(path.join(dir_data, 'planetary_boundaries_data.xlsx'), sheet_name='2023')
indata.head(5)
list(indata.columns.values)

#%% get data
print(indata.iloc[:,0:2])

# for future: automate this step
# control_variables = list[]
# for variable in range(len(indata['control_variable'])):
    
co2_data = indata.loc[indata['control_variable'] == 'carbon dioxide', :]
radiative_data = indata.loc[indata['control_variable'] == 'radiative forcing', :]
functional_data = indata.loc[indata['control_variable'] == 'functional integrity', :]
genetic_data = indata.loc[indata['control_variable'] == 'genetic diversity', :]
ozone_data = indata.loc[indata['control_variable'] == 'ozone', :]
acidification_data = indata.loc[indata['control_variable'] == 'aragonite saturation state', :]
phosphorus_data = indata.loc[indata['control_variable'] == 'phosphorus', :]
nitrogen_data = indata.loc[indata['control_variable'] == 'nitrogen', :]
forest_data = indata.loc[indata['control_variable'] == 'forest cover', :]
bluewater_data = indata.loc[indata['control_variable'] == 'blue water', :]
greenwater_data = indata.loc[indata['control_variable'] == 'green water', :]
aerosol_data = indata.loc[indata['control_variable'] == 'AOD', :]
entities_data = indata.loc[indata['control_variable'] == 'novel entities', :]

#%% build control variable impacts
# for future also automate this step

# water
blue_water = ControlVariable(
    name=bluewater_data['control_variable'].iat[0], 
    baseline_value=bluewater_data['baseline'].iat[0],
    current_value=bluewater_data['current_value'].iat[0], 
    boundary_value=bluewater_data['planetary_boundary'].iat[0], 
    upper_value=bluewater_data['upper_limit'].iat[0]
)
green_water = ControlVariable(
    name=greenwater_data['control_variable'].iat[0], 
    baseline_value=greenwater_data['baseline'].iat[0],
    current_value=greenwater_data['current_value'].iat[0], 
    boundary_value=greenwater_data['planetary_boundary'].iat[0], 
    upper_value=greenwater_data['upper_limit'].iat[0]
)
# climate
radiative_forcing = ControlVariable(
    name=radiative_data['control_variable'].iat[0], 
    baseline_value=radiative_data['baseline'].iat[0],
    current_value=radiative_data['current_value'].iat[0], 
    boundary_value=radiative_data['planetary_boundary'].iat[0], 
    upper_value=radiative_data['upper_limit'].iat[0]
)
co2_concentration = ControlVariable(
    name=co2_data['control_variable'].iat[0], 
    baseline_value=co2_data['baseline'].iat[0],
    current_value=co2_data['current_value'].iat[0], 
    boundary_value=co2_data['planetary_boundary'].iat[0], 
    upper_value=co2_data['upper_limit'].iat[0]
)

# biosphere
functional_integrity = ControlVariable(
    name=functional_data['control_variable'].iat[0], 
    baseline_value=functional_data['baseline'].iat[0],
    current_value=functional_data['current_value'].iat[0], 
    boundary_value=functional_data['planetary_boundary'].iat[0], 
    upper_value=functional_data['upper_limit'].iat[0]
)
genetic_diversity = ControlVariable(
    name=genetic_data['control_variable'].iat[0], 
    baseline_value=genetic_data['baseline'].iat[0],
    current_value=genetic_data['current_value'].iat[0], 
    boundary_value=genetic_data['planetary_boundary'].iat[0], 
    upper_value=genetic_data['upper_limit'].iat[0]
)

# biogeochemistry
nitrogen = ControlVariable(
    name=nitrogen_data['control_variable'].iat[0], 
    baseline_value=nitrogen_data['baseline'].iat[0],
    current_value=nitrogen_data['current_value'].iat[0], 
    boundary_value=nitrogen_data['planetary_boundary'].iat[0], 
    upper_value=nitrogen_data['upper_limit'].iat[0]
)
phosphorus = ControlVariable(
    name=phosphorus_data['control_variable'].iat[0], 
    baseline_value=phosphorus_data['baseline'].iat[0],
    current_value=phosphorus_data['current_value'].iat[0], 
    boundary_value=phosphorus_data['planetary_boundary'].iat[0], 
    upper_value=phosphorus_data['upper_limit'].iat[0]
)

# aerosols
atmospheric_aerosols = ControlVariable(
    name=aerosol_data['control_variable'].iat[0], 
    baseline_value=aerosol_data['baseline'].iat[0],
    current_value=aerosol_data['current_value'].iat[0], 
    boundary_value=aerosol_data['planetary_boundary'].iat[0], 
    upper_value=aerosol_data['upper_limit'].iat[0]
)

# ozone
ozone_layer = ControlVariable(
    name=ozone_data['control_variable'].iat[0], 
    baseline_value=ozone_data['baseline'].iat[0],
    current_value=ozone_data['current_value'].iat[0], 
    boundary_value=ozone_data['planetary_boundary'].iat[0], 
    upper_value=ozone_data['upper_limit'].iat[0]
)

# ocean acidification
ocean_acidification = ControlVariable(
    name=acidification_data['control_variable'].iat[0], 
    baseline_value=acidification_data['baseline'].iat[0],
    current_value=acidification_data['current_value'].iat[0], 
    boundary_value=acidification_data['planetary_boundary'].iat[0], 
    upper_value=acidification_data['upper_limit'].iat[0]
)

# novel entities
novel_entities = ControlVariable(
    name=entities_data['control_variable'].iat[0], 
    baseline_value=entities_data['baseline'].iat[0],
    current_value=entities_data['current_value'].iat[0], 
    boundary_value=entities_data['planetary_boundary'].iat[0], 
    upper_value=entities_data['upper_limit'].iat[0]
)

# land use
land_use = ControlVariable(
    name=forest_data['control_variable'].iat[0], 
    baseline_value=forest_data['baseline'].iat[0],
    current_value=forest_data['current_value'].iat[0], 
    boundary_value=forest_data['planetary_boundary'].iat[0], 
    upper_value=forest_data['upper_limit'].iat[0]
)

#%% build planetray boundary variables
water = PlanetaryBoundary('Freshwater\nchange', [blue_water, green_water])
climate = PlanetaryBoundary('Climate\nchange', [radiative_forcing, co2_concentration])
biosphere = PlanetaryBoundary('Biosphere\nintegrity', [functional_integrity, genetic_diversity])
biogeochemistry = PlanetaryBoundary('Biogeochemical\nflows', [nitrogen, phosphorus])
aerosols = PlanetaryBoundary('Atmospheric\naerosol\nloading', [atmospheric_aerosols])
ozone = PlanetaryBoundary('Stratospheric\nozone\ndepletion', [ozone_layer])
acidification = PlanetaryBoundary('Ocean\nacidification', [ocean_acidification])
novel_entity = PlanetaryBoundary('Novel\nentities', [novel_entities])
land_use_change = PlanetaryBoundary('Land\nsystem\nchange', [land_use])

#%% build planetary boundary system & plot
pbs_2023 = PlanetarySystem(
    'PBS: 2023', 
    [
     ozone, 
     novel_entity, 
     climate, 
     biosphere, 
     land_use_change, 
     water, 
     biogeochemistry, 
     acidification, 
     aerosols
     ]
    )

ax = pbs_2023.plot(label=True, control_var_label=True)
plt.title('PBS 2023', loc='left', fontweight='bold')
# plt.show()
plt.savefig(path.join(dir_plots, 'pbs_2023.png'), dpi=600, bbox_inches='tight')
