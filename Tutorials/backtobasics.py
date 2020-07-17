
def extract_data_with_for_loops(data):
    # data: string of a table
    table = [] # ready to catch our lists of row items
    # loop through each row by splitting in '\n'  (newline)
    for i in data.split('\n'):
        # i.split('\t') = list of values in each row
        table.append(i.split('\t') ) # add to list
    header = table[0] # first row -

    index = []
    for i in table[1:]:
        index.append(i[0]) # first item in each row (except the headers)

    values = []
    for i in table[1:]:
        values.append(i[1:])
    # make the strings of numbers into floats
    float_values = []
    for row in values:
        float_row = []
        for val in row:
            float_row.append(float(val))
        float_values.append(float_row)

    # we're maing a dictionary of dictionaries
    d1 = {} # d1 will contain {amino_acid1: {property1: 0.2, ...}, amino_acid2: {...} ... }
    for aa, row in zip(index, values): # use zip(iterable1, iterable2,...) to iterate through multiple variables at once
        # we have the amino_acid name  as a string and the row of properties as a list
        # we want to label each property with its name with another dictionary
        d2 = {}
        for val, feature in zip(row, header):
            d2[feature] = val
        d1[aa] = d2
    return d1


def extract_data_with_list_comprehensions(data):
    # data: string of a table
    table = [i.split('\t') for i in data.split('\n')]
    header = table[0]
    index = [i[0] for i in table[1:]]
    values = [[float(val) for val in i[1:]] for i in table[1:]]
    dictionary = {j:dict(zip(header, i)) for i,j in zip(values, index)}
    return dictionary
