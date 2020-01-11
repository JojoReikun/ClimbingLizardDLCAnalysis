"""
LizardDLCAnalysis Toolbox
© Jojo S.
Licensed under MIT License
"""
import pandas as pd

from lizardanalysis.utils.auxiliaryfunctions import UserFunc

# list of all calculations and their requirements of labels as implemented in the program
calculations = {'direction_of_climbing': ['nose'],
                'climbing_speed': ['nose'],
                'stride_and_stance_phases': ['fl', 'fr', 'hl', 'hr'],
                'stride_length': ['fl', 'fr', 'hl', 'hr'],
                'limb_kinematics': ['shoulder', 'hip', 'fr_knee', 'shoulder_fr', 'fl_knee', 'shoulder_fl', 'hr_knee',
                                    'shoulder_hr', 'hl_knee', 'shoulder_hl'],
                'wrist_angles': ['shoulder', 'hip', 'fr_knee', 'fr_ti', 'fr_to', 'fl_knee', 'fl_ti', 'fl_to',
                                 'shoulder_fl', 'hr_knee', 'hr_ti', 'hr_to', 'hl_knee', 'hl_ti', 'hl_to']
                }
# add ROM
calculations_str = [calculations.keys()]
results_file = pd.DataFrame(columns=calculations.keys())


def check_calculation_requirements(cfg):
    """
    this function checks if the required labels needed for the respective calculations
    are available in the list of available label extracted from the .csv file before.
    Depending on the result of the comparison, the calculation will be added to the calculations_checked list
    :param cfg: read in config file
    :return: list of available calculations
    """
    # If labels are named similarly but differ from default slightly, variations can be added to another variation list
    # and additionally checked with any() instead of all()

    calculations_checked = []
    for calculation in calculations.keys():
        calculation_ok = all(elem in cfg['labels'] for elem in calculations.values())
        # add available calculations to list
        if calculation_ok:
            func = UserFunc(calculation, calculation)   # module name calculation, function name calculation
            calculations_checked.append(func)
    if len(calculations_checked) == 0:
        print(
            'there is no calculation available for analysis due to insufficient or non-relevant labels in DLC result files.')
        return

    return calculations_checked


def process_file(data, likelihood, calculations_checked):
    """
    Goes through all available calculations which were determined on their labels and stored in calculations_checked.
    For all calculations in that list the parameter will be calculated.
    If calculations not in calculations_checked but in calculations, one or more of the required labels are missing/weren't found and parameter will be skipped.
    :param data: pd.dataframe DLC csv file
    :param likelihood: float value to change accuracy of results
    :param calculations_checked: list of available calculations (required labels exist)
    :return: #TODO
    """

    # TODO: allow filter for direction of climbing (e.g. only files with direction of climbing = UP will be processed)

    # TODO:filter data for values with likelihood >= e.g. 90%
    # data = data['likelihood'] >= likelihood
    # print("data with filtered likelihood: ", data.head())

    # TODO: simplify: list with possible calculations, loop through that. This definitely can be done nicer and easierer augmentable
    for calc in calculations:
        print("calc: ", calc)
        if calc in calculations.keys() and calc not in calculations_checked:
            print("Some label requirements are not fulfilles to calculate {} ".format(calc))
        elif calc in calculations_checked:
            calc.__getitem__([1])()

    # that's how it was beforehand:
    #     calc_direction_of_climbing(data)
    # else:
    #     print('At least one label required for the calculation of the direction of climbing is missing. Parameter skipped.')
    #
    # if climbing_speed:
    #
    #     calc_climbing_speed(data)
    # else:
    #     print('At least one label required for the calculation of the climbing speed is missing. Parameter skipped.')
    #
    # if stride_and_stance_phases:
    #
    #     calc_stride_and_stance_phases(data)
    # else:
    #     print('At least one label required for the calculation of stride and stance phases is missing. Parameter skipped.')
    #
    # if stride_length:
    #     from lizardanalysis.calculations import calc_stride_length
    #     calc_stride_length(data)
    # else:
    #     print('At least one label required for the calculation of stride lengths is missing. Parameter skipped.')


def read_csv_files(config, separate_gravity_file=False, likelihood=0.90):
    """
    Reads the DLC result csv files which are listed in the config file and checks which labels are available for calculation.
    config : string
        Contains the full path to the config file of the project.
        Tipp: Store path as a variable >>config<<
    seperate_gravity_file : bool, optional
        If this is set to True, user can choose a gravity csv file to use the gravity axis as reference axis for analysis.
        If this is set to False, x-axis of video will be used as reference axis for analysis.
        Default: False
    likelihood: float [0.0-1.0]
        defines the level of accuracy used for including label results in the analysis.
        Default: 0.90
    """
    import os
    import sys
    import numpy as np
    from pathlib import Path
    from tkinter import Tk, filedialog
    from lizardanalysis.utils import auxiliaryfunctions

    config_file = Path(config).resolve()
    cfg = auxiliaryfunctions.read_config(config_file)
    print("Config file read successfully.")

    # get the file paths from the config file
    project_path = cfg['project_path']

    files = cfg['file_sets'].keys()  # object type ('CommentedMapKeysView' object), does not support indexing
    filelist = []  # store filepaths as list
    for file in files:
        filelist.append(file)
    # print("files (keys): ,", filelist)  # TEST

    # check if user entered camera specs in config file
    if cfg['framerate'] is None and cfg['shutter'] is None:
        print('Please add camera settings in the config file before you continue.')
        return
    else:
        print('Camera settings entered: \n',
              'framerate: ', cfg['framerate'], '\n',
              'shutter: ', cfg['shutter'], '\n',
              'Available labels will be checked and written to config file...')

    # check if user set separate gravity file to True
    if separate_gravity_file:
        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        gravity_filepath = filedialog.askopenfilename(
            filetype=[('csv files', '*.csv')])  # show an "Open" dialog box and return the path to the selected file
        df_gravity = pd.read_csv(gravity_filepath)  # read in gravity file

    # check available labels in .csv files and write them to config file. Uses the first .csv file in the directory.
    # TODO: Check if working directory differs from default and set path respectively
    # if working_directory = DEFAULT:
    # use Path lib
    current_path = Path(os.getcwd())
    project_dir = '{pn}-{exp}-{spec}-{date}'.format(pn=cfg['task'], exp=cfg['scorer'], spec=cfg['species'],
                                                    date=cfg['date'])
    label_file_path_2 = os.path.join(project_dir, "files", os.path.basename(filelist[0]))
    label_file_path = os.path.join(current_path, label_file_path_2)
    # print('label_file_path: ', label_file_path)
    # else:
    # TODO: look for working directory
    data_labels = pd.read_csv(label_file_path, delimiter=",",
                              header=[0, 1, 2])  # reads in first csv file in filelist to extract all available labels
    data_labels.rename(columns=lambda x: x.strip(), inplace=True)  # remove whitespaces from column names
    # print(data.head())

    data_labels_columns = list(data_labels.columns)
    # scorer = data_columns[1][0]     atm not needed
    label_names = []
    for i in range(1, len(data_labels_columns)):
        label_names.append(str(data_labels_columns[i][1]).lower())  # append all label names and convert to lowercase
    label_names_no_doubles = []
    [label_names_no_doubles.append(label) for label in label_names if
     label not in label_names_no_doubles]  # makes sure labels only appear once

    if len(label_names_no_doubles) == 0:
        print(
            'no labels could be found. Maybe check that there are .csv files available in the files folder with the DLC result format.')
        return
    else:
        print("available are the following ", len(label_names_no_doubles), " labels in csv files: ",
              label_names_no_doubles)

    # write labels to config file:
    if cfg['labels'] is None:
        cfg['labels'] = label_names_no_doubles
        auxiliaryfunctions.write_config(config, cfg)
        print('\n labels written to config file.')
    else:
        print('labels already exist in config file.')

    # check label requirements for calculations:
    calculations_checked = check_calculation_requirements(cfg)

    ### ToDo: erst hier solltest du das results dataframe anlegen, wenn du weißt, welche Rechnungen funktionieren und welche columns du bekommen wirst!
    # results_file = pd.DataFrame(columns=calculations.keys())

    # TODO: run calculations loop for every file
    for i in range(len(filelist)):
        file_path_2 = os.path.join(project_dir, "files", os.path.basename(filelist[i]))
        file_path = os.path.join(current_path, file_path_2)
        data = pd.read_csv(file_path, delimiter=",",
                           header=[0, 1, 2])  # reads in first csv file in filelist to extract all available labels
        data_labels.rename(columns=lambda x: x.strip(), inplace=True)  # remove whitespaces from column names
        # perform calculations for the current file
        process_file(data, likelihood, calculations_checked)
        i += 1
