"""This module implments utility functions for use with the Intelligent Plant APIs"""
__author__ = "Ross Kelso"
__docformat__ = 'reStructuredText'

import math
from functools import reduce
from datetime import datetime, timezone

import pandas as pd

def query_result_to_data_frame(result, include_dsn=False, force_numeric=False, force_string=False):
    """Convert the result of a data query into a data frame
       warn: this assumes that the timestamps for eachtag match (i.e. this won't work properly for raw queries)
       :param result: The parsed JSON result object. seealso: data_core_clinet.DataCoreClient.get_data(..)
       :param include_dsn: Whether or not to include the sata source name in the column name, defaul false.
       :param force_numeric: Force numeric values to be taken over string values. Default: False
       :param force_string: Force string values to be taken over numeric values. Default: False
       :return: A data frame with the queried tags as column headers and a row for each data point returned.
    """
    frame_data = {}
    

    assert not (bool(force_numeric) and bool(force_string)), f'At most one of force_numeric or force_string can be set. Numeric: {force_numeric}, String: {force_string}' 
    
    for dsn in result:
        #put the data data each tag into the data frame
        for (tag_name, tag_data) in result[dsn].items():
            if (include_dsn):
                name = dsn + "." + tag_name
            else:
                name = tag_name
            
            time_stamps = list(map(lambda x: pd.Timestamp(x["UtcSampleTime"]), tag_data["Values"]))
            selected_values = list(map(lambda x: float(x["NumericValue"]) if (force_numeric or x["IsNumeric"]) and (not force_string) else x["TextValue"], tag_data["Values"]))
            values = pd.Series(selected_values, index=time_stamps)

            frame_data[name] = values
    
    
    return pd.DataFrame(frame_data)

def construct_tag_value(tag_name, utc_sample_time = None, numeric_value = None, text_value = None, status = 'Good', unit = '', notes = None, error = None, properties = {}):
    """Construct a tag value object for use with the write_tag_value_snapshot(..) or write_tag_value_historical(..) functions

       :param tag_name: The pname of the tag to write to.
       :param utc_sample_time: The UTC sample time that should be recored with the timestamp. Default value: the current system time.
       :param numeric_value: The numeric value that should be written. Optional, for text values leave unspecified or None.
       :param text_value: The text value that should be written. Optional, for numeric values leave unspecified or None.
       :param status: The status of this tag value. Must be 'Good', 'Bad' or 'Uncertain'. Default: 'Good'
       :param unit: The unit value that should be written. Default: the empty string.
       :param notes: Any notes that should be written. Default: None.
       :param properties: Dictionary of generic properties to be written. Default {}

       :return: A tag value dictionary which can be used to write values to historians using data core.
    """
    
    assert numeric_value is not None or text_value is not None, 'Either numeric or text value must be specified'
    
    # set sample time to now if unspecified
    utc_sample_time = datetime.now(timezone.utc) if utc_sample_time is None else utc_sample_time
    
    # determine whether the value is numveric based on 
    is_numeric = True if numeric_value is not None else False
    
    # the text value is the string form of the numeric value if it is numeric
    text_value = str(numeric_value) if is_numeric else text_value
    
    # check that the status is the correct value
    assert status == 'Good' or status == 'Uncertain' or status == 'Bad', "Status must be 'Good', 'Uncertain' or 'Bad'"
    
    # check whether an error has been specified
    has_error = True if error is not None else False
    
    return {
        'TagName': tag_name,
        'UtcSampleTime': str(utc_sample_time),
        'NumericValue': numeric_value,
        'IsNumeric': is_numeric,
        'TextValue': text_value,
        'Status': status,
        'Unit': unit,
        'Notes': notes,
        'HasError': has_error,
        'Properties': properties
    }

def construct_tag_definition(tag_name, current_value=None, description='', digital_states=[], is_meta_tag=False, original_name='', properties={}, unit_of_measure=''):
    """Construct the tag defintion object as required by the DataCoreClient.create_tag(..) function.

    :param tag_name: The name of the tag to be created.
    :param current_value: The current value of the tag to be created. Optional, default None.
    :param description: The tag description. Optional, defaults to the empty string.
    :param digital_states: A list of digital states this tag has. Optional, defaults to an empty list.
    :param is_meta_tag: Should be set if this is a meta-tag. Optional, default False.
    :param original_name: Tags original name.
    :param properties: Additional tag proeprties as required by data source implmentation.
    :param unit_of_measure: The unit used to measure this tag.

    :return: A tag defintoion object.
    """
    return {
        'CurrentValue': current_value,
        'Description': description,
        'DigitalStates': digital_states,
        'IsMetaTag': is_meta_tag,
        'Name': tag_name,
        'OriginalName': original_name,
        'Properties': properties,
        'UnitOfMeasure': unit_of_measure
    }

def construct_tag_definition_property(name, value, category=None, description=None, display_index=0, is_read_only=False, is_write_only=False, use_long_text_editor=False):
    """Construct tag defintion property object used in construct_tag_definition(..).

    :param name: The name of property.
    :param value: The value of the property
    :param description: The proeprty description. Optional, defaults to None.
    :param digital_states: A list of digital states this tag has. Optional, defaults to an empty list.


    :return: A tag definition property object.
    """
    return {
        'Name': name,
        'Value': value,
        'Category': category,
        'Description': description,
        'IsReadOnly': is_read_only,
        'IsWriteOnly': is_write_only,
        'DisplayIndex': display_index,
        'UseLongTextEditor': use_long_text_editor
    }
