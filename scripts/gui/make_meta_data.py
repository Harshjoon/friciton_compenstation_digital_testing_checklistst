

def make_meta_data(
        gui_object,
        default = False
):
    
    default_meta_data = {
        'actuator_serial_number'            : "No serial no found",
        'document_number'                   : "No document no found",
        'revision_number'                   : "No revision no found",
        'date'                              : "No date found",
        'assembler_name'                    : "No name found",
        'assembly_date'                     : "No date found",
        'assembler_signature'               : "No signature found",
        'tester_name'                       : "No name found",
        'testing_date'                      : "No date found",
        'tester_signature'                  : "No signature found",
        'approver_name'                     : "No name found",
        'approval_date'                     : "No date found",
        'approver_signature'                : "No signature found",
        'end_remarks'                       : "No remarks found",
        'ch_1'                              : u'\u2717',
        'ch_2'                              : u'\u2717',
        'ch_3'                              : u'\u2717',
        'ch_4'                              : u'\u2717',
        'ch_5'                              : u'\u2717',
        'ch_6'                              : u'\u2717',
        'ch_7'                              : u'\u2717',
        'ch_8'                              : u'\u2717',
        'yn_1'                              : "No data found",
        'yn_2'                              : "No data found",
        'remarks_1'                         : "",
        'remarks_2'                         : "",
        'remarks_3'                         : "",
        'remarks_4'                         : "",
        'remarks_5'                         : "",
        'remarks_6'                         : "",
        'inspector_name_1'                  : "",
        'inspector_name_2'                  : "",
    }

    meta_data = {}

    if default:
        meta_data = default_meta_data
    
    return meta_data