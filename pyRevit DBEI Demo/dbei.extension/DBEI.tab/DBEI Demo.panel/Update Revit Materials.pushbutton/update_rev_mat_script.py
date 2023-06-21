__author__ = "Jared Friedman"
__title__ = "Update Revit\n Materials"
__doc__ = """

Updates Revit Materials from Airtable

This tool will update properties of Revit materials based on Airtable records.
"""

import sys

from rpw import db, UI
from rpw.ui.forms import Console

from pyrevit import forms


from my_airtable import url, get_request_webclient, get_request_requests

__fullframeengine__ = True  # must be set in order for requests to work


AT_TO_REVIT_MAPPING = {
    "#GWP Regional Baseline": "#GWP_Regional",
    "#GWP Conservative Estimate": "#GWP_Estimate",
    "#Material Plant": "#Plant_Name",
    "Airtable Id" : "#Airtable_Record_Id"
}

def process_records(air_records):
    """
    Takes list of records and converts into a dictionary with the material name as key
    """
    outdict = {}
    for rec in air_records:
        record_dict = {}
        record_dict["Airtable Id"] = rec["id"] #storing the airtable record id
        for key, value in rec["fields"].items():
            if key in AT_TO_REVIT_MAPPING.keys():
                record_dict[key] = value

        outdict[rec["fields"]["Material Name"]] = record_dict
    return outdict

##################################################
# Collect records from Airtable base
##################################################
#NOTE THE REQUESTS MODULE VERSION OF THE FUNCTION IS NOT WORKING ON VIRTUAL MACHINES
#(USE THE WEBCLIENT VERSION INSTEAD IF ON VIRTUAL MACHINE)

#USING REQUESTS MODULE
airtable_response = get_request_requests(url)

#USING WEBCLIENT
#airtable_response = get_request_webclient(url)

all_mat_records = airtable_response["records"]

mat_dict = process_records(all_mat_records)


##################################################
# Ask user what materials to update
##################################################
mats_to_update = forms.SelectFromList.show(
    sorted(mat_dict.keys()),
    multiselect=True,
    button_name="Update Materials",
    title="Select Materials to Update"
)

#Exit if nothing selected
if not mats_to_update:
    UI.TaskDialog.Show(
        "Invalid Selection", "Please select at least one Material to update."
    )
    sys.exit()

##################################################
# Retrieve matching material and update
##################################################

mat_collector = db.Collector(of_class="Material",
                             where=lambda x: x.Name in mats_to_update)

with db.Transaction("Updating Revit Materials"):
    for mat in mat_collector:
        property_dict = mat_dict[mat.Name]
        for key, value in property_dict.items():
            rev_param_name = AT_TO_REVIT_MAPPING[key]
            rev_param = mat.LookupParameter(rev_param_name)
            rev_param.Set(value)
