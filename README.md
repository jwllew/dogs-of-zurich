Dogs of Zürich
---
### Two web-based visualisations of publicly available data. I created this project in the completion of a Data Visualisation elective module, as part of my MSc in Computing.
---
I chose this dataset as I wanted to do something fun, and avoid data showing correlation or a change over time. 
It soon became apparent to me that maybe the physical details and name of every dog in Zurich (years 2015-2023) didn’t actually have very much to say in the way of a story. It was a challenge to try and make something interactive and engaging out of this dataset. 

  
Dataset is available at [Open Data Zurich](https://data.stadt-zuerich.ch/). 

[Names of dogs](https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002)

[Other data including breeds, colours, owner details](https://data.stadt-zuerich.ch/dataset/sid_stapo_hundebestand_od1001)

 
Inspiration taken from work by [Thomas Massie](https://public.tableau.com/app/profile/thomas.massie) as featured at [ODI](https://theodi.org/article/the-open-data-olympics-seven-weird-and-wonderful-open-datasets/).



### About the visualisations
---
The first visualisation is an interactive sunburst plot, created with Plotly and deployed within Dash. A user can adjust the range of displayed data and navigate through the hierarchy. Tooltips display further information.

![](https://github.com/jwllew/dogs-of-zurich/blob/main/vis1.gif)


The second visualisation is a d3 bubble plot displaying various categories of dog names and their frequencies.
It loads the d3 library from a script linked in the HTML head, and displays data from a JSON file contained within the /static directory. 

![](https://github.com/jwllew/dogs-of-zurich/blob/main/vis2.gif)


### Usage
---
The two visualisations are stored within separate folders.

#### Running vis 1
optionally run this in a virtual environment to sandbox the requirements
```
cd ./vis1
pip install -r requirements.txt
python -m vis1_dash
```

#### Running vis 2
```
cd ./vis2
python -m http.server
```
---
