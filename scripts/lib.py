def build_qa_mask(iarray, rarray):
    """build an array mask.

    :param iarray: input arrray (ndvi)
    :param rarray: reliability array. Resulting mask is stored here.
    :return:
    """
    #rarray[rarray == 1] = 0
    rarray[iarray == -3000] = 1
    rarray[rarray != 0] = 1
