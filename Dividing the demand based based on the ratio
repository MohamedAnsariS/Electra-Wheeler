import numpy as np

def adjust_numbers(shares, total):
    """
    Adjust numbers based on percentage shares to ensure the sum matches the total.

    Args:
        shares (list of float): Percentage shares (not required to sum to 100).
        total (int): The total number to divide among shares.

    Returns:
        list of int: Adjusted integer values for each share.
    """
    # Normalize shares to ensure they sum to 100%
    shares = np.array(shares)
    normalized_shares = shares / shares.sum() * 100

    # Step 1: Calculate initial values by applying the percentage and rounding down
    exact_values = normalized_shares * total / 100
    rounded_values = np.floor(exact_values).astype(int)

    # Step 2: Calculate the difference between the target total and the sum of rounded values
    diff = total - np.sum(rounded_values)

    # Step 3: Adjust the values to minimize the percentage impact
    fractional_parts = exact_values - rounded_values

    if diff > 0:
        # Increase values for the shares with the largest fractional parts
        indices = np.argsort(-fractional_parts)
    elif diff < 0:
        # Decrease values for the shares with the smallest fractional parts
        indices = np.argsort(fractional_parts)

    for i in range(abs(diff)):
        rounded_values[indices[i]] += 1 if diff > 0 else -1

    # Return the adjusted values
    return rounded_values.tolist()
# Example usage
shares = [
    0.07031112674, 0.1230444718, 55.80945685, 24.36280541, 12.12866936,
    0.8788890842, 0.1582000352, 0.01757778168, 0.1406222535, 6.275268061,
    0.03515556337
]
totals = [42, 16, 0, 5, 7, 0, 20, 1, 3, 0, 0, 4, 0, 0, 0, 3, 198, 6, 0, 2, 0, 0, 34, 0, 25]

# Calculate and print results
for total in totals:
    result = adjust_numbers(shares, total)
    print(f"Total: {total}, Adjusted Values: {result}, Sum: {sum(result)}")
