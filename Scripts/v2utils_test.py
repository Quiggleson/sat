from v2_utils import todict

def count_rope(rope: dict, length=-1):
    """
    Count the number of total clauses in rope (should be 6 * len(instance))
    """

    # track count
    count = 0

    # iterate keys in rope
    for key in rope:

        # if key is 0 
        if key == "0":

            # if counting the current length
            if length == -1 or len(rope[key]) == length:
                # count clause as found
                count += 1

        # else if the key is not 0, a subdictionary exists
        elif key != "0":

            # search for clauses in child - found gets modified in place
            count += count_rope(rope[key], length)
            
    # return found clauses
    return count

def test_rope_len():
    clauses = [
        [1, 2, 3],
        [1, 2, -3],
        [1, -2, 3],
        [1, -2, -3],
        [-1, -2, 3],
    ]
    rope = todict(clauses)
    assert count_rope(rope) == 6 * len(clauses), "the instance is sorted into a dict incorrectly"