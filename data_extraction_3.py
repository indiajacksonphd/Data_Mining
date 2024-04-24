import pandas as pd
import itertools
from itertools import combinations
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import csv



# Read the CSV file
extracted_df = pd.read_csv('GSEP_Data_Mining.csv')
df = extracted_df.copy()
# Extract the desired columns
desired_columns = ['cme_1st_app_time', 'fl_goes_class', 'ppf_gt10MeV', 'ppf_gt30MeV', 'ppf_gt60MeV', 'ppf_gt100MeV']
df = df[desired_columns]


# Mapping of fl_goes_class to SF_C, SF_M, SF_X
def map_fl_goes_class(fl_goes_class):
    if pd.isna(fl_goes_class):  # Check for missing values
        return None
    elif fl_goes_class.startswith('X'):
        return 'X'
    elif fl_goes_class.startswith('M'):
        return 'M'
    elif fl_goes_class.startswith('C'):
        return 'C'
    else:
        return None


# Map fl_goes_class
df['fl_goes_class'] = df['fl_goes_class'].apply(map_fl_goes_class)
# Set display options to show all rows and columns

# Replace empty cells with 0 and non-empty cells with 1 for specified columns
cols_to_replace = ['cme_1st_app_time', 'ppf_gt10MeV', 'ppf_gt30MeV', 'ppf_gt60MeV', 'ppf_gt100MeV']
df[cols_to_replace] = df[cols_to_replace].fillna(0).applymap(lambda x: 0 if x == 0 else 1)


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Create new columns for SF_C, SF_M, SF_X
df['SF_C'] = 0
df['SF_M'] = 0
df['SF_X'] = 0

# Update values based on fl_goes_class
df.loc[df['fl_goes_class'] == 'C', 'SF_C'] = 1
df.loc[df['fl_goes_class'] == 'M', 'SF_M'] = 1
df.loc[df['fl_goes_class'] == 'X', 'SF_X'] = 1

# print(df)

# Rename columns
df.rename(columns={'cme_1st_app_time': 'CME', 'ppf_gt10MeV': 'SEP_10', 'ppf_gt30MeV': 'SEP_30', 'ppf_gt60MeV': 'SEP_60', 'ppf_gt100MeV': 'SEP_100'}, inplace=True)

# Create a new DataFrame with desired column names
new_df = df[['SF_C', 'SF_M', 'SF_X', 'CME', 'SEP_10', 'SEP_30', 'SEP_60', 'SEP_100']]
# Assuming your DataFrame is named df
new_df = new_df.astype(bool)
#print(new_df)

# Count of True values in the 'SF_C' column
sf_c_count = new_df['SF_C'].sum()
print(sf_c_count)

sf_m_count = new_df['SF_M'].sum()
print(sf_m_count)

sf_x_count = new_df['SF_X'].sum()
print(sf_x_count)

# Count of True values for transaction 0
transaction_0_count = new_df.iloc[0].sum()
print(transaction_0_count)


# Function to create the itemset
def create_itemset(row):
    itemset = []
    for column, value in row.items():
        if value == 1:
            itemset.append(column)
    return set(itemset)


# Define the columns
columns = ['SF_C', 'SF_M', 'SF_X', 'CME', 'SEP_10', 'SEP_30', 'SEP_60', 'SEP_100']


########################## ALL COMBINATIONS ######################################
# List of column names
columns_C = ['SF_C', 'CME', 'SEP_10', 'SEP_30', 'SEP_60', 'SEP_100']

# Generate combinations of different lengths
combinations_C = []
for r in range(1, len(columns_C)+1):
    combinations_C.extend(itertools.combinations(columns_C, r))

print("Class C")
# Print the combinations
for combo in combinations_C:
    print(combo)

# List of column names
columns_M = ['SF_M', 'CME', 'SEP_10', 'SEP_30', 'SEP_60', 'SEP_100']

# Generate combinations of different lengths
combinations_M = []
for r in range(1, len(columns_M)+1):
    combinations_M.extend(itertools.combinations(columns_M, r))

print("Class M")
# Print the combinations
for combo in combinations_M:
    print(combo)

# List of column names
columns_X = ['SF_X', 'CME', 'SEP_10', 'SEP_30', 'SEP_60', 'SEP_100']

# Generate combinations of different lengths
combinations_X = []
for r in range(1, len(columns_X)+1):
    combinations_X.extend(itertools.combinations(columns_X, r))

print("Class X")
# Print the combinations
for combo in combinations_X:
    print(combo)

print("Length of C: ", len(combinations_C))
print("Length of M: ", len(combinations_M))
print("Length of X: ", len(combinations_X))

# List of column names and combinations
column_combinations = [
    ('Class C', combinations_C),
    ('Class M', combinations_M),
    ('Class X', combinations_X)
]

# Define the file path
file_path = 'combinations.csv'

# Write the combinations to the CSV file
with open(file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for class_name, combinations in column_combinations:
        writer.writerow([class_name])
        for combo in combinations:
            writer.writerow(combo)
        writer.writerow([])  # Add an empty row between classes
#############################################################################

################################ ITEM COUNTS #####################################################
counts_C = {}

# Iterate over each combination
for combo in combinations_C:
    # Create a key for the combination
    combo_key = ','.join(combo)

    # Filter the DataFrame based on the combination and count the occurrences
    count = new_df[list(combo)].all(axis=1).sum()

    # Store the count in the dictionary
    counts_C[combo_key] = count

# Print the counts
for combo_key, count in counts_C.items():
    print(f"Count of {combo_key}: {count}")


counts_M = {}

# Iterate over each combination
for combo in combinations_M:
    # Create a key for the combination
    combo_key = ','.join(combo)

    # Filter the DataFrame based on the combination and count the occurrences
    count = new_df[list(combo)].all(axis=1).sum()

    # Store the count in the dictionary
    counts_M[combo_key] = count

# Print the counts
for combo_key, count in counts_M.items():
    print(f"Count of {combo_key}: {count}")

counts_X = {}

# Iterate over each combination
for combo in combinations_X:
    # Create a key for the combination
    combo_key = ','.join(combo)

    # Filter the DataFrame based on the combination and count the occurrences
    count = new_df[list(combo)].all(axis=1).sum()

    # Store the count in the dictionary
    counts_X[combo_key] = count

# Print the counts
for combo_key, count in counts_X.items():
    print(f"Count of {combo_key}: {count}")


# Define the file path
file_path = 'combination_counts.csv'


# Define a function to save counts to a CSV file
def save_counts_to_csv(file_path, all_counts):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Combination', 'Count'])
        for combo_key, count in all_counts.items():
            writer.writerow([combo_key, count])


# Combine counts for all classes into a single dictionary
all_counts = {**counts_C, **counts_M, **counts_X}

# Save counts for all combinations to a single CSV file
save_counts_to_csv(file_path, all_counts)

#####################################################################################

# Run the Apriori algorithm to find frequent itemsets
frequent_itemsets = apriori(new_df, min_support=0.01, use_colnames=True)
print(frequent_itemsets)
# Generate association rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# Print the association rules
print(rules)
# Save the filtered rules to a CSV file
rules.to_csv('first_set_of_rules.csv', index=False)

# Iterate over the rows of the DataFrame
rows_to_drop = []
for index, row in rules.iterrows():
    antecedent = row['antecedents']
    consequent = row['consequents']

    # Check if any SEPs are in the antecedent and any of SF_C, SF_M, SF_X, or CME are in the consequent
    if any(item.startswith('SEP') for item in antecedent) and any(item in consequent for item in ['SF_C', 'SF_M', 'SF_X', 'CME']):
        rows_to_drop.append(index)

# Drop the rows that meet the specified criteria
rules.drop(rows_to_drop, inplace=True)

# Reset the index after dropping rows
rules.reset_index(drop=True, inplace=True)
rules.to_csv('pruned_rules.csv', index=False)

