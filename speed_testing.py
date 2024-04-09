import json
import numpy as np
import timeit
from scipy import stats
import simulate

def run_simulation_trials(num_trials=10):
    times = timeit.repeat(stmt=lambda: simulate.main(plot=False, verbose=False),
                          repeat=num_trials, number=1)
    return np.array(times)

def save_results(times, filepath='simulation_performance.json'):
    data = {'mean': np.mean(times), 'std_dev': np.std(times)}
    with open(filepath, 'w') as file:
        json.dump(data, file)

def load_previous_results(filepath='simulation_performance.json'):
    try:
        with open(filepath, 'r') as file:
            data = file.read()
            # Check if the file is not empty
            if data:
                return json.loads(data)
            else:
                return None
    except FileNotFoundError:
        return None

def calculate_p_value(new_times, prev_data):
    if prev_data is not None:
        _, p_value = stats.ttest_ind_from_stats(mean1=prev_data['mean'], std1=prev_data['std_dev'], nobs1=len(new_times),
                                                mean2=np.mean(new_times), std2=np.std(new_times), nobs2=len(new_times))
        return p_value
    return None

def main():
    num_trials = 20
    filepath = 'simulation_performance.json'

    # Run simulation trials and get timing
    new_times = run_simulation_trials(num_trials)

    # Load previous results for comparison
    prev_data = load_previous_results(filepath)

    new_mean = np.mean(new_times)
    new_std_dev = np.std(new_times)

    # Initialize variables for old data to None
    old_mean = None
    percent_change = None

    # Check if previous data exists and calculate the old mean and percent change
    if prev_data:
        old_mean = prev_data['mean']
        # Calculate percent change in mean execution time
        # Note: To avoid division by zero error, check if old_mean is not zero
        percent_change = ((new_mean - old_mean) / old_mean * 100) if old_mean != 0 else None

    # Output results including the old mean and percent change with color
    print(f"New simulation mean time: {new_mean} seconds")
    if old_mean is not None:
        print(f"Old simulation mean time: {old_mean} seconds")
        if percent_change is not None:
            color_code = "\033[92m" if percent_change < 0 else "\033[91m"  # Green for reduction, Red for increase
            reset_code = "\033[0m"  # Reset to default color
            print(f"Percent change in mean execution time: {color_code}{percent_change:.2f}%{reset_code}")

    # Calculate p-value if previous data exists
    p_value = None
    if prev_data:
        p_value = calculate_p_value(new_times, prev_data)
        print(f"P-value for change in simulation speed: {p_value}")
        if p_value < 0.05:
            print(f"The change in simulation speed is statistically significant.")
        else:
            print(f"The change in simulation speed is not statistically significant.")

    # Save new results
    save_results(new_times, filepath)

if __name__ == "__main__":
    main()