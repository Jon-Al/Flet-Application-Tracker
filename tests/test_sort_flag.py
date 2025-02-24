from subprojects.data_view import SortFlag


def test_sort_flag_cycling():
    state = SortFlag.NONE
    assert state == SortFlag.NONE

    # First full cycle
    state = state.next()
    assert state == SortFlag.ASCENDING
    state = state.next()
    assert state == SortFlag.DESCENDING
    state = state.next()
    assert state == SortFlag.NONE

    # Second full cycle
    state = state.next()
    assert state == SortFlag.ASCENDING
    state = state.next()
    assert state == SortFlag.DESCENDING
    state = state.next()
    assert state == SortFlag.NONE


def test_sort_flag_equality():
    assert SortFlag.NONE == "NONE"
    assert SortFlag.NONE == 0
    assert SortFlag.ASCENDING == "ASCENDING"
    assert SortFlag.ASCENDING == 1
    assert SortFlag.DESCENDING == "DESCENDING"
    assert SortFlag.DESCENDING == 2
    assert SortFlag.ASCENDING != "descending"
    assert SortFlag.DESCENDING != 1
    assert SortFlag.NONE != "ascending"


def test_sort_flag_next():
    assert SortFlag.NONE.next() == SortFlag.ASCENDING
    assert SortFlag.ASCENDING.next() == SortFlag.DESCENDING
    assert SortFlag.DESCENDING.next() == SortFlag.NONE


def test_sort_flag_eq_with_integers():
    assert SortFlag.NONE == 0
    assert SortFlag.ASCENDING == 1
    assert SortFlag.DESCENDING == 2
    assert SortFlag.ASCENDING != 2
    assert SortFlag.DESCENDING != 1


def test_sort_flag_eq_with_strings():
    assert SortFlag.NONE == "NONE"
    assert SortFlag.ASCENDING == "ASCENDING"
    assert SortFlag.DESCENDING == "DESCENDING"
    assert SortFlag.NONE != "ASCENDING"
    assert SortFlag.ASCENDING != "DESCENDING"


def test_sort_flag_eq_with_case_insensitive_strings():
    assert SortFlag.NONE == "none"
    assert SortFlag.ASCENDING == "ascending"
    assert SortFlag.DESCENDING == "descending"


def test_sort_flag_eq_invalid_comparisons():
    assert (SortFlag.NONE == "INVALID") is False
    assert (SortFlag.ASCENDING == 99) is False
    assert (SortFlag.DESCENDING == None) is False
