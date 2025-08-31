import json
import pprint

from google.protobuf import json_format

import profile_pb2


def search_id(obj_id: int, obj_list: list):
    for obj in obj_list:
        if obj.id == obj_id:
            return obj
    return None


def decode_function(function, string_table: list) -> dict:
    function_dict = {
        'name': string_table[function.name],
        'system_name': string_table[function.system_name],
        'filename': string_table[function.filename],
        'start_line': function.start_line
    }
    return function_dict


def decode_line(line, functions: list, string_table: list) -> dict:
    function_id = line.function_id
    function = search_id(function_id, functions)
    function_dict = decode_function(function, string_table)
    line_dict = {
        'function': function_dict,
        'line': line.line,
    }
    return line_dict


def decode_mapping(mapping, string_table: list) -> dict | None:
    if mapping is None:
        return None
    mapping_dict = {
        'memory_start': mapping.memory_start,
        'memory_limit': mapping.memory_limit,
        'file_offset': mapping.file_offset,
        'filename': string_table[mapping.filename],
        'build_id': string_table[mapping.build_id],
        'has_functions': mapping.has_functions,
        'has_filenames': mapping.has_filenames,
        'has_line_numbers': mapping.has_line_numbers,
        'has_inline_frames': mapping.has_inline_frames
    }
    return mapping_dict


def decode_location(location, mappings: list, functions: list, string_table: list) -> dict:
    lines = location.line
    line_dicts = []
    for line in lines:
        line_dicts.append(decode_line(line, functions, string_table))
    mapping_id = location.mapping_id
    mapping = search_id(mapping_id, mappings)
    mapping_dict = decode_mapping(mapping, string_table)
    location_dict = {
        'mapping': mapping_dict,
        'address': location.address,
        'line': line_dicts,
        'is_folded': location.is_folded,
    }
    return location_dict


def decode_label(label, string_table: list) -> dict:
    label_dict = {
        'key': string_table[label.key],
        'str': string_table[label.str],
        'num': label.num,
        'num_unit': string_table[label.num_unit]
    }
    return label_dict


def decode_sample(sample, locations: list, mappings: list, functions: list, string_table: list) -> dict:
    location_ids = sample.location_id
    location_dicts = []
    for location_id in location_ids:
        location = search_id(location_id, locations)
        location_dict = decode_location(location, mappings, functions, string_table)
        location_dicts.append(location_dict)
    labels = sample.label
    label_dicts = []
    for label in labels:
        label_dicts.append(decode_label(label, string_table))

    values = [value for value in sample.value]

    sample_dict = {
        'location': location_dicts,
        'value': values,
        'label': label_dicts
    }
    return sample_dict


def decode_value_type(value_type, string_table: list) -> dict:
    return {
        'type': string_table[value_type.type],
        'unit': string_table[value_type.unit]
    }


def decode_profile(profile) -> dict:
    samples = profile.sample
    mappings = profile.mapping
    locations = profile.location
    functions = profile.function
    string_table = profile.string_table
    sample_dicts = []

    for sample in samples:
        sample_dicts.append(decode_sample(sample, locations, mappings, functions, string_table))

    sample_types = profile.sample_type
    sample_type_dicts = []
    for sample_type in sample_types:
        sample_type_dicts.append(decode_value_type(sample_type, string_table))

    profile_dict = {
        'sample_type': sample_type_dicts,
        'samples': sample_dicts,
        'drop_frames': string_table[profile.drop_frames],
        'keep_frames': string_table[profile.keep_frames],
        'time_nanos': profile.time_nanos,
        'duration_nanos': profile.duration_nanos,
        'period_type': decode_value_type(profile.period_type, string_table),
        'period': profile.period,
        'comment': string_table[profile.comment] if profile.comment else None,
        'default_sample_type': string_table[profile.default_sample_type] if profile.default_sample_type else None,
    }
    return profile_dict

def main():
    with open('pprof.bin', 'rb') as f:
        binary_data = f.read()

    profile = profile_pb2.Profile()
    profile.ParseFromString(binary_data)
    print(profile)
    print(json.dumps(decode_profile(profile)))
    #print(json_format.MessageToDict(profile))


if __name__ == "__main__":
    main()
