import json

def read_json(file_path):
    with open(file_path, 'r') as fp:
        return json.load(fp)

# returns the filename of the csv for each stage, based in the original csv 
# filename and the stage number. Adds a suffix in the case it is provided 
# (useful in stage 6)
def get_filename_stage(stage:int, csv_filename:str, network:str=''):
    dtype_dict_stages = read_json('config_dictionaries/dictionary_stages_list.json')
    # [:-4] to strip the .csv extension
    file_name = f"{csv_filename[:-4]}_{dtype_dict_stages['Stage'+str(stage)]}.csv"
    if network != '':
        network = network.replace("^","up").replace("*","ALL")
        file_name = f"{csv_filename[:-4]}_{dtype_dict_stages['Stage'+str(stage)]}_{network}.csv"
    # file names should not contain spaces, ideally
    file_name = file_name.replace(" ","-")
    return file_name

# returns the filename for the plot that is generated in the final stage (6)
# it works for both global and per unit plots
def get_plot_filename(unit:str, measured_value:str, csv_filename:str, sufix:str=''):
    # for cases where the unit comes with "^" or "*" symbols
    unit = unit.replace("^","up").replace("*","ALL")
    # [:-4] to strip the .csv extension
    file_name = f'{csv_filename[:-4]}_plot_{unit}_{measured_value}.png'
    if sufix != '':
        file_name = f'{csv_filename[:-4]}_plot_{unit}_{measured_value}_{sufix}.png'
    # file names should not contain spaces, ideally
    file_name = file_name.replace(" ","-")
    return file_name
