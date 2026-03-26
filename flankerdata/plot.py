import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("combined.csv")
print(df.columns)

#must compute participant means 
means = df.groupby(['participant', 'type'])['rt'].mean().reset_index() #computes one mean for each condition (congruent vs incongruent)

#must compute group means 
group_means = means.groupby('type')['rt'].mean()

#we need the standard error of the mean (SEM)
group_sem = means.groupby('type')['rt'].sem()

#values and plotting
conditions = group_means.index
values = group_means.values
errors = group_sem.values
plt.bar(conditions, values, yerr=errors, capsize=5)
plt.ylabel("Reaction Time (ms)")
plt.title("Effect of Congruency on Reaction Time")
plt.show()
