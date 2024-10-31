## Glacier model projection figures for the ICCI State of the Cryosphere report 2024

For the ICCI State of the Cryosphere report 2024, we decided to show simplified glacier projection figures that are available under [v2024_figures](v2024_figures/).

---

|![Figure:](v2024_figures/png/simple_icci_report_2024_median_iqr_oggm_glogem_pygem_temp_levels_global_v3_below45deg_final_no_lowess_fit_p50.png)|
|:--:|
|*Figure 1: Global glacier volume until 2300, relative to 2020. Black lines denote the past evolution from 2000-2019. The lines show the median and the shading shows the interquartile range (25th to 75th percentile). n corresponds to the amount of experiments (i.e. glacier model projections times amount of climate scenarios). In case of 1.5°C, there is just one climate scenario and just two glacier models that did projections for that climate scenario.*|

These figures are available for every region, and in addition for High Mountain Asia (i.e., the sum of Central Asia, South Asia West and South Asia East). 
The figures do not include anymore the LOWESS fit estimates from the ICCI report 2023 (see [README.md](README.md) for infos about the LOWESS fit). 
Code: [v2024_simplified_visualisation_choice.ipynb.ipynb notebook](v2024_simplified_visualisation_choice.ipynb).

***Short description of the new method:*** 
To show glacier mass projections until the year 2300, we group the climate scenarios (climate models and emission scenario combinations) into clusters of 1.5±0.2°C, 2.2±0.2°C and 2.8±0.2°C global temperature change in 2100. We show the median global temperature for each group. We chose the temperature levels of +1.5, +2.2 and +2.8°C because for these temperature levels the actual median within the ±0.2°C is equal to the given temperature level.

*Small methodological update: We use now the IPCC AR6 estimates instead of the IPCC SROCC estimates for the past warming between 1850-1900 and 1986-2005. That means, we assume now 0.69°C warming instead of the 0.63°C warming that we used for the v2023*


----

The advantages of these simplified v2024 figures are that the figures are cleaner and clearer. They have less lines and are easier to understand. In addition, the lines directly correspond to climate scenarios within that range. 


The disadvantages are that they are less scientifically robust. In the above v2024 simplified figures, we cannot really represent uncertainties stemming from the climate model choice, because there is only one climate scenario combinations near 1.5°C global temperature change in 2100. Similarly, for 2.2°C or 2.8°C global temperature change in 2100 there are only six or five climate scenario combinations.  In addition, the climate scenario that is chosen for the +1.5°C level (CMIP5, MPI-ESM-LR, rcp26) is not one that stabilises at 1.5°C but one that "overshoots", i.e. declines back to colder temperatures after 2100. This has something to do with specific climate model sensitivities and that RCP scenario. With this global cooling, and thus in some regions also regional cooling, we see growing glaciers in some fast-responding regions. 

|![Figure:](v2024_figures/png/v2024_simplified_climate_scenario_selection.png)|
|:--:|
|*Figure 2: Global mean temperature change of the used climate scenarios for the three temperature levels (within +/-0.2°C). Temperature change is described as 30-year rolling averages. The lines show the median and the shading shows the interquartile range (25th to 75th percentile). The shading shows the interquartile range (25th to 75th percentile). n corresponds here to the amount of climate scenarios and is thus lower than in the glacier projection figure.*|

---

To still get an overview over the different regions and to keep the eventually more scientific robustness of the LOWESS fit approach, we have created an overview figure of the different regions and their remaining glacier mass. 

|![Figure:](v2024_figures/png/boxplot_lowess_fit_region_overview.png)|
|:--:|
|*Figure 3: Overview of some selected glacier regions with the LOWESS fit estimates (see [README.md](README.md) for infos about the LOWESS fit) just for the year 2300. Boxplots show 5th, 25th, 50th, 75th and 95th percentiles. Note that we use here the IPCC AR6 estimate of past warming. *|
