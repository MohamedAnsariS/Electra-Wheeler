import pandas as pd
import numpy as np
import math
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# Load the distance matrix from an Excel file
file_path = r"C:\Users\smoha\Downloads\Copy_Andhradistance.xlsx"
df = pd.read_excel(file_path, index_col=0)  # Load with first column as index

# Convert distances from meters to kilometers
df = df / 1000
df[df == 0] = 0

# Load product-wise demand data
product_demand_df = pd.read_excel(r"C:\Users\smoha\Downloads\Andhra_Demand.xlsx", index_col=0)
demand = product_demand_df.sum(axis=1).tolist()
truck_capacity = 120
max_trucks = 200

def allocate_products(location_index, quantity):
    total_location_demand = product_demand_df.iloc[location_index].sum()
    if total_location_demand == 0:
        return {}
    product_distribution = {}
    for product in product_demand_df.columns:
        product_demand = product_demand_df.iloc[location_index][product]
        allocated = int((product_demand / total_location_demand) * quantity)
        product_distribution[product] = allocated
    return product_distribution

remaining_demand = demand.copy()
total_trucks_used = 0
distance_travelled = {}
initial_fulfillment_trucks = 0
optimization_trucks = 0

print("\n🚀 Initial Fulfillment with Full Truckloads:\n")

# Initial fulfillment phase
for location_index, location_demand in enumerate(remaining_demand):
    while remaining_demand[location_index] > truck_capacity and total_trucks_used < max_trucks:
        total_trucks_used += 1
        initial_fulfillment_trucks += 1
        allocated_products = allocate_products(location_index, truck_capacity)
        print(f"Truck {total_trucks_used} dispatched to {product_demand_df.index[location_index]} with 120 units ({', '.join([f'{v} {k}' for k, v in allocated_products.items() if v > 0])})")
        remaining_demand[location_index] -= truck_capacity
        
        # Calculate distance for initial fulfillment trucks
        depot_index = len(remaining_demand)  # Depot is the last node
        distance = df.iloc[location_index, depot_index] * 2  # Round trip distance
        distance_travelled[total_trucks_used - 1] = distance  # Store distance

def create_data_model(remaining_demand):
    num_vehicles = min(sum(math.ceil(d / truck_capacity) for d in remaining_demand), max_trucks - total_trucks_used)
    data = {
        'distance_matrix': df.values.tolist(),
        'demands': remaining_demand + [0],
        'vehicle_capacities': [truck_capacity] * num_vehicles,
        'num_vehicles': num_vehicles,
        'depot': len(remaining_demand),
        'cost_per_km': 500
    }
    return data

iteration = 0
while any(d > 0 for d in remaining_demand) and total_trucks_used < max_trucks:
    iteration += 1
    print(f"\n🚀 Iteration {iteration}: Running Optimization...\n")
    
    data = create_data_model(remaining_demand)
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)
    
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(data['distance_matrix'][from_node][to_node] * data['cost_per_km'])
    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]
    
    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(demand_callback_index, 0, data['vehicle_capacities'], True, 'Capacity')
    
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_parameters.time_limit.seconds = 1200  # Give it more time to optimize

    
    solution = routing.SolveWithParameters(search_parameters)
    place_names = list(df.index)
    
    if solution:
        print(f"Objective (Total Cost): {solution.ObjectiveValue()}")
        truck_quantities = {}
        
        for vehicle_id in range(data['num_vehicles']):
            if total_trucks_used >= max_trucks:
                break
            total_trucks_used += 1
            optimization_trucks += 1
            index = routing.Start(vehicle_id)
            route = []
            distance = 0
            while not routing.IsEnd(index):
                route.append(place_names[manager.IndexToNode(index)])
                next_index = solution.Value(routing.NextVar(index))
                distance += data['distance_matrix'][manager.IndexToNode(index)][manager.IndexToNode(next_index)]
                index = next_index
            route.append(place_names[data['depot']])
            distance_travelled[total_trucks_used - 1] = distance  # Store distance for optimized trucks
            
            if len(route) > 2:
                print(f"Optimized Route for truck {total_trucks_used - 12}: {route} (Distance: {distance:.2f} km)")
                quantities = []
                remaining_capacity = truck_capacity
                for location in route[1:-1]:
                    location_index = place_names.index(location)
                    fulfilled = min(remaining_demand[location_index], remaining_capacity)
                    product_allocation = allocate_products(location_index, fulfilled)
                    quantities.append((location, fulfilled, product_allocation))
                    remaining_capacity -= fulfilled
                    remaining_demand[location_index] -= fulfilled
                truck_quantities[vehicle_id] = quantities
        
        print("\n📦 Product Quantities Carried by Each Truck:") 
        for vehicle_id, quantities in truck_quantities.items():
            print(f"Truck {total_trucks_used - data['num_vehicles'] + vehicle_id + 1 - 12} carries:")
            for location, quantity, product_allocation in quantities:
                product_breakdown = ", ".join([f"{v} {k}" for k, v in product_allocation.items() if v > 0])
                print(f"  - {location}: {quantity} units ({product_breakdown})")
            print(f"  Total carried: {sum(q for _, q, _ in quantities)} units\n")
    
    else:
        print("No solution found in this iteration.")
        break

print("\n📊 Total Trucks Used:")
print(f"Initial Fulfillment Trucks: {initial_fulfillment_trucks}")
print(f"Optimization Trucks: {optimization_trucks - 12}")
print(f"Grand Total Trucks Used: {total_trucks_used - 12}")

total_distance = sum(distance_travelled.values())  # Sum all distances
objective_cost = total_distance  # Assign it as objective cost

print("\n🚛 Distance Travelled by Each Truck:")
truck_counter = 1
for truck, distance in distance_travelled.items():
    if distance > 0:  # Only show trucks with non-zero distances
        print(f"Truck {truck_counter}: {distance:.2f} km")
        truck_counter += 1

print(f"\n📌 Objective Cost (Total Distance): {objective_cost:.2f} km")

import pandas as pd
import numpy as np
import math

# Load the distance matrix from an Excel file
file_path = r"C:\Users\smoha\Downloads\Copy_Andhradistance.xlsx"
df = pd.read_excel(file_path, index_col=0)  # Load with first column as index

# Convert distances from meters to kilometers
df = df / 1000
df[df == 0] = 0

# Load product-wise demand data
product_demand_df = pd.read_excel(r"C:\Users\smoha\Downloads\Andhra_Demand.xlsx", index_col=0)
demand = product_demand_df.sum(axis=1).tolist()
truck_capacity = 120
max_trucks = 200

# Second method: Assign trucks based on demand directly
single_location_trucks_used = 0
single_location_distance_travelled = {}

def calculate_trucks_and_distance():
    global single_location_trucks_used
    for location_index, location_demand in enumerate(demand):
        trucks_needed = math.ceil(location_demand / truck_capacity)
        depot_index = len(demand)  # Depot is the last node
        distance = df.iloc[location_index, depot_index] * 2  # Round trip distance
        for _ in range(trucks_needed):
            single_location_trucks_used += 1
            single_location_distance_travelled[single_location_trucks_used] = distance
            print(f"Truck {single_location_trucks_used} dispatched to {product_demand_df.index[location_index]} (Distance: {distance:.2f} km)")

calculate_trucks_and_distance()

total_single_location_distance = sum(single_location_distance_travelled.values())

print("\n📊 Single Location Assignment Results:")
print(f"Total Trucks Used: {single_location_trucks_used}")
print(f"Total Distance Covered: {total_single_location_distance:.2f} km")

# Results from the first method (Optimized Routing)
optimized_trucks = total_trucks_used - 12
optimized_distance = objective_cost  # Total distance from optimized method

# Results from the second method (Direct Assignment)
direct_trucks = single_location_trucks_used
direct_distance = total_single_location_distance

# Calculate efficiency improvements
truck_reduction = ((direct_trucks - optimized_trucks) / direct_trucks) * 100

distance_reduction = ((direct_distance - optimized_distance) / direct_distance) * 100

# Print efficiency comparison
print("\n🚀 Efficiency Comparison:")
print(f"Total Trucks Used - Optimized Method: {optimized_trucks}")
print(f"Total Trucks Used - Direct Assignment: {direct_trucks}")
print(f"🚛 Truck Efficiency Improvement: {truck_reduction:.2f}%")

print("\n📏 Distance Covered - Optimized Method: {:.2f} km".format(optimized_distance))
print("📏 Distance Covered - Direct Assignment: {:.2f} km".format(direct_distance))
print(f"📉 Distance Efficiency Improvement: {distance_reduction:.2f}%")

# Interpretation of Results
if truck_reduction > 20 and distance_reduction > 30:
    print("\n✅ The optimized method provides a significant improvement in both truck usage and total distance covered.")
elif truck_reduction > 10 or distance_reduction > 20:
    print("\n⚠️ The optimized method is more efficient, but improvements could be made.")
else:
    print("\n❌ The optimization does not significantly reduce truck usage or distance. Consider refining the approach.")
