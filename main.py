import streamlit as st
import pandas as pd
import csv
import plotly.express as px

file_path = 'C:\\Users\\mhcwainwri\\Documents\\AppDev\\Python\\misc\\79_FAL.csv'

data_dict = []
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    data_as_string = "\n".join(",".join(row) for row in reader)
   

all_data = {}
for line in map(str.strip, data_as_string.splitlines()):
    if line == "":
        continue
    line = line.split(",")
    all_data.setdefault(len(line), []).append(line)

# for i in all_data:
#     st.write(i,len(all_data[i]))
    
    
key = []
rows = []
longlat = []
for i in all_data:
    length = len(all_data[i])
    
    for j in range(length):
        for x in all_data[i][j]:
            if len(x) == 5 or len(x) == 6:
                key.append(i)
                rows.append(j)
                longlat.append(x)


df_longlat = pd.DataFrame({'Key': key, 'Row': rows, 'LongLat': longlat})
df_longlat = df_longlat.groupby(['Key', 'Row'], as_index=False).agg({'LongLat': ' '.join})
df_longlat[['Latitude', 'Longitude']] = df_longlat['LongLat'].str.split(' ', expand=True)
df_longlat=df_longlat.drop('LongLat', axis=1)



df_longlat[['Lat Degrees', 'Lat Minutes', 'Lat Seconds']] = df_longlat['Latitude'].apply(
    lambda x: pd.Series([x[:2], x[2:4], x[4:]]))
df_longlat[['Lat Degrees', 'Lat Minutes', 'Lat Seconds']] = df_longlat[['Lat Degrees', 'Lat Minutes', 'Lat Seconds']].apply(pd.to_numeric)
df_longlat['LAT'] = df_longlat['Lat Degrees'] + df_longlat['Lat Minutes']/60.0 + df_longlat['Lat Seconds']/3600.0


df_longlat[['Long Degrees', 'Long Minutes', 'Long Seconds']] = df_longlat['Longitude'].apply(
    lambda x: pd.Series([x[:3], x[3:5], x[5:]]))
df_longlat[['Long Degrees', 'Long Minutes', 'Long Seconds']] = df_longlat[['Long Degrees', 'Long Minutes', 'Long Seconds']].apply(pd.to_numeric)
df_longlat['Longitude'] = df_longlat['Long Degrees'] + df_longlat['Long Minutes']/60.0 + df_longlat['Long Seconds']/3600.0
df_longlat['LON'] = df_longlat['Longitude']*-1


df_longlat=df_longlat.drop(['Latitude','Longitude', 'Lat Degrees', 'Lat Minutes', 'Lat Seconds', 'Long Degrees', 'Long Minutes', 'Long Seconds'], axis=1)
st.dataframe(df_longlat, use_container_width=True)
     
     
     
st.map(df_longlat, color='#529c98', )
