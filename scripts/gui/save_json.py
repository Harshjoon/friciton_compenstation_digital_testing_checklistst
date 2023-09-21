import json
import os

def save_json(
        meta_data = {}
):

    json_object     = json.dumps(meta_data, indent=4)
    out_path        = "../../report_data/json/{}".format(meta_data['actuator_serial_number'])

    with open( out_path, "w") as outfile:
        json.dump(json_object, outfile)
    
    return None


def file_exists(
        actuator_number = "",
) -> bool:
    
    json_files_dir  = "../../report_data/"
    
    files_list      = os.listdir(json_files_dir)

    if actuator_number in files_list:
        return True
    else:
        return False