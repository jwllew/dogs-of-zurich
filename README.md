Dogs of Zürich
---
### Two web-based visualisations of publicly available data. I created this project in the completion of a Data Visualisation elective module, as part of my MSc in Computing.
---
I chose this dataset as I wanted to do something different, and avoid data showing correlation or a change over time. 
It soon became apparent to me that maybe the physical details and name of every dog in Zurich (years 2015-2023) didn’t actually have very much to say in the way of a story. It was a challenge to try and make something interactive and fun out of this dataset. 

  
Dataset is available at [Open Data Zurich](https://data.stadt-zuerich.ch/). 

[Names of dogs](https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002)

[Other data including breeds, colours, owner details](https://data.stadt-zuerich.ch/dataset/sid_stapo_hundebestand_od1001)

 
Inspiration taken from work by <a href="https://public.tableau.com/app/profile/thomas.massie">Thomas Massie </a> as featured at <a href="https://theodi.org/article/the-open-data-olympics-seven-weird-and-wonderful-open-datasets/">ODI</a>.

### Running the visualisations
The first visualisation is a Plotly chart deployed within Dash.
Usage
---
cd ./vis1 
pip install -r requirements.txt
python -m vis1_dash
---
The second visualisation is a d3 plot.
It loads the d3 library from a script linked in the HTML head, and displays data from a JSON file contained within the /static directory. 

Usage
---
cd ./vis2
python -m http.server
---
