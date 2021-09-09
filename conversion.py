import pandas as pd
import json

def Data_cleaning(data):
    data = data.split('|')
    d1 = data[0].strip()
    if len(data) > 1:
        d2 = data[1].strip()
        data = '|'.join([d1, d2])
        return data
    else:
        return d1

def convert(file):
    with open(file, 'r', encoding='utf-8') as f:
        json_data = json.load(f, strict=False)
    df = pd.json_normalize(json_data)
    df['Scout id'] = df['Scout id'].apply(lambda x: Data_cleaning(x))
    csv_file = file.split('.')[0] + '.csv'
    df.to_csv(csv_file, index=False)

convert('temp_Kaufen_Haus.json')
