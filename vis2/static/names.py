import pandas as pd
import numpy as np
from unidecode import unidecode
import json


# OPEN CSV

basecsv = "static/Hundenamen.csv"
dogs=pd.read_csv(basecsv)




# SCRUB CSV

# remove unnecessary columns
dogs = dogs.iloc[:, [0, 1, 2, 4]]

# rename German columns to English
dogs = dogs.rename(columns={'StichtagDatJahr' : 'Year of Registration', 'HundenameText' : 'Name', 'GebDatHundJahr' : 'Year of Birth', 'SexHundLang' : 'Sex'})

# map to change German data values to English
DeEnMapping = {
    'weiblich': 'female',
    'männlich': 'male'
}
dogs.replace(DeEnMapping, inplace=True)

# remove broken values from name data
dogs = dogs.loc[~dogs['Name'].str.contains(r'^\d+$|\?+')].reset_index(drop=True)
dogs = dogs.loc[~dogs['Name'].str.contains('unbekannt')].reset_index(drop=True)

# reformat names
dogs['Name'] = dogs['Name'].astype(str).apply(lambda x: unidecode(x))

# create columns with name lengths, dog ages for ease
dogs['Name Length'] = dogs['Name'].str.len()
dogs['Age'] = dogs['Year of Registration'] - dogs['Year of Birth']
dogs = dogs.iloc[:, [1, 4, 2, 0, 5, 3]]








# FUNCTIONS TO SEPARATE DOGS BY DIFFERENT CRITERIA


# find dogs ridiculously named after fashion houses/designers/luxury brands (why notm, it's Zurich)
# args taken - dataframe
def designerNames(d):
    with open("static/designers.txt", "r") as file:
        lines = file.readlines()
        lines = lines[0].split()
    df = d[d['Name'].str.contains('|'.join(lines))]
    d.iloc[:,[0,1,2]]
    return df

# find the longest names (30 character limit in Zurich)
# args taken - dataframe, name length 
def longNames(d, x):
    df = d[d['Name Length'] > x]
    df.iloc[:,[0,1,2]]
    return df

# find short names that only appear once in the dataset
# args taken - dataframe, name length 
def uniqueShortNames(d,x):
    df = d[d['Name Length'] <= x]
    nameNums = df['Name'].value_counts()
    unique_names = nameNums[nameNums == 1].index
    new_df = df[df['Name'].isin(unique_names)].copy()
    new_df['Name'] = new_df['Name'].str.title()
    df.iloc[:,[0,1,2]]
    return new_df





# JSON OUTPUT FUNCTIONS

# create JSON for names registered in a given year, sorted by frequency
# args - dataframe, year
def NamesByYear(d, year, mode):
    d = d[d['Year of Registration'] == year]
    counts = d['Name'].value_counts()
    # if all names, just output the top 100 names per year
    if mode == 'top':
        counts = (counts.head(100))
    counts.to_json('json/%s/nameCount_%s.json'%(mode,year),orient='index')


 
# call nameJSON function for each year
# generates separate year JSON for use in d3
# accepts a dataframe as input
def yearJSON(d, mode):
    yearsArr = d['Year of Registration'].unique()
    print('outputting %s jsons by year:'%(mode))
    for y in yearsArr:
        NamesByYear(d, y, mode)

        
        
# make JSON from lists
def listToJSON(l, mode):
    with open('json/%s/list.json'%mode, 'w') as f:
        json.dump(l, f)




# CALLING FUNCTIONS - MAKING JSONS

# make sub-dataframes for each criteria
des = designerNames(dogs)
lon = longNames(dogs, 29)
uniq = uniqueShortNames(dogs,10)


# generate JSONS for each sub-dataframe
yearJSON(dogs,'top')
yearJSON(des, 'designer')
yearJSON(lon,'long')
yearJSON(uniq,'unique')


# make lists of unique names for each sub-dataframe
designerList = sorted(des['Name'].unique())
longList = sorted(lon['Name'].unique())
uniqueList = sorted(uniq['Name'].unique())


# output these to JSON
listToJSON(designerList, 'designer')
listToJSON(longList, 'long')
listToJSON(uniqueList, 'unique')



# unused functions

# def sortByNameLength():
#     dogs.sort_values('name length', ascending=False, inplace=True)


# def findLongestName(d):
#     longestname = max(d['Name'], key=len)
#     print(longestname)

