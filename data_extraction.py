# To import an area from one particular region
!pip install earthengine-api geemap

# ================================
# Earth Engine Initialization
# ================================
import ee

ee.Authenticate()
ee.Initialize(project='urbanization-489507')

# ================================
# Regions and coordinates
# ================================
regions = {

    "Bangalore": {
        "folder": "Bangalore_Images",
        "coords": [
            [77.7300, 12.9500],
            [77.8100, 12.9500],
            [77.8100, 13.0200],
            [77.7300, 13.0200]
        ]
    },

    "Gurgaon": {
        "folder": "Gurgaon_Images",
        "coords": [
            [77.0200, 28.4100],
            [77.1100, 28.4100],
            [77.1100, 28.4800],
            [77.0200, 28.4800]
        ]
    },

    "Godavari": {
        "folder": "Godavari_Images",
        "coords": [
            [81.2725, 16.8500],  # southwest
            [81.4073, 16.8500],  # southeast
            [81.4073, 16.9848],  # northeast
            [81.2725, 16.9848]   # northwest
         ]
    }
}

# ================================
# Year range
# ================================
startYear = 2014
endYear = 2024
years = list(range(startYear, endYear + 1))

# ================================
# Landsat dataset
# ================================
dataset = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')

# ================================
# Cloud mask function
# ================================
def maskL8sr(image):

    qaPixel = image.select('QA_PIXEL')

    mask = qaPixel.bitwiseAnd(1 << 3).eq(0) \
           .And(qaPixel.bitwiseAnd(1 << 4).eq(0))

    return image.updateMask(mask)

dataset = dataset.map(maskL8sr)

# ================================
# Export function
# ================================
def exportBandsForRegion(region_name, region_info):

    customBounds = ee.Geometry.Polygon([region_info["coords"]])
    folder = region_info["folder"]

    for year in years:

        startDate = ee.Date.fromYMD(year, 1, 1)
        endDate = ee.Date.fromYMD(year, 5, 31)

        yearlyData = dataset.filterBounds(customBounds) \
                            .filterDate(startDate, endDate) \
                            .median()

        scaled = yearlyData.select(
            ['SR_B2','SR_B3','SR_B4','SR_B5','SR_B6','SR_B7']
        ).multiply(0.0000275).add(-0.2)

        bands = ['SR_B2','SR_B3','SR_B4','SR_B5','SR_B6','SR_B7']

        for band in bands:

            filename = f"Landsat8_{region_name}_{year}_8{band}"

            task = ee.batch.Export.image.toDrive(
                image = scaled.select(band),
                description = filename,
                folder = folder,
                fileNamePrefix = filename,
                region = customBounds,
                scale = 30,
                maxPixels = 1e13
            )

            task.start()
            print(f"Export started: {filename}")


# ================================
# Run for all regions
# ================================
for region_name, region_info in regions.items():
    exportBandsForRegion(region_name, region_info)

print("All export tasks started.")
