#%%Import necessary libraries
import xarray as xr # - Used to open and process data from NetCDF files
import pandas as pd # - Used to read and manipulate data tables and perform data analysis
import numpy as np # - Used for numerical operations and mathematical operations
from tqdm import tqdm # - Used to generate a progress bar for loops in Python
import matplotlib.pyplot as plt # - used to create plots and visuals
import plotly.express as px
import seaborn as sns
from scipy.interpolate import UnivariateSpline


#%%Function to read and process precipitation data from a NetCDF file
def get_data(var):
    # Open NetCDF file and convert specified variable to DataFrame
    # 'var' is the variable name in the NetCDF file, typically representing precipitation data
        # data = Open the dataset to the path in which NCDF files are stored
    data = xr.open_dataset(r"C:\Users\alfredo.serrano.fig1\Desktop\Flood\Code\pr_day_MIROC6_ssp245_r1i1p1f1_gn_20200101-21001231_v20191016.nc")
    df = data[var].to_dataframe()
    df = df.reset_index()
    # Adjust longitudes to a standard format (-180 to 180 degrees)
    df["lon"] = ((df["lon"]+180)%360)-180
    return df

#%% Function to read exposure data from a CSV file
def get_exposure():
    # Read exposure data and select relevant columns
    # 'Value' represents the asset value, 'Latitud' and 'Longitud' are the geographical coordinates
    return pd.read_excel("Collateral_Columns.xlsx")

#%% Function to read impact functions (damage curves) from an Excel file
def get_impf(haz):
    # Read damage curves for the specified hazard (e.g., flood)
    # 'haz' is the hazard type, 'intensity' is the environmental intensity measure, and 'mdr' is mean damage ratio
    fun = pd.read_excel("Damage_Curves_Assets.xlsx")
    fun = fun[fun["peril"]== haz] #ADJUST CURVES!!!
    return (fun["intensity"],fun["mdr"])

#%% Setting parameters for the analysis
start_date = 2023 # Start year for the analysis - 2023
end_date = 2100 # End year for the analysis - 2100
radius = 1  # Radius around each exposure point for data consideration
var = "pr"  # Variable name for precipitation in the dataset
event = "Flood"
threshold = 50  # Precipitation threshold for flood event in mm/day - Changed from "20" to "50"


#%% Retrieve precipitation data
df = get_data(var)

#%% Retrieve exposure data
exp = get_exposure()

#%% Retrieve impact function for the flood event
impf_x, impf_y = get_impf(event)

#%% Extract year from time data and filter based on the specified date range
df["year"] = df["time"].dt.year
df = df[(df["year"] >= start_date) & (df["year"] <= end_date)]


#%% Initialize DataFrame to store impact results
impacts = pd.DataFrame()

#%% Iterate over each exposure point to calculate impact
for i in tqdm(range(exp.shape[0])):
    val, lat, lon = exp.loc[i]
    # Filter data within the specified radius around the exposure point
    aux = df[(df["lat"] >= lat-radius) & (df["lat"] <= lat+radius) & (df["lon"] >= lon-radius) & (df["lon"] <= lon+radius)]
    # Group by time and calculate mean precipitation
    aux = aux.groupby("time").mean().reset_index()
    # Convert precipitation to a daily scale (specific to this dataset)
    aux[var] = aux[var]
    # Identify days exceeding the flood event threshold
    aux[var + "_event"] = aux[var]
    aux.loc[aux[var+"_event"] < threshold, var+"_event"] = np.nan
    # Calculate yearly statistics
    res = pd.DataFrame()
    res["Mean"] = aux.groupby("year").mean()[var]
    res["Mean_event"] = aux.groupby("year").mean()[var+"_event"]
    res["Exceeds_Threshold"] = aux.groupby("year").count()[var+"_event"]
    # Calculate impact using the impact function
    # Interpolation is used to find the damage ratio for the mean event precipitation
    res["Impact"] = np.interp(res["Mean_event"],impf_x,impf_y)
    # Adjust impact based on the number of exceedance events
    res["Impact"] = 1-(1-res["Impact"])**res["Exceeds_Threshold"]
    # Scale impact by the value of the exposure
    res["Impact"] = res["Impact"] * val
    # Add location and ID information for tracking
    res["Latitutde"] = lat
    res["Longitud"] = lon
    res["id"] = i
    res["Ccol collateral"] = val # added by CS
    # Append results to the impacts DataFrame
    impacts = pd.concat([impacts,res])

# #%% Function to apply spline smoothing
# def smooth_column(data, column_name, s=0.5):
#     """
#     Apply spline smoothing to a column.
#     :param data: DataFrame containing the data.
#     :param column_name: Name of the column to smooth.
#     :param s: Smoothing factor.
#     :return: Smoothed column.
#     """
#     spline = UnivariateSpline(data.index, data[column_name], s=s)
#     return spline(data.index)

# #%% Apply smoothing to the specified columns
# impacts['Mean_smoothed'] = smooth_column(impacts, 'Mean')
# impacts['Mean_event_smoothed'] = smooth_column(impacts, 'Mean_event')
# impacts['Exceeds_Threshold_smoothed'] = smooth_column(impacts, 'Exceeds_Threshold')
# impacts['Impact_smoothed'] = smooth_column(impacts, 'Impact')


#%% Reset index and export results to a CSV file
impacts = impacts.reset_index()
impacts.to_excel("Flood_4.5_MIROC6.xlsx") # Importing results into a CSV file - Into directory where we want the results to be




