"""
Calculate field values from electric potential, and plots the E_f vectors.
Can handle multple csvs.

Inputs:
    Voltage Readings <- .CSV

Outputs:
    Electric Field X Component at Each Point -> .CSV file
    Electric Field Y Component at Each Point -> .CSV file
    Plot of Electric Field Vectors at each point -> .PNG Image File
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def csv_import(path: str, size: tuple) -> pd.DataFrame:
    # Convert csv into dataframe
    df = pd.read_csv(path, header=None, index_col=False)

    # Normalize CSV Shape in return
    return df.iloc[: size[0], : size[1]]


def Ex_Calc(current_config: pd.DataFrame, size: tuple, step_size: float) -> tuple:
    """
    Function to return the calculated Ex Field from a config's csv file.

    Inputs:
        current_config <-- pandas DataFrame type of the config csv
        size <-- tuple (number of rows , number of columns)
        step_size <-- float distance between readings
    Outputs:
        Ex --> pandas DataFrame type of the Ex Field at each point from the config csv
    """

    Ex = {}
    Ex_Formula = {}

    for row in current_config.itertuples():
        # Initialize list for each row
        Ex[row[0]] = []
        Ex_Formula[row[0]] = []

        for v_reading in range(1, len(row[1:])):
            Ex_point = -1 * ((row[v_reading + 1] - row[v_reading]) / step_size)
            Ex[row[0]].append(Ex_point)
            Ex_Formula[row[0]].append(f"{row[v_reading + 1]} - {row[v_reading]}")

    return pd.DataFrame.from_dict(Ex).T.iloc[
        : size[0], : size[1]
    ], pd.DataFrame.from_dict(Ex_Formula).T.iloc[: size[0], : size[1]]


def Ey_Calc(current_config: pd.DataFrame, size: tuple, step_size: float) -> tuple:
    """
    Function to return the calculated Ey Field from a config's csv file.

    Inputs:
        current_config <-- pandas DataFrame type of the config csv
        size <-- tuple (number of rows , number of columns)
        step_size <-- float distance between readings
    Outputs:
        Ey --> pandas DataFrame type of the Ey Field at each point from the config csv
    """

    Ey = {}
    Ey_Formula = {}

    for col in current_config.items():
        # Initialize list for each row
        Ey[col[0]] = []
        Ey_Formula[col[0]] = []

        for v_reading in range(len(col[1])):
            try:
                Ey_point = -1 * (
                    (col[1][v_reading + 1] - col[1][v_reading]) / step_size
                )

                Ey[col[0]].append(Ey_point)
                Ey_Formula[col[0]].append(
                    f"{col[1][v_reading + 1]} - {col[1][v_reading]}"
                )
            except:
                pass

    return pd.DataFrame.from_dict(Ey).iloc[
        : size[0], : size[1]
    ], pd.DataFrame.from_dict(Ey_Formula).iloc[: size[0], : size[1]]


def plot_data(x_data, y_data, magnitudes, filename):
    """
    Generates a quiver plot of the supplied data.
    No return.
    """

    # Plot setup
    plt.ion()
    fig, ax = plt.subplots()

    # Generate vector plot
    pivot = "mid"
    title = f"E Field Vector Plot of {filename[1]}"

    q = ax.quiver(x_data, y_data, magnitudes, pivot=pivot)

    ax.set_title(title)

    # Add colorbar
    cbar = plt.colorbar(q)
    cbar.set_label("Vector magnitude", rotation=90)

    # Display plot
    plt.pause(0.1)
    plt.draw()

    # Save image
    print("Saving plot to {}".format(filename[0]))
    fig.savefig(filename[0] + "_vector_plot.png", dpi=300)

    # Cleanup
    plt.clf()
    plt.close()


def main():
    # Configs is a list of the information where the different readings are stored and how they should be outputted. Create a new config entry and folders for each different reading configurations.
    """
    Example Config Entry =
    {
        "path": "path/to/csv",                         <-- the path to the csv file of voltage readings
        "name": "name_of_reading",                     <-- name of the csv file without the '.csv'
        "Ex_Field": "path/to/E_field_x_component.csv", <-- this is a path for the script to output
        "Ey_Field": "path/to/E_field_y_component.csv", <-- this is a path for the script to output
        "folder": "config_a/",                         <-- folder where everything for specific configuration is stored
        "nicename": "Config A - Sharp",                <-- name for the plot title, can be whatever you want
        "dims": (int rows , int columns)               <-- size of the CSV file for this specific config
    }
    """
    configs = [
        {
            "path": "path/to/csv",
            "name": "name_of_reading",
            "Ex_Field": "path/to/E_field_x_component.csv",
            "Ey_Field": "path/to/E_field_y_component.csv",
            "folder": "config_a/",
            "nicename": "Config Example",
            "dims": (0, 0),
        }
    ]

    # Adjust to the dimensions of the voltage readings CSV: (rows,columns)
    size = (20, 28)

    # adjust to the distance between readings, assume uniform distance in x and y direction.
    step_size = 0.001

    for current_config in configs:
        print(current_config["name"])

        ###----------Uncomment line below if each different config CSV has different dimensions----------###
        # try:
        #     size = current_config["dims"]
        # except:
        #     print("Invalid or Nonexistant dimensions from config\Attempting to Default to global size...")
        ###----------------------------------------------------------------------------------------------###

        # Convert current config into pd dataframe]
        current_csv = csv_import(current_config["path"], size)

        Ecalc_size = (size[0] - 1, size[1] - 1)
        Ex, Ex_Formula = Ex_Calc(current_csv, Ecalc_size, step_size)
        # print("Ex\n", Ex)
        # print("Ex_Formula\n", Ex_Formula)

        Ey, Ey_Formula = Ey_Calc(current_csv, Ecalc_size, step_size)
        # print("Ey\n", Ey)
        # print("Ey_Formula\n", Ey_Formula)

        try:
            Ex.to_csv(current_config["Ex_Field"], index=False, encoding="utf-8")
            Ey.to_csv(current_config["Ey_Field"], index=False, encoding="utf-8")
            print(
                f"Successfully saved {current_config['name']} at {current_config['Ex_Field']} and {current_config['Ey_Field']}"
            )
        except Exception as e:
            print("Unable to create component csv\nCaught error: ", e)

        try:
            x_data, y_data = Ex.to_numpy(), Ey.to_numpy()
            magnitudes = np.sqrt(x_data**2 + y_data**2)
            plot_data(
                x_data,
                y_data,
                magnitudes,
                (
                    current_config["folder"] + current_config["name"],
                    current_config["nicename"],
                ),
            )
        except Exception as e:
            print("Unable to plot: ", e)


if __name__ == "__main__":
    main()
