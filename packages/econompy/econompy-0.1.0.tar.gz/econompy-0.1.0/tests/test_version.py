from econompy import __version__


def test_is_version_str() -> None:
    assert isinstance(__version__, str)
