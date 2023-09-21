import json


def save_json(
        meta_data = {}
):

    # description
    json_object     = json.dumps(meta_data, indent=4)
    out_path        = "../../report_data/json/{}".format(meta_data['actuator_serial_number'])

    with open( out_path, "w") as outfile:
        json.dump(json_object, outfile)
    
    return None



