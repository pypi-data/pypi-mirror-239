import pyarrow.compute as pc


def _calculate_column_mean(
    table,
    column_name: str
) -> float:
    return pc.mean(table[column_name]).as_py()


def expect_column_mean_greater_than(
    table,
    column_name: str,
    value: float
):
    """
    Given a column name, expect the mean of that column to be greater than value
    """
    _mean = _calculate_column_mean(table, column_name)
    assert _mean > value, 'Expected mean of column {} to be greater than {}, but got {}'.format(column_name, value, _mean)

    return True


def expect_column_mean_smaller_than(
    table,
    column_name: str,
    value: float
):
    """
    Given a column name, expect the mean of that column to be smaller than value
    """
    _mean = _calculate_column_mean(table, column_name)
    assert _mean < value, 'Expected mean of column {} to be smaller than {}, but got {}'.format(column_name, value, _mean)

    return True
