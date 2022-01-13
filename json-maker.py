import csv
import json
 

with open("result.csv") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(rows)       
with open('vernoi.json','w') as f1:
    json.dump(rows,f1)