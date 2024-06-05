import numpy as np
from scipy.stats import norm

def calculate_std_dev_for_30_percent_within_range(mean, lower_limit, upper_limit, desired_percentage=0.3):
    # Mean is given
    mu = mean

    # Calculate the z-scores for the desired range
    z_lower = norm.ppf((1 - desired_percentage) / 2)
    z_upper = norm.ppf(1 - (1 - desired_percentage) / 2)

    # Calculate the actual limits based on the desired percentage
    limit_range = upper_limit - lower_limit

    # Calculate the standard deviation based on z-scores and the desired limits
    std_dev = limit_range / (z_upper - z_lower)

    return std_dev

# Parameters
mean = 5
lower_limit = 4
upper_limit = 6

# Calculate appropriate standard deviation
std_dev = calculate_std_dev_for_30_percent_within_range(mean, lower_limit, upper_limit)

# Generate a single random number
random_number = np.random.normal(mean, std_dev)
print(std_dev)
print("Random number:", random_number)
