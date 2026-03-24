import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

# Read in the CSV data
data = pd.read_csv('csvcopy.csv')

# Filter out rows with missing rt values
data = data.dropna(subset=['rt'])

# Convert rt to numeric
data['rt'] = pd.to_numeric(data['rt'])

# Run the repeated measures ANOVA
model = ols('rt ~ C(stimulus)', data=data).fit()
anova_table = anova_lm(model)

# Print the ANOVA table
print(anova_table)
