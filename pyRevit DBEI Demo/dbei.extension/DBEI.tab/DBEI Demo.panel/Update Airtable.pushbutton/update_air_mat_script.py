__author__ = "Jared Friedman"
__title__ = "Update Airtable\n Materials"
__doc__ = """

Updates Airtable Comments from Revit Schedule

This tool will update the #Comments field in Airtable based on Comments in a Revit material.
"""

import sys

from rpw import db, UI
from rpw.ui.forms import Console

from pyrevit import forms

import posixpath

from my_airtable import url, patch_request_webclient, patch_request_requests


__fullframeengine__ = True  # must be set in order for requests to work


def update_records(url, record_dict):
    '''
    Places a PATCH request in order to update existing records in Airtable
    '''
    for id, data in record_dict.items():
        record_url = posixpath.join(url, id)
        fields_dict = {"fields" : {"#Comments": data}}

        #NOTE: You can use either the WebClient or the requests module to make the PATCH request

        #PATCH REQUEST USING REQUESTS MODULE (NOT WORKING ON VIRTUAL MACHINES)
        patch_request_requests(record_url, fields_dict)

        #PATCH REQUEST USING WEBCLIENT
        #patch_request_webclient(record_url, fields_dict)

def check_for_record_id(mat):
    '''
    Checks if a material has a valid Airtable record id
    '''
    record_id = mat.LookupParameter("#Airtable_Record_Id").AsString()
    if record_id and len(record_id) > 0:
        return True
    else:
        return False

##################################################
# Collect material for DBEI schedule
##################################################
mat_collector = db.Collector(of_class="Material",
                             where=lambda x: check_for_record_id(x))

mat_dict = {m.Name : m for m in mat_collector}


##################################################
# Ask user what materials to update
##################################################
mats_to_update = forms.SelectFromList.show(
    sorted(mat_dict.keys()),
    multiselect=True,
    button_name="Update Airtable",
    title="Select Materials to Update"
)

#Exit if nothing selected
if not mats_to_update:
    UI.TaskDialog.Show(
        "Invalid Selection", "Please select at least one Material to update."
    )
    sys.exit()


##################################################
# Update records in Airtable
##################################################

#Make a dictionary with the Airtable record as key and the Comments as value
mat_comments_dict = {m.LookupParameter("#Airtable_Record_Id").AsString() : m.LookupParameter("Comments").AsString() for m in mat_collector}

#NOTE If you are updating a large number of records, you may need to break this up into batches with delays to avoid API limits
update_records(url, mat_comments_dict)