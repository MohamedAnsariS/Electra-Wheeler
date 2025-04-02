import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Load the shapefile
shapefile_path = r'C:\Users\smoha\Downloads\India_State_Boundary.shp'
gdf = gpd.read_file(shapefile_path)

# Inspect available columns
print(gdf.columns)
print(gdf['State_Name'].unique())

# Replace 'State_Name' with the correct column name if different
correct_column_name = 'State_Name'  # Update if necessary

# Define the zone classification function
def classify_zone(state):
    cluster_1 = ['Maharashtra', 'Goa', 'Puducherry', 'Karnataka', 'Kerala', 'Tamilnadu', 'Andhra Pradesh', 'Telengana']
    cluster_2 = ['Gujarat', 'Chandigarh', 'Daman and Diu and Dadra and Nagar Haveli', 'Madhya Pradesh', 'Rajasthan', 
                 'Delhi', 'Uttar Pradesh', 'Haryana', 'Punjab', 'Himachal Pradesh', 'Uttarakhand', 'Jammu and Kashmir', 'Ladakh']
    cluster_3 = ['Bihar', 'Jharkhand', 'Chhattishgarh', 'Odisha', 'West Bengal', 'Assam', 'Meghalaya', 'Sikkim', 
                 'Arunachal Pradesh', 'Tripura', 'Mizoram', 'Manipur', 'Nagaland']
    
    if state in cluster_1:
        return 'Cluster 1'
    elif state in cluster_2:
        return 'Cluster 2'
    elif state in cluster_3:
        return 'Cluster 3'
    else:
        return 'Unknown'

# Apply the classification
gdf['Cluster'] = gdf[correct_column_name].apply(classify_zone)

# Ensure the coordinate system is set to WGS 84 (latitude and longitude)
if gdf.crs is None or gdf.crs.to_epsg() != 4326:
    gdf = gdf.to_crs(epsg=4326)

# Save the updated shapefile with correct CRS (optional)
gdf.to_file("output_clustered_shapefile.shp")

print("Classification completed successfully.")

# Define the main warehouse coordinates and labels
warehouse_coords = [
    (76.92227644, 13.45334167),  
    (74.87423542, 26.5074875),
    (85.78119663, 23.37459768)
]
warehouse_labels = ["Karnataka", "Rajasthan", "Jharkhand"]

# Define the sub-warehouse coordinates and labels
sub_warehouse1_coords = [
    (75.62511871, 18.937502),
    (76.34655176, 10.18782403),
    (78.74456977, 11.64121535),
    (81.17365302, 16.2333507)
]
sub_warehouse2_coords = [
    (72.28780561, 22.19407754),
    (77.57307162, 23.46433668),
    (77.06788598, 28.72792649),
    (80.08529855, 27.03942092),
    (75.70249535, 31.05376667),
    (78.07500434, 30.26344936),
    (75.10666796, 33.06470879)
]
sub_warehouse3_coords = [
    (85.28562989, 25.70584109),
    (81.92763132, 21.57723545),
    (84.84285466, 20.42726355),
    (87.95297717, 23.14238258),
    (92.56831994, 26.02158502)
]

# Convert coordinates to GeoDataFrames
warehouse_gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lon, lat in warehouse_coords], crs="EPSG:4326")
sub_warehouse1_gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lon, lat in sub_warehouse1_coords], crs="EPSG:4326")
sub_warehouse2_gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lon, lat in sub_warehouse2_coords], crs="EPSG:4326")
sub_warehouse3_gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lon, lat in sub_warehouse3_coords], crs="EPSG:4326")

# Plot the clusters with real-life latitude and longitude
fig, ax = plt.subplots(figsize=(12, 10))
gdf.plot(column='Cluster', cmap='viridis', legend=True, edgecolor='black', ax=ax, alpha=0.6)

# Plot main warehouses in red
warehouse_gdf.plot(ax=ax, color='red', markersize=100, marker='o', label="Main Warehouses")

# Plot sub-warehouses in different colors
sub_warehouse1_gdf.plot(ax=ax, color='blue', markersize=80, marker='s', label="Southern Zone")
sub_warehouse2_gdf.plot(ax=ax, color='green', markersize=80, marker='s', label="Northern Zone")
sub_warehouse3_gdf.plot(ax=ax, color='yellow', markersize=80, marker='s', label="Eastern Zone")

# Add labels for warehouses
for (lon, lat), label in zip(warehouse_coords, warehouse_labels):
    plt.text(lon, lat, label, fontsize=10, ha='right', color='red', fontweight='bold')

# Define specific names for sub-warehouses
sub_warehouse1_names = [
    "Maharasthra(Goa)", "Kerala(Mahe)", "Tamilnadu(Puducherry)", "Andhra(Yanam)"
]
sub_warehouse2_names = [
    "Gujarat", "Madhya", "Haryana(Delhi)", "Uttar Pradesh", "Punjab(Chandigarh)", "Uttarakhand(Himachal)", "Kashmir(Ladakh)"
]
sub_warehouse3_names = [
    "Bihar", "Chattisgarh", "Odisha", "Bengal", "Northeast"
]

# Add specific labels for sub-warehouse 1 locations
for (lon, lat), name in zip(sub_warehouse1_coords, sub_warehouse1_names):
    plt.text(lon, lat, name, fontsize=8, ha='right', color='blue', fontweight='bold')

# Add specific labels for sub-warehouse 2 locations
for (lon, lat), name in zip(sub_warehouse2_coords, sub_warehouse2_names):
    plt.text(lon, lat, name, fontsize=8, ha='right', color='green', fontweight='bold')

# Add specific labels for sub-warehouse 3 locations
for (lon, lat), name in zip(sub_warehouse3_coords, sub_warehouse3_names):
    plt.text(lon, lat, name, fontsize=8, ha='right', color='yellow', fontweight='bold')

plt.title('Warehouse Locations')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.legend()
plt.show()

# Load the shapefile
shapefile_path = r'C:\Users\smoha\Downloads\India_State_Boundary.shp'
gdf = gpd.read_file(shapefile_path)

# Check the current CRS and convert to WGS 84 if necessary
if gdf.crs is None or gdf.crs.to_epsg() != 4326:
    gdf = gdf.to_crs(epsg=4326)

# Define the zone classification function
def classify_zone(state):
    cluster_1 = ['Maharashtra', 'Goa', 'Puducherry', 'Karnataka', 'Kerala', 'Tamilnadu', 'Andhra Pradesh', 'Telengana']
    cluster_2 = ['Gujarat', 'Chandigarh', 'Daman and Diu and Dadra and Nagar Haveli', 'Madhya Pradesh', 'Rajasthan', 
                 'Delhi', 'Uttar Pradesh', 'Haryana', 'Punjab', 'Himachal Pradesh', 'Uttarakhand', 'Jammu and Kashmir', 'Ladakh']
    cluster_3 = ['Bihar', 'Jharkhand', 'Chhattishgarh', 'Odisha', 'West Bengal', 'Assam', 'Meghalaya', 'Sikkim', 
                 'Arunachal Pradesh', 'Tripura', 'Mizoram', 'Manipur', 'Nagaland']
    
    if state in cluster_1:
        return 'Cluster 1'
    elif state in cluster_2:
        return 'Cluster 2'
    elif state in cluster_3:
        return 'Cluster 3'
    else:
        return 'Unknown'

# Identify the correct column name for state names
correct_column_name = 'State_Name'  # Update if necessary based on printed columns

# Apply the classification
gdf['Cluster'] = gdf[correct_column_name].apply(classify_zone)

# Define the city coordinates (longitude, latitude)
city_coordinates = {
    "Ranipet": (79.2840, 12.9442),
    "Hosur": (77.8326, 12.7365),
    "Akurdi": (73.7720, 18.6440),
    "Jaipur": (75.7789, 26.9221),
    "Chakan": (73.8635, 18.7606),
    "Bhiwadi": (76.8606, 28.2104),
    "Raipur": (81.6296, 21.2514),
    "Ludhiana": (75.8500, 30.9000),
    "Chittoor": (79.1003, 13.2172),
    "Ahmednagar": (74.7496, 19.0952),
    "Manesar": (76.9360, 28.3542),
    "Kolar": (78.1291, 13.1365),
    "Bengaluru": (77.5946, 12.9716),
    "Ahmedabad": (72.5714, 23.0225),
    "Baddi": (76.7914, 30.9578),
    "Krishnagiri": (78.2137, 12.5186),
    "Sangareddy": (78.0867, 17.6244),
    "Hyderabad": (78.4867, 17.3850),
    "Mysore": (76.6394, 12.2958),
    "Dharmapuri": (78.1587, 12.1276),
    "Nalagrah": (76.7200, 31.0400),
    "Vadodara": (73.1812, 22.3072),
    "Deoghar": (86.6952, 24.4855)
}

# Convert coordinates to GeoDataFrame
city_points = [Point(lon, lat) for lon, lat in city_coordinates.values()]
city_gdf = gpd.GeoDataFrame(geometry=city_points, crs="EPSG:4326")

# Plot the clusters with city locations
fig, ax = plt.subplots(figsize=(12, 10))
gdf.plot(column='Cluster', cmap='viridis', legend=True, edgecolor='black', ax=ax, alpha=0.6)

# Plot city points
city_gdf.plot(ax=ax, color='red', markersize=50, label="Plants")

# Add city labels
for city, (lon, lat) in city_coordinates.items():
    plt.text(lon, lat, city, fontsize=8, ha='right', color='blue', fontweight='bold')

# Add title and labels
plt.title("Manufacturing plants location in India")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)
plt.legend()
plt.show()
