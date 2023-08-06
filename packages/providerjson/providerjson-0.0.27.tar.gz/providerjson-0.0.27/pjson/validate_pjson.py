#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars
import json, sys

from pjson.validate_basic import validate_basic_dict
from pjson.validate_addresses import validate_address_list
from pjson.validate_licenses import validate_license_list
from pjson.validate_direct_addresses import validate_direct_address_list
from pjson.validate_taxonomies import validate_taxonomy_list
from pjson.validate_identifiers import validate_identifier_list
from pjson.validate_other_names import validate_other_name_list

#from validate_basic import validate_basic_dict
#from validate_addresses import validate_address_list
#from validate_licenses import validate_license_list
#from validate_direct_addresses import validate_direct_address_list
#from validate_taxonomies import validate_taxonomy_list
#from validate_identifiers import validate_identifier_list
#from validate_other_names import validate_other_name_list


def validate_pjson(j):
    """
    Input a JSON object as a string. return a list of errors. If error list
    is empty then the file is valid.
    """
    errors =[]
    warnings =[]
    response = { "errors": [], "warnings": [] }
    
    
    # Does the string contain JSON
    try:
        d = json.loads(j)
    except:
        error ="The string did not contain valid JSON."
        errors.append(error)
        response["errors"] = errors
        return response

    # Is it a dict {} (JSON object equiv)?
    if type(d)!=type({}):
        error ="The JSON string did not contain a JSON object i.e. {}."
        errors.append(error)
        response["errors"] = errors
        return response

    # Does it contain the top-level enumeration_type
    if not d.has_key("enumeration_type"):
        error ="The JSON object does not contain an enumeration_type."
        errors.append(error)
        response["errors"] = errors
        return response


    # Is the enumeration_type a valid?
    if d["enumeration_type"] not in ("NPI-1", "NPI-2", "OEID", "HPID"):
        error ="enumeration_type must be one of these: ('NPI-1', 'NPI-2', 'OEID', 'HPID')"
        errors.append(error)
        response["errors"] = errors
        return response

    #If a number is present we assume this is an update.
    if not d.has_key("number"):
        number = None
    else:
        number = d['number']

    # Sanity check epoch dates
    if d.has_key("last_updated_epoch"):
        if type(d["last_updated_epoch"]) != type(1):
            warning ="last_updated_epoch is not an integer."
            warnings.append(warning)
    else:
        warning ="last_updated_epoch is missing."
        warnings.append(warning)
            
    if d.has_key("created_epoch"):
        if type(d["created_epoch"]) != type(1):
            warning ="created_epoch is not an integer."
            warnings.append(warning)
    else:
        warning ="created_date_epoch is missing."
        warnings.append(warning)


    #Check for errors in the basic section
    basic_errors = validate_basic_dict(d['basic'], d['enumeration_type'], number)


    #Check for errors in the basic section
    address_errors = validate_address_list(d['addresses'], d['enumeration_type'])


    #Check for errors in the license section

    if d.has_key('licenses'):
        license_errors = validate_license_list(d['licenses'], d['enumeration_type'])
    else:
        license_errors = []
   
    taxonomy_errors = validate_taxonomy_list(d['taxonomies'], d['enumeration_type'],
                        d.get('licenses', []), d['basic'].get('sole_proprietor', "NO"))

    if d.has_key('identifiers'):
        identifier_errors = validate_identifier_list(d['identifiers'], d['enumeration_type'])
    else:
        identifier_errors = []

    if d.has_key('direct_addresses'):
        direct_errors = validate_direct_address_list(d['direct_addresses'], d['enumeration_type'])
    else:
        direct_errors = []
         
    if d.has_key('other_names'):
        other_names_errors = validate_other_name_list(d['other_names'], d['enumeration_type'], d['basic'])
    else:
        other_names_errors = []    

    errors = errors + basic_errors + other_names_errors + address_errors + license_errors + \
                        direct_errors + taxonomy_errors + identifier_errors

    response["errors"] = errors
    response["warnings"] = warnings
    return response


if __name__ == "__main__":

    if len(sys.argv)<2:
        print "You must suppy a ProviderJSON file to validate."
        print "Usage: validate-pjson [ProivderJSON]"
        sys.exit(1)
    else:
        pjson_file = sys.argv[1]



    #Open the file

    try:
        fh = open(pjson_file, 'r')

        j = fh.read()

        errors = validate_pjson(j)

        errors_json =  json.dumps(errors, indent =4)
        print errors_json
    except IOError:
        print "Could not open file %s." % (pjson_file)
        sys.exit(1)




