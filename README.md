# ESG---Physical-Risk---Flood_Hazard
This repository contains Python scripts for evaluating the physical risk due to flood hazards. The methodology leverages climate model outputs, exposure data, and damage curves to assess potential financial impacts under future climate scenarios.

## Methodology Overview

The physical risk assessment process involves several key steps:

1. **Data Preparation**: Utilize climate model outputs (e.g., precipitation data from the MIROC6 model) and exposure data to set the analysis framework.
2. **Impact Assessment**: Apply damage curves (impact functions) to the prepared data to estimate the financial impact of flood events on exposed assets.
3. **Result Compilation**: Aggregate and compile the impact assessments to provide a comprehensive view of potential financial risks due to flood hazards.

### Important Note on Data Sources

The analysis requires precipitation data from climate models, which are not included in this repository. Specifically, the MIROC6 model data for precipitation can be obtained from the [CMIP6 dataset hosted by Copernicus](https://cds.climate.copernicus.eu/cdsapp#!/search?type=dataset). Users are encouraged to download the required NetCDF files directly from this source to ensure they have the most up-to-date and accurate data for their analysis.

The selection pattern: Temporal Resolution Daily > Experiment ssp2-4.5 > Variable precipitation > Model MIROC6(Japan) > Years 2023 - 2100 > All months > All days > Adjust sub-extraction region - USA:
North 49.38
West -125
East -66.93
South 24.39

## Code Overview

The provided Python scripts perform the following functions:

- **Data Reading and Processing**: Open and process NetCDF files containing climate model outputs, specifically focusing on precipitation data.
- **Exposure and Impact Functions**: Read exposure data and impact functions from external files to assess the vulnerability of assets to flood events.
- **Impact Calculation**: Iterate over exposure points to calculate the impact based on the specified damage curves and climate data.
- **Result Export**: Compile and export the calculated impacts into an Excel file for further analysis and review.

### Libraries Used

- `xarray`: For handling NetCDF files and processing climate model data.
- `pandas`: For data manipulation and analysis.
- `numpy`: For numerical operations.
- `matplotlib`, `plotly.express`, `seaborn`: For data visualization.
- `scipy`: For statistical functions, including spline smoothing to smooth the results.

### Key Functions

- `get_data(var)`: Reads and processes precipitation data from a specified NetCDF file.
- `get_exposure()`: Reads exposure data from an external file.
- `get_impf(haz)`: Reads impact functions (damage curves) for the specified hazard type from an external file.
- `smooth_column(data, column_name, s)`: Applies spline smoothing to a specified column in the DataFrame to smooth the results.

## Running the Analysis

To run the analysis, ensure you have the required climate model output files and the exposure data file in the specified directory. Adjust the script parameters as needed to match your analysis scenario and data file paths.



