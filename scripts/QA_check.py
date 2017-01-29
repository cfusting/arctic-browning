# return the qa flag(0/1) for the given 2d quality information array...
def qa_check(qa):
    import numpy

    """ QA filter from 2 byte VI Quality layer value
    See the detail of QA in
    https://lpdaac.usgs.gov/products/modis_products_table/mod13q1
    """
    rows = qa.shape[0]
    cols = qa.shape[1]
    bits = numpy.zeros(shape=(rows, cols, 16),
                       dtype='uint8')  # 16 because quality comes as uint 16, one one stores the ith bit
    for i in range(0, 16):
        cur_bit = qa % 2
        qa = qa - qa % 2
        qa = qa / 2
        bits[:, :, i] = cur_bit

    # creating qa numbers using information provided in metadata
    qa0_1 = bits[:, :, 0] + bits[:, :, 1] * 2  # bits 0 & 1
    qa2_5 = bits[:, :, 2] + bits[:, :, 3] * 2 + bits[:, :, 4] * 4 + bits[:, :, 5] * 8  # bits 2-5 VI usefulness
    qa6_7 = bits[:, :, 6] + bits[:, :, 7] * 2  # bits 6-7 aerosol
    qa8 = bits[:, :, 8]  # bit 8 Adjacent cloud detected
    qa10 = bits[:, :, 10]  # bit 10 Mixed clouds
    qa15 = bits[:, :, 15]  # bit 15 Possible shadow

    # creating a logical array based on different quality flags
    # result = numpy.logical_and(qa6_7<=2,qa0_1<=1)
    # result = numpy.logical_and(result,qa8==0)
    # result = numpy.logical_and(result,qa10==0)
    # result = numpy.logical_and(result,qa15==0)

    result = numpy.logical_and(qa0_1 <= 1, qa8 == 0)
    result = numpy.logical_and(result, qa10 == 0)
    result = numpy.logical_and(result, qa15 == 0)
    result = numpy.logical_and(result, qa2_5 <= 11)
    dummy = numpy.logical_or(qa6_7 == 1, qa6_7 == 2)
    result = numpy.logical_and(result, dummy)

    return result
