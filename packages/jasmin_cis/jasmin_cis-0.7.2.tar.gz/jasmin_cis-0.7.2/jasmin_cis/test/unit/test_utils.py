import numpy
from jasmin_cis.exceptions import InvalidCommandLineOptionError
from jasmin_cis.utils import apply_intersection_mask_to_two_arrays, calculate_histogram_bin_edges, \
    split_into_float_and_units, parse_distance_with_units_to_float_km, parse_distance_with_units_to_float_m, \
    array_equal_including_nan, apply_mask_to_numpy_array
from nose.tools import istest, eq_, raises

@istest
def can_apply_intersection_mask_to_two_masked_arrays():
    import numpy.ma as ma
    import numpy as np
    array1 = ma.array([1,2,3,4,5,6,7,8,9,10], mask=[1,1,1,0,0,0,0,0,0,0])
    array2 = ma.array([2,4,5,6,7,8,4,3,6,80], mask=[0,1,0,0,0,0,0,1,0,0])
    array1, array2 = apply_intersection_mask_to_two_arrays(array1, array2)
    assert(np.equal(array1.mask, [1,1,1,0,0,0,0,1,0,0]).all())
    assert(np.equal(array2.mask, [1,1,1,0,0,0,0,1,0,0]).all())

@istest
def can_apply_intersection_mask_to_three_masked_arrays():
    import numpy.ma as ma
    array1 = ma.array([1,2,3,4,5,6,7,8,9,10], mask=[1,1,1,0,0,0,0,0,0,0])
    array2 = ma.array([2,4,5,6,7,8,4,3,6,80], mask=[0,1,0,0,0,0,0,1,0,0])
    array3 = ma.array([2,4,5,6,7,8,4,3,6,80], mask=[0,0,0,0,0,0,0,0,0,1])
    array1, array2 = apply_intersection_mask_to_two_arrays(array1, array2)
    array1, array3 = apply_intersection_mask_to_two_arrays(array1, array3)
    array1, array2 = apply_intersection_mask_to_two_arrays(array1, array2)

    assert(ma.equal(array1.mask, [1,1,1,0,0,0,0,1,0,1]).all())
    assert(ma.equal(array2.mask, [1,1,1,0,0,0,0,1,0,1]).all())
    assert(ma.equal(array3.mask, [1,1,1,0,0,0,0,1,0,1]).all())


@istest
def can_apply_intersection_mask_to_one_masked_and_one_unmasked_array():
    import numpy.ma as ma
    import numpy as np
    array1 = ma.array([1,2,3,4,5,6,7,8,9,10], mask=[1,1,1,0,0,0,0,0,0,0])
    array2 = np.array([2,4,5,6,7,8,4,3,6,80])
    array1, array2 = apply_intersection_mask_to_two_arrays(array1, array2)
    assert(np.equal(array1.mask, [1,1,1,0,0,0,0,0,0,0]).all())
    assert(np.equal(array2.mask,[1,1,1,0,0,0,0,0,0,0]).all())

@istest
def can_apply_intersection_mask_to_two_unmasked_arrays():
    import numpy as np
    array1 = np.array([1,2,3,4,5,6,7,8,9,10])
    array2 = np.array([2,4,5,6,7,8,4,3,6,80])
    array1, array2 = apply_intersection_mask_to_two_arrays(array1, array2)
    assert(all(array1.mask)== False)
    assert(all(array2.mask)== False)

@istest
def can_expand_1d_array_across():
    import numpy as np
    from jasmin_cis.utils import expand_1d_to_2d_array
    a = np.array([1,2,3,4])
    b = expand_1d_to_2d_array(a, 4, axis=0)
    ref = np.array([[1, 2, 3, 4],[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]])
    assert(np.equal(b, ref).all())

@istest
def can_expand_1d_array_down():
    import numpy as np
    from jasmin_cis.utils import expand_1d_to_2d_array
    a = np.array([1,2,3,4])
    b = expand_1d_to_2d_array(a, 4, axis=1)
    ref = np.array([[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]])
    assert(np.equal(b, ref).all())

@istest
def ten_bins_are_created_by_default():
    from numpy import array
    data = array([0.0, 1.0, 2.0, 3.0])
    val_range = {}
    step = None

    bin_edges = calculate_histogram_bin_edges(data, "x", val_range, step)
    eq_(len(bin_edges), 11) # 11 edges = 10 bins
    eq_(bin_edges.min(), data.min())
    assert(abs(bin_edges.max() - data.max()) < 1.e-7)

@istest
def bin_width_can_be_specified_where_bin_width_perfectly_divides_range():
    from numpy import array
    data = array([0.0, 1.0, 2.0, 3.0])
    val_range = {}
    step = 0.5

    bin_edges = calculate_histogram_bin_edges(data, "x", val_range, step)
    eq_(len(bin_edges), 7)
    eq_(bin_edges.min(), data.min())
    eq_(bin_edges.max(), data.max())

@istest
def bin_width_can_be_specified_where_bin_width_does_not_perfectly_divides_range():
    from numpy import array
    data = array([0.0, 1.0, 2.0, 3.0])
    val_range = {}
    step = 0.7

    bin_edges = calculate_histogram_bin_edges(data, "x", val_range, step)
    eq_(len(bin_edges), 5)
    eq_(bin_edges.min(), data.min())
    assert(bin_edges.max() < data.max())

@istest
def ten_bins_are_created_when_min_is_specified():
    from numpy import array
    data = array([0.0, 1.0, 2.0, 3.0])
    val_range = {"xmin" : 0.3}
    step = None

    bin_edges = calculate_histogram_bin_edges(data, "x", val_range, step)
    eq_(len(bin_edges), 11) # 11 edges = 10 bins
    eq_(bin_edges.min(), 0.3)
    assert(abs(bin_edges.max() - data.max()) < 1.e-7) # 1.e-7 is approx 0

@istest
def ten_bins_are_created_when_max_is_specified():
    from numpy import array
    data = array([0.0, 1.0, 2.0, 3.0])
    val_range = {"xmax" : 2.3}
    step = None

    bin_edges = calculate_histogram_bin_edges(data, "x", val_range, step)
    eq_(len(bin_edges), 11) # 11 edges = 10 bins
    eq_(bin_edges.min(), data.min())
    assert(abs(bin_edges.max() - 2.3) < 1.e-7) # 1.e-7 is approx 0'''

@istest
def ten_bins_are_created_when_min_and_max_is_specified():
    from numpy import array
    data = array([0.0, 1.0, 2.0, 3.0])
    val_range = {"xmin" : 0.3, "xmax" : 2.3}
    step = None

    bin_edges = calculate_histogram_bin_edges(data, "x", val_range, step)
    eq_(len(bin_edges), 11) # 11 edges = 10 bins
    assert(abs(bin_edges.min() - 0.3) < 1.e-7) # 1.e-7 is approx 0
    assert(abs(bin_edges.max() - 2.3) < 1.e-7) # 1.e-7 is approx 0


@istest
def test_split_into_float_and_units():
    eq_(split_into_float_and_units('10km')['value'], 10)
    eq_(split_into_float_and_units('10km')['units'], 'km')


@istest
def test_split_into_float_and_units_with_spaces():
    eq_(split_into_float_and_units('10 km')['value'], 10)
    eq_(split_into_float_and_units('10 km')['units'], 'km')


@istest
def test_split_into_float_and_units_with_full_float():
    eq_(split_into_float_and_units('12.3e4uM')['value'], 12.3e4)
    eq_(split_into_float_and_units('12.3e4uM')['units'], 'uM')


@istest
@raises(InvalidCommandLineOptionError)
def test_split_into_float_and_units_with_extra_numbers():
    split_into_float_and_units('10km10')


@istest
@raises(InvalidCommandLineOptionError)
def test_split_into_float_and_units_with_no_numbers():
    split_into_float_and_units('km')


@istest
def test_split_into_float_and_units_with_no_units():
    eq_(split_into_float_and_units('10')['value'], 10)
    eq_(split_into_float_and_units('10')['units'], None)


@istest
@raises(InvalidCommandLineOptionError)
def test_split_into_float_and_units_with_extra_units():
    eq_(split_into_float_and_units('km10m'), 10)


@istest
def test_parse_distance_with_units_of_km_to_float_km():
    eq_(parse_distance_with_units_to_float_km('10km'), 10)


@istest
def test_parse_distance_with_units_of_m_to_float_km():
    eq_(parse_distance_with_units_to_float_km('10000m'), 10)


@istest
def test_parse_distance_without_units_to_float_km():
    eq_(parse_distance_with_units_to_float_km('10'), 10)


@istest
@raises(InvalidCommandLineOptionError)
def test_parse_distance_with_invalid_units():
    eq_(parse_distance_with_units_to_float_km('10Gb'), 10)


@istest
def test_parse_distance_with_units_of_m_to_float_m():
    eq_(parse_distance_with_units_to_float_m('10m'), 10)


@istest
def test_parse_distance_with_units_of_km_to_float_m():
    eq_(parse_distance_with_units_to_float_m('10km'), 10000)


@istest
def test_parse_distance_without_units_to_float_m():
    eq_(parse_distance_with_units_to_float_m('10'), 10)

@istest
def test_array_equal_including_nan():
    array1 = numpy.array([[1, 2], [3, 4]])
    array2 = numpy.array([[1, 2], [3, 4.1]])
    array3 = numpy.array([[1, 2], [3, float('nan')]])
    assert array_equal_including_nan(array1, array1)
    assert not array_equal_including_nan(array1, array2)
    assert not array_equal_including_nan(array1, array3)
    assert array_equal_including_nan(array3, array3)

# Tests for apply_mask_to_numpy_array
@istest
def test_apply_mask_to_numpy_array_with_unmasked_array():
    # Input array not a masked array to which is applied a mask containing 'True's
    in_array = numpy.array([1, 2, 3, 4])
    mask = numpy.array([False, False, True, False])
    out_array = apply_mask_to_numpy_array(in_array, mask)
    assert numpy.array_equal(out_array.mask, mask)

@istest
def test_apply_mask_to_numpy_array_with_masked_array():
    # Input array has masked points to which is applied a mask containing 'True's
    in_array = numpy.ma.array([1, 2, 3, 4], mask=numpy.array([True, False, False, False]))
    mask = numpy.array([False, False, True, False])
    out_array = apply_mask_to_numpy_array(in_array, mask)
    assert numpy.array_equal(out_array.mask, numpy.array([True, False, True, False]))

@istest
def test_apply_mask_to_numpy_array_with_masked_array_with_nomask():
    # Input array is a masked array but with mask 'nomask'. This is masked by a mask with no 'True's.
    # The output array should not have had a mask created.
    in_array = numpy.ma.array([1, 2, 3, 4], mask=numpy.ma.nomask)
    mask = numpy.array([False, False, False, False])
    out_array = apply_mask_to_numpy_array(in_array, mask)
    assert numpy.ma.getmask(out_array) is numpy.ma.nomask

@istest
def test_apply_mask_to_numpy_array_with_masked_array_but_all_unmasked():
    # Input array is a masked array but no elements are masked. The mask contains no 'True's.
    # This is masked by a mask with no 'True's. The output array should not have had a mask created.
    in_array = numpy.ma.array([1, 2, 3, 4], mask=numpy.array([False, False, False, False]))
    mask = numpy.array([False, False, False, False])
    out_array = apply_mask_to_numpy_array(in_array, mask)
    assert numpy.array_equal(out_array.mask, mask)

@istest
def test_apply_mask_to_numpy_array_with_masked_array_with_array_unmasked():
    # Input array is a masked array but with mask 'nomask'. This is masked by a mask with 'True's.
    # The output array should not have had a mask created.
    in_array = numpy.ma.array([1, 2, 3, 4], mask=numpy.ma.nomask)
    mask = numpy.array([False, True, False, True])
    out_array = apply_mask_to_numpy_array(in_array, mask)
    assert numpy.array_equal(out_array.mask, mask)
