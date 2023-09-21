from docx           import Document
from docx.oxml      import OxmlElement
from docx.oxml.ns   import qn
from docx2pdf       import convert


def make_document(
        meta_data       = {},
        template_path   = "../../documents/template.docx",
        output_path     = "../../documents/checklist_report.docx",
        save_pdf        = True
):
    
    document = Document(template_path)

    # set header information
    header          = document.sections[0].header

    header_data     = {
        "{{actuator_serial_no}}" : meta_data['actuator_serial_number'] + "           ",
        "{{doc_no}}"             : meta_data['document_number'],
        "{{rev no}}"             : "                   " + meta_data['revision_number']
    }

    for paragraph in header.paragraphs:
        for key,value in header_data.items():
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key,value)

    # set paragraph information
    main_paragraph_data     = {
        "{{date}}"                  : meta_data['date'],
        "{{assembled_by}}"          : meta_data['assembler_name'] + "\t",
        "{{assembled_date}}"        : meta_data['assembly_date'] + "\t" + "\t",
        "{{assembler_signature}}"   : meta_data['assembler_signature'],
        "{{tested_by}}"             : meta_data['tester_name'],
        "{{tested_date}}"           : meta_data['testing_date'] + "               ",
        "{{tester_signature}}"      : meta_data['tester_signature'],
        "{{approved_by}}"           : meta_data['approver_name'] + "\t", 
        "{{approved_date}}"         : meta_data['approval_date'] + "\t" + "\t",
        "{{approver_signature}}"    : meta_data['approver_signature'],
        "{{end_remarks}}"           : meta_data['end_remarks']
    }

    main_paragraph_data = fix_spaces(main_paragraph_data)

    for i,paragraph in enumerate(document.paragraphs):
        for key,value in main_paragraph_data.items():
            if key in paragraph.text:
                paragraph.text      = paragraph.text.replace(key,value)

    # set table information
    check_box_status = {
            "{{ch_1}}" : meta_data['ch_1'],
            "{{ch_2}}" : meta_data['ch_2'],
            "{{ch_3}}" : meta_data['ch_3'],
            "{{ch_4}}" : meta_data['ch_4'],
            "{{ch_5}}" : meta_data['ch_5'],
            "{{ch_6}}" : meta_data['ch_6'],
            "{{ch_7}}" : meta_data['ch_7'],
            "{{ch_8}}" : meta_data['ch_8'],
        }

    yes_no_status   = {
        "{{yn_1}}" : meta_data['yn_1'],
        "{{yn_2}}" : meta_data['yn_2'],
    }

    table_remarks_status = {
        "{{remarks_1}}" : meta_data['remarks_1'],
        "{{remarks_2}}" : meta_data['remarks_2'],
        "{{remarks_3}}" : meta_data['remarks_3'],
        "{{remarks_4}}" : meta_data['remarks_4'],
        "{{remarks_5}}" : meta_data['remarks_5'],
        "{{remarks_6}}" : meta_data['remarks_6'],
    }

    inspected_by_status = {
        "{{inspected_by_1}}" : meta_data['inspector_name_1'],
        "{{inspected_by_2}}" : meta_data['inspector_name_2'],
    }

    main_table          = document.tables[0]

    for i in range(len(main_table.columns)):
        for cell in main_table.column_cells(i):
            for key,value in check_box_status.items():
                if key in cell.text:
                    cell.text = cell.text.replace(key,value)
            
    for i in range(len(main_table.columns)):
        for cell in main_table.column_cells(i):
            for key,value in yes_no_status.items():
                if key in cell.text:
                    cell.text = cell.text.replace(key,value)
            
    for i in range(len(main_table.columns)):
        for cell in main_table.column_cells(i):
            for key,value in table_remarks_status.items():
                if key in cell.text:
                    cell.text = cell.text.replace(key,value)
            
    for i in range(len(main_table.columns)):
        for cell in main_table.column_cells(i):
            for key,value in inspected_by_status.items():
                if key in cell.text:
                    cell.text = cell.text.replace(key,value)

    # save document
    document.save(output_path)

    # save pdf
    convert(output_path, output_path[:-5] + ".pdf")


    return None


def fix_spaces(meta_data):

    if "{{assembled_by}}" in meta_data.keys():
        x = 30
        l = len(meta_data["{{assembled_by}}"]) 
        if l < x:
            meta_data["{{assembled_by}}"] = meta_data["{{assembled_by}}"] +  (x - l)*" "

    if "{{tested_by}}" in meta_data.keys():
        x = 30
        l = len(meta_data["{{tested_by}}"]) 
        if l < x:
            meta_data["{{tested_by}}"] = meta_data["{{tested_by}}"] +  (x - l)*" "

    if "{{approved_by}}" in meta_data.keys():
        x = 30
        l = len(meta_data["{{approved_by}}"]) 
        if l < x:
            meta_data["{{approved_by}}"] = meta_data["{{approved_by}}"] +  (x - l)*" "

    return meta_data