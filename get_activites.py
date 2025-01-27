import json
from pathlib import Path

data = []
directory = "./HealthData/Sleep"
pathlist = Path(directory).glob('**/*.json')

# Read all JSON files
for path in pathlist:
    with open(path) as file:
        sleepData = json.load(file)  # Load the entire JSON file
        HRV = float(sleepData["avgOvernightHrv"])  # Ensure HRV is a float
        RHR = int(sleepData["restingHeartRate"])   # Ensure RHR is an integer
        calendarDate = sleepData["dailySleepDTO"]["calendarDate"]
        
        # Append to data list
        data.append({"HRV": HRV, "RHR": RHR, "calendarDate": calendarDate})
        print("HR: ", RHR, "HRV: ", HRV, "Date: ", calendarDate)

# Function to calculate the average overall HR
def avgOverallHR():
    totalHR = 0
    for entry in data:  # Iterate through each dictionary in the data list
        totalHR += entry["RHR"]  # Sum up the "RHR" values
    avg = totalHR / len(data)  # Calculate the average
    print(f"Average HR: {avg}")

avgOverallHR()



def determine_cycle_phase(data, cycle_length=28):
    

    """
    Determine the menstrual cycle phase based on HRV and RHR trends.

    :param data: List of dictionaries with HRV, RHR, and calendarDate.
    :param cycle_length: Average cycle length in days (default 28).
    :return: List of dictionaries with phases assigned to each date.
    """
    phases = []  # Store results
    rolling_window = 3  # Rolling window for smoothing trends

    # Helper: Rolling average
    def rolling_avg(values, window_size):
        return sum(values[-window_size:]) / min(len(values), window_size)

    # Phases with approximate cycle day ranges
    phase_days = {
        "Menstrual": (1, 5),
        "Follicular": (6, cycle_length // 2),
        "Ovulatory": (cycle_length // 2 + 1, cycle_length // 2 + 3),
        "Luteal": (cycle_length // 2 + 4, cycle_length),
    }

    recent_hrv = []
    recent_rhr = []

    for i, entry in enumerate(data):
        # Track HRV and RHR
        recent_hrv.append(entry["HRV"])
        recent_rhr.append(entry["RHR"])

        # Rolling averages for trends
        avg_hrv = rolling_avg(recent_hrv, rolling_window)
        avg_rhr = rolling_avg(recent_rhr, rolling_window)

        # Calculate cycle day (assuming repeated cycle of cycle_length days)
        cycle_day = (i % cycle_length) + 1

        # Determine phase based on cycle day
        for phase, (start, end) in phase_days.items():
            if start <= cycle_day <= end:
                current_phase = phase
                break

        # Assign phase
        phases.append({
            "calendarDate": entry["calendarDate"],
            "HRV": entry["HRV"],
            "RHR": entry["RHR"],
            "cycleDay": cycle_day,
            "phase": current_phase,
        })

    return phases


# Run function
phases = determine_cycle_phase(data)

# Output results
for phase in phases:
    print(f"{phase['calendarDate']} - HRV: {phase['HRV']} | RHR: {phase['RHR']} | Phase: {phase['phase']} (Cycle Day: {phase['cycleDay']})")

