# for loop method, took 5.5  mins to run

import pandas as pd
import numpy as np

# Step 1: Read the .dat file and parse the contents
dat_file = r'C:\Users\Rajvi\Documents\WORK\GATech\Spring RA\codinh\20240506-Score_Matching\20240506-Score_Matching\condor\patientMatchingScores_AL.dat'

# dat_file1= r"C:\Users\Rajvi\Documents\WORK\GATech\Spring RA\codinh\patientMatchingScores_AL.dat"

with open(dat_file, 'r') as f:
    lines = f.readlines()
    
# print(lines)
    

# Parse the contents
state_key = int(lines[0].strip()[1])
depressed_indexes = list(map(int, lines[1].strip()[1:-1].split(',')))
depressed_scores = list(map(float, lines[2].strip()[1:-1].split(',')))
non_depressed_indexes = list(map(int, lines[3].strip()[1:-1].split(',')))
non_depressed_scores = list(map(float, lines[4].strip()[1:-1].split(',')))


print("formatting done")

# Convert parsed data into DataFrames
dataD = pd.DataFrame({'id': depressed_indexes, 'scoresD': depressed_scores})
dataN = pd.DataFrame({'id': non_depressed_indexes, 'scoresN': non_depressed_scores})

# Step 2: Convert scores to numpy arrays
scoresD = dataD['scoresD'].values
scoresN = dataN['scoresN'].values


print("variables ready now entering loop")
# Step 3: Initialize a list to store the matches
matches = []

# Step 4: Greedy matching
for i, scoreD in enumerate(scoresD):
    # Find the non-depressed score with the smallest absolute difference
    differences = np.abs(scoresN - scoreD)
    j = np.argmin(differences)
    matches.append((dataD['id'][i], scoreD, dataN['id'][j], scoresN[j], differences[j]))

    # Remove the matched non-depressed score to avoid duplicate matching
    scoresN = np.delete(scoresN, j)
    dataN = dataN.drop(dataN.index[j]).reset_index(drop=True)

# Step 5: Convert matches to DataFrame
matches_df = pd.DataFrame(matches, columns=['Depression ID', 'Depression Score', 'Non Depression ID', 'Non Depression Score', 'Abs. Score Difference'])

# Step 6: Save to CSV
state_dict = {1: 'AL', 5: 'AR', 6: 'CA', 12: 'FL', 13: 'GA', 22: 'LA', 28: 'MN', 29: 'MS', 38: 'NC', 37: 'NY', 45: 'PA', 48: 'SC', 50: 'TN', 51: 'TX'}
stateName = state_dict.get(state_key, "")

matchFile = f"matched_IDs_{stateName}.csv"
matches_df.to_csv(matchFile, index=False)

print("Matching completed and saved to:", matchFile)
print(matches_df)
