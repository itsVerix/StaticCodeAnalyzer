def spaces_cnt(line):
    nbr_of_spaces = 0
    for character in line:
        if character == " ":
            nbr_of_spaces += 1
        else:
            break
    return nbr_of_spaces
