# E-Field-Vector-Plotter
## Isaac Wines

> A simple python logic tool that takes in bulk CSV files of different recorded voltage readings across a grid and outputs the E Field Vectors at each of those points, plotted with matplotlib.

## Setting up Environment

1) Clone repo and set working directory to said folder
2) If new setup:
    - Set up your virtual environment, in terminal --> "python -m venv .venv" *or if using python3* "python3 -m venv .venv"
3) If .venv is already made:
    - in terminal --> "source .venv/bin/activate"
4) Install dependancies, in terminal --> "pip install -r requirements.txt"

## Using the Script

> **Note:** This script assumes that each reading has a uniform distance between each point in the x and in the y direction. It also does not account for field in the z direction.

> **Note:** The script for testing purposes can also output the following `Ex_formula` or `Ey_formula` variables, these are CSV files that instead of numbers in each point, outputs what two numbers are being subtracted to get the value for that specific Ex or Ey component. 

1) Follow the comment in the code for the config setup, create a seperate folder for each different reading config, script will output everything pertaining to that specific config in its specific folder.
2) Set the `step_size` variable to the distance between readings (or points). Script math based in **mm**.
3) Set the `size` variable to the dimensions of the voltage reading CSV files. **Note:** This assumes all the reading CSV files are the same dimensions, if bulk calculating multiple different voltage reading CSV files, either set this value to the dimensions of the smallest CSV file or specify in the config each the dimensions of each different CSV file.
4) If specifying each dimension, uncomment **Line 167** through **Line 170**.
5) Run script, all plots and component CSV files will be saved to their respective folders.

## Proper Folder Setup 

> Before Running Script
```txt
E-Field-Vector-Plotter/
├── .venv/
├── config_example/
│   └── config_example.csv
├── requirements.txt
├── Efield_Plot.py
├── LICENSE
└── README.md
```

> After Running Script
```txt
E-Field-Vector-Plotter/
├── .venv/
├── config_example/
│   ├── config_example.csv
│   ├── config_example_Ex.csv
│   ├── config_example_Ey.csv
│   └── config_example_vector_plot.png
├── requirements.txt
├── Efield_Plot.py
├── LICENSE
└── README.md
```

## Concept

Imagine you have a grid where each value on said grid corresponds with a specific point on a table, with the top left box in the grid being the origin. Every box does not store positional data, but it does store the Electric Potential otherwise known as Voltage, at each point on this table. If you were to run a current through the table in different paths, then the Voltage at each point would change depending on the amount of current and the shape it takes through the table.
In a 2 Dimensional space, the flow of these electrons can create an electric field in the X and in the Y dimensions. Through taking in the Voltage through equidistant measurements on our table, we can determine what the vectors of our electric field is. 

The script takes in the Readings for point 0 then calculates the vector from point 0 to point 1, and so on until every point in the X and in the Y has been calculated to get the components of each E field vector at each point, and seperates them into two new relational grids. **This calculation will result in a 1 row loss and a 1 column loss** as it is doing vector calculations.
