import re

def extract_code(text):
    pattern = r'(```[\s\S]+?```)'  # Add capturing group with parentheses
    segments = re.split(pattern, text)
    return segments

def split_string(input_string):
    max_size = 2000
    # check if there is a code block in the output
    if '```' in input_string:
        input_string = extract_code(input_string)
    else:
        input_string = [input_string]

    # Loop through the resulting strings and split the string if it is too long.
    new_strings = []
    for s in input_string:
        if len(s) >= max_size:
            s = s.split('\n')
            mes = ""
            for line in s:
                if len(mes) + len(line) >= max_size:
                    new_strings.append(mes)
                    mes = line + "\n"
                else:
                    mes += line + "\n"
            new_strings.append(mes)
        else:
            new_strings.append(s)

    # Return the list of strings
    return new_strings

