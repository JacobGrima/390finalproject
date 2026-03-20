import pandas as pd 

df = pd.read_csv("flankerdata/combined.csv")

#add partcipant id 
n_participants = 16
trials_per_participant = len(df) // n_participants 
df["participant_id"] = df.index // trials_per_participant + 1 

#analysis
print ("Mean RT:")
print(df.groupby("type")["rt"].mean())

print("\nAccuracy:")
print(df.groupby("type")["accuracy"].mean())

