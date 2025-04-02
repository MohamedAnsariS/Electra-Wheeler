import pulp
import math

# Warehouses and products
warehouses = ['Ranipet', 'Hosur', 'Akurdi', 'Jaipur', 'Chakan', 'Bhiwadi', 'Raipur', 'Ludhiana' , 'Chittoor','Ahmednagar', 'Manesar', 'Kolar', 'Bengaluru', 'Ahmedabad', 'Baddi', 'Krishnagiri', 'Sangareddy', 'Hyderabad', 'Mysore', 'Dharmapuri', 'Nalagarh', 'Vadodara']
products = ['Ather', 'Bajaj', 'Battre', 'Bgauss', 'Bounce', 'Godawari', 'Greaves', 'Hero Elec', 'Hero', 'Hop', 'Kinetic', 'Lectrix', 'Numeros', 'Oben', 'Odysse', 'Okaya', 'Ola', 'Pur', 'Quantum', 'Revolt', 'River', 'Simple', 'TVS', 'Ultra', 'Ward']
Destinations = ['Kallakurchi', 'Bengaluru1', 'Beed', 'Ajmer', 'Rajouri Garden', 'Baloda Bazaar', 'Ludhiana1', 'Bhavnagar', 'Machilipatnam']
# Supply at warehouses (units per product)
supply = {
    'Ranipet': {'Greaves': 2536},
    'Hosur': {'Ather': 9374, 'Simple': 18, 'TVS': 8300},
    'Akurdi': {'Bajaj': 10888},
    'Jaipur': {'Battre': 287, 'Hop': 25},
    'Chakan': {'Bgauss': 1485},
    'Bhiwadi': {'Bounce': 286},
    'Raipur': {'Godawari': 35},
    'Ludhiana': {'Hero Elec': 419},
    'Chittoor': {'Hero': 1492},
    'Ahmednagar': {'Kinetic': 820},
    'Manesar': {'Lectrix': 507, 'Revolt': 533},
    'Kolar': {'Numeros': 18,},
    'Bengaluru': {'Oben': 0, 'River': 43, 'Ultra':13},
    'Ahmedabad': {'Odysse': 11},
    'Baddi': {'Okaya': 581},
    'Krishnagiri': {'Ola': 32407},
    'Sangareddy': {'Pur': 620},
    'Hyderabad': {'Quantum': 383},
    'Mysore': {'TVS': 4150},
    'Dharmapuri': {'Simple': 17},
    'Nalagarh': {'TVS': 2905},
    'Vadodara': {'Ward': 977}
}

# Demand at warehouses (units per product)
demand = {
    'Kallakurchi': {'Greaves': 2536, 'Hero': 1492, 'Simple': 17},
    'Bengaluru1': {'Ather': 9374, 'Numeros': 18, 'Oben': 0, 'Ola': 32407, 'River': 43, 'Simple': 18, 'TVS': 12450, 'Ultra': 13},
    'Beed': {'Bajaj': 10888, 'Bgauss': 1485, 'Kinetic': 820, 'Pur': 620},
    'Ajmer': {'Battre': 287, 'Hop': 25},
    'Rajouri Garden': {'Bounce': 286, 'Lectrix': 507, 'Revolt': 533},
    'Baloda Bazaar': {'Godawari': 35},
    'Ludhiana1': {'Hero Elec': 419, 'Okaya': 581, 'TVS': 2905},
    'Bhavnagar': {'Odysse': 11, 'Ward': 977},
    'Machilipatnam': {'Quantum': 383},
}

# Check supply and demand balance
total_supply = {p: 0 for p in products}
total_demand = {p: 0 for p in products}

# Calculate total supply for each product
for wh, products_supplied in supply.items():
    for p, qty in products_supplied.items():
        total_supply[p] += qty

# Calculate total demand for each product
for dest, products_demanded in demand.items():
    for p, qty in products_demanded.items():
        total_demand[p] += qty

# Print supply and demand balance
print("\nSupply and Demand Balance:")
for p in products:
    print(f"Product: {p}")
    print(f"  Total Supply: {total_supply[p]}")
    print(f"  Total Demand: {total_demand[p]}")
    if total_supply[p] >= total_demand[p]:
        print("  Balance: Sufficient Supply")
    else:
        print("  Balance: Insufficient Supply")

# Truck capacities
truck_capacities = [80, 120, 160, 240]
# Create the LP problem
prob = pulp.LpProblem("Warehouse_to_Destination_Transport_with_Trucks", pulp.LpMinimize)

# Decision variables for transport from warehouses to destinations
x_wh_to_dest = pulp.LpVariable.dicts(
    "Transport_WH_to_Dest",
    (warehouses, Destinations, products),
    lowBound=0,
    cat='Integer'
)

# Objective Function: Minimize total transport cost (can be adjusted for truck usage)
prob += pulp.lpSum(
    x_wh_to_dest[wh][d][p] for wh in warehouses for d in Destinations for p in products
), "MinimizeTransport"

# Constraints:

# 1. Supply constraints at each warehouse
for wh in warehouses:
    for p in products:
        prob += (
            pulp.lpSum(x_wh_to_dest[wh][d][p] for d in Destinations) <= supply.get(wh, {}).get(p, 0)
        ), f"SupplyConstraint_{wh}_{p}"

# 2. Demand constraints at each destination
for d in Destinations:
    for p in products:
        prob += (
            pulp.lpSum(x_wh_to_dest[wh][d][p] for wh in warehouses) >= demand.get(d, {}).get(p, 0)
        ), f"DemandConstraint_{d}_{p}"

# Solve the problem
prob.solve()

# Output
if pulp.LpStatus[prob.status] == 'Optimal':
    print("\nOptimal Warehouse-to-Destination Transport Solution (Combined Products with Breakdown):")
    for wh in warehouses:
        for d in Destinations:
            # Calculate total combined units for the warehouse-destination pair
            total_units = sum(
                pulp.value(x_wh_to_dest[wh][d][p]) or 0 for p in products
            )
            if total_units > 0:
                # Prepare breakdown of units by product
                breakdown = []
                for p in products:
                    val = pulp.value(x_wh_to_dest[wh][d][p])
                    if val and val > 0:
                        breakdown.append(f"{int(val)} {p}")
                
                breakdown_str = ", ".join(breakdown)
                print(f"  {wh} to {d}: {int(total_units)} total units ({breakdown_str})")
                
                # Calculate trucks needed
                num_240_trucks = total_units // 240
                remainder = total_units % 240
                trucks_used = []
                
                # Use largest trucks for remainder
                if remainder > 0:
                    if remainder > 120:
                        trucks_used.append("1 truck of capacity 240")
                    elif remainder > 80:
                        trucks_used.append("1 truck of capacity 120")
                    elif remainder > 40:
                        trucks_used.append("1 truck of capacity 80")
                    else:
                        trucks_used.append("1 truck of capacity 40")
                
                if num_240_trucks > 0:
                    trucks_used.insert(0, f"{num_240_trucks} truck(s) of capacity 240")
                
                print(f"    Trucks used: {', '.join(trucks_used)}")
else:
    print(f"Problem status: {pulp.LpStatus[prob.status]}")
