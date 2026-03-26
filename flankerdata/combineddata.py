import pandas as pd

dfs = []

files = [
    "flankerdata1.csv",
    "flankerdata2.csv",
    "flankerdata3.csv",
    "flankerdata4.csv",
    "flankerdata5.csv",
    "flankerdata6.csv",
    "flankerdata7.csv",
    "flankerdata8.csv",
    "flankerdata9.csv",
    "flankerdata10.csv",
    "flankerdata11.csv",
    "flankerdata12.csv",
    "flankerdata13.csv",
    "flankerdata14.csv",
    "flankerdata15.csv",
    "flankerdata16.csv"
]

for i, file in enumerate(files):
    temp = pd.read_csv(file)
    temp["participant"] = i + 1   # ✅ THIS is the key line
    dfs.append(temp)

df = pd.concat(dfs, ignore_index=True)

df.to_csv("combined.csv", index=False)