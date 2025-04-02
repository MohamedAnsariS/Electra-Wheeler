import geopandas as gpd
import networkx as nx
import pandas as pd
import numpy as np
from shapely.geometry import LineString
from geopy.distance import geodesic
from scipy.spatial import cKDTree
from joblib import Parallel, delayed

# 📌 Step 1: Load Road Network
print("🔄 Loading road network...")
roads = gpd.read_file("INDIA_NATIONAL_HIGHWAY.geojson")

# Convert MultiLineString to LineString if needed
if roads.geom_type.str.contains("MultiLineString").any():
    roads = roads.explode(index_parts=False)

# Ensure CRS is EPSG:4326 (Latitude/Longitude)
roads = roads.to_crs("EPSG:4326")

# 📌 Step 2: Create a Graph
print("🔄 Building NetworkX graph...")
G = nx.Graph()

# Add roads to the graph
for _, road in roads.iterrows():
    line = road.geometry
    if isinstance(line, LineString):
        coords = list(line.coords)
        for i in range(len(coords) - 1):
            node1, node2 = tuple(coords[i]), tuple(coords[i + 1])
            dist_km = geodesic(node1[::-1], node2[::-1]).kilometers  # (lon, lat) → (lat, lon)
            G.add_edge(node1, node2, weight=dist_km)

# 📌 Step 3: Load and Snap Locations
print("🔄 Loading locations...")
locations = gpd.read_file("snapped_locations_fixed.shp").to_crs(roads.crs)

# Extract location names and geometries
location_names = locations.iloc[:, 0].tolist()  # Assuming the first column is the location name
location_geometries = locations.geometry

# Extract all graph nodes for fast lookup
graph_nodes = np.array(G.nodes)
kdtree = cKDTree(graph_nodes)  # Use KDTree for fast nearest neighbor search

# Map each location to the nearest road network node
def find_nearest_node(point):
    _, idx = kdtree.query([point.x, point.y])
    return tuple(graph_nodes[idx])

nodes = {name: find_nearest_node(geom) for name, geom in zip(location_names, location_geometries)}

# 📌 Step 4: Compute Shortest Paths (Parallel Dijkstra)
print("🔄 Computing shortest paths...")

# Get node list for indexing
node_list = list(nodes.values())

def compute_dijkstra(source_node):
    """Compute shortest paths from a single source using Dijkstra."""
    shortest_paths = nx.single_source_dijkstra_path_length(G, source=source_node, weight="weight")
    return [shortest_paths.get(target, np.inf) for target in node_list]

# Parallelized computation
num_cores = -1  # Use all available cores
results = Parallel(n_jobs=num_cores)(
    delayed(compute_dijkstra)(node) for node in node_list
)

# 📌 Step 5: Convert to DataFrame and Save
print("🔄 Saving distance matrix...")

# Create DataFrame with location names as index and columns
distance_matrix = pd.DataFrame(results, index=location_names, columns=location_names)

output_file = "distance_matrix_km_parallel.csv"
distance_matrix.to_csv(output_file)

print(f"✅ Distance matrix saved to {output_file}")
