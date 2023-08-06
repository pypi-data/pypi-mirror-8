from nose.tools import assert_raises

from eelbrain.plot._base import Layout


def assert_layout_ok(*args, **kwargs):
    error = None
    l = Layout(*args, **kwargs)
    if l.nrow * l.ncol < l.nax:
        error = ("%i rows * %i cols = %i < %i (nax). args=%%r, kwargs=%%r"
                 % (l.nrow, l.ncol, l.nrow * l.ncol, l.nax))

    if error:
        raise AssertionError(error % (args, kwargs))


def test_layout():
    "Test the Layout class"
    for nax in xrange(1, 100):
        assert_layout_ok(nax, 1.5, 2, True, w=5)
        assert_layout_ok(nax, 1.5, 2, True, h=5)
        assert_layout_ok(nax, 1.5, 2, True, axw=5)
        assert_layout_ok(nax, 1.5, 2, True, axh=5)
        assert_layout_ok(nax, 1.5, 2, True, axw=5, w=20)
        assert_layout_ok(nax, 1.5, 2, True, axw=5, h=20)
        assert_layout_ok(nax, 1.5, 2, True, axh=5, w=20)
        assert_layout_ok(nax, 1.5, 2, True, axh=5, h=20)

    # single axes larger than figure
    assert_raises(ValueError, Layout, 2, 1.5, 2, True, h=5, axh=6)
    assert_raises(ValueError, Layout, 2, 1.5, 2, True, w=5, axw=6)
