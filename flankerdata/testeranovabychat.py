#from chatgpt... more correct 
import pandas as pd
from statsmodels.stats.anova import AnovaRM

# Read in the CSV data
data = pd.read_csv("combined.csv")

# Filter out rows with missing rt values
data = data.dropna(subset=["rt"])

# Convert rt to numeric
data["rt"] = pd.to_numeric(data["rt"], errors="coerce")
data = data.dropna(subset=["rt"])

# Keep only correct trials if accuracy exists
if "accuracy" in data.columns:
    data = data[data["accuracy"] == 1]

# Keep only main trials if block exists
if "block" in data.columns:
    data = data[data["block"] == "main"]

# Repeated measures ANOVA
# For the standard flanker analysis, use 2 conditions:
# congruent vs incongruent
rm_anova = AnovaRM(
    data=data,
    depvar="rt",
    subject="participant",
    within=["type"],
    aggregate_func="mean"
)

results = rm_anova.fit()

# Print the ANOVA table
print(results)



#from aider... not so correct 
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

#coded with the help of aider 
# Read in the CSV data
data = pd.read_csv('csvforanova.csv')

# Filter out rows with missing rt values
data = data.dropna(subset=['rt'])

# Convert rt to numeric
data['rt'] = pd.to_numeric(data['rt'])

# Run the repeated measures ANOVA
model = ols('rt ~ C(stimulus)', data=data).fit()
anova_table = anova_lm(model)

# Print the ANOVA table
print(anova_table)
