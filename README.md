# Plotting the planetary boundaries

![2025 planetary boundaries following the <a href="https://www.stockholmresilience.org/research/planetary-boundaries.html">2025 Planetary Health Check</a>](/plots/pbs_2025.png)

This repository is inspired by and forked from <a href="https://www.github.com/douxlit/Planetary-Boundary-Graph">douxlit's</a> repository. 
The aim of this code is to plot Earth's planetary boundaries following the <a href="https://www.stockholmresilience.org/research/planetary-boundaries.html">Planetary Health Check reports</a>. 

# Code description

The code comprises:
- planetary_boundary_classes.py which defines the classes
- pbs_2023.py which plots the 2025 planetary boundaries
- pbs_2025.py which plots the 2023 planetary boundaries

The planetary_boundary_classes.py script defines three classes:
1. ControlVariables:	to define the limits and impact of each control variable. 
2. PlanetaryBoundary:	to define each planetary boundary from its control variables. 
3. PlanetarySystem:	to define and plot the whole planetary boundaries system. 
