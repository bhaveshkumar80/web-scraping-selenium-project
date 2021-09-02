import pandas as pd
import json

with open('Kaufen_Anlageobjekte.json', 'r') as f:
    json_data = json.load(f)

df = pd.json_normalize(json_data)
df.to_csv('Kaufen_Anlageobjekte.csv', index=False)
