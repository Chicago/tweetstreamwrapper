# first pass at filter for tweet document object
# this method treats the tweet object and a "white list" filter
# object as "sets" and takes the intersection of the two objects
# since the filter object is a whitelist, and we are looking for
# an intersection (overlap), all fields will be ignored by default
# and only fields in the whitelist will be captured
def get_intersection(json_object, white_list):
    r_dict = {}
    for value in white_list:
        nested_values = white_list[value]
        if nested_values != None:
            i_dict = {}
            for nested_value in nested_values:
                i_dict[nested_value] = json_object[value][nested_value]
            r_dict[value] = i_dict        
        elif value in json_object:
           r_dict[value] = json_object[value]
    return r_dict
