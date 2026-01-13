🛰️Urbanization Change Detection Using Satellite Imagery:-

Project Description:This project analyzes urbanization changes over time using satellite imagery and remote sensing techniques. It focuses on identifying urban growth patterns by computing spectral indices, performing clustering-based classification, and analyzing temporal trends from multi-year satellite data.

AIM:
  - Analyze satellite imagery to detect urban and non-urban regions
  - Measure changes in urbanization over time
  - Extract meaningful insights using remote sensing indices
  - Support urban growth analysis through data-driven techniques

DATASET:
Source: Landsat satellite imagery (via Google Earth Engine / public satellite data)
Type: Multi-band satellite images
Time Frame: Multi-year imagery for temporal comparison

MEETHODOLOGY:
1. Data Preprocessing
Satellite image acquisition
Band selection and normalization
Noise and cloud handling (if applicable)

2. Remote Sensing Indices
Computed indices to distinguish land cover types:
NDVI – Vegetation detection
NDBI – Built-up (urban) area detection
MNDWI – Water body detection
Urban Index / BAEI – Urban feature enhancement

3. Urban Classification
Applied K-Means clustering to classify regions into urban and non-urban zones based on spectral features.

4. Change Detection
Compared index values and classified maps across different years to identify urban expansion trends.

5. Trend Analysis (Optional)
Time-series and regression analysis to study urban growth patterns over time.


TECHNOLOGIES USED:
Python
Jupyter Notebook
Remote Sensing Indices (NDVI, NDBI, MNDWI)
Machine Learning: K-Means Clustering
Satellite Data: Landsat Imagery
Data Visualization Libraries: Matplotlib, Seaborn

KEY OUTCOMES:
Identified urban growth and land-use change patterns
Classified urban vs non-urban regions using satellite data
Visualized temporal changes in urbanization

USE CASES:
Urban planning and development analysis
Environmental and land-use monitoring
