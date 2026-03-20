with open("combined.csv", "w") as out:
    first = True 

    for name in ["flankerdata/flankerdata1.csv", "flankerdata/flankerdata2.csv", "flankerdata/flankerdata3.csv", "flankerdata/flankerdata4.csv", "flankerdata/flankerdata5.csv", "flankerdata/flankerdata6.csv", "flankerdata/flankerdata7.csv", "flankerdata/flankerdata8.csv", "flankerdata/flankerdata9.csv", "flankerdata/flankerdata10.csv", "flankerdata/flankerdata11.csv", "flankerdata/flankerdata12.csv", "flankerdata/flankerdata13.csv", "flankerdata/flankerdata14.csv", "flankerdata/flankerdata15.csv", "flankerdata/flankerdata16.csv"]:
        with open(name) as file: 
            lines = file.readlines() #read all lines in file and store them in a list called lines 

            if first:   #first file only
                out.writelines(lines)   #write everything into this combinedcvsv file 
                first = False   #done with first 
            else: 
                out.writelines(lines[1:])   #write everything except first row for all other files 
