def compare_vectors(vec1, vec2):
    """Inputs: vec1 and vec2 are same-length, 1d numpy arrays of line y-data.
    Calculates Euclidean Distance between vec1 and vec2.
    returns: euclidean distance between vec1 and vec2."""

    if len(vec1) != len(vec2):
        print(  "Vec1 length {} != vec2 length {},".format(len(vec1), len(vec2),
                " comparison will fail.")
        return -1

    return np.linalg.norm(vec1 - vec2)
        
