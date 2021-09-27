import ford
from textwrap import dedent
import pytest


def test_quiet_false():
    """This checks that bool options like 'quiet' are parsed correctly in input md file"""

    data, _, _ = ford.parse_arguments({}, "quiet: false")
    assert data["quiet"] is False
    data, _, _ = ford.parse_arguments({}, "quiet: TRUE")
    assert data["quiet"] is True


def test_quiet_command_line():
    """Check that setting --quiet on the command line overrides project file"""

    data, _, _ = ford.parse_arguments({"quiet": True}, "quiet: false")
    assert data["quiet"] is True
    data, _, _ = ford.parse_arguments({"quiet": False}, "quiet: true")
    assert data["quiet"] is False


def test_list_input():
    """Check that setting a non-list option is turned into a single string"""

    settings = """\
    include: line1
             line2
    summary: This
             is
             one
             string
    """
    data, _, _ = ford.parse_arguments({}, dedent(settings))

    assert len(data["include"]) == 2
    assert data["summary"] == "This\nis\none\nstring"


def test_path_normalisation():
    """Check that paths get normalised correctly"""

    settings = """\
    page_dir: my_pages
    src_dir: src1
             src2
    """
    data, _, _ = ford.parse_arguments({}, dedent(settings), "/prefix/path")
    assert data["page_dir"] == "/prefix/path/my_pages"
    assert data["src_dir"] == ["/prefix/path/src1", "/prefix/path/src2"]


def test_source_not_subdir_output():
    """Check if the src_dir is correctly detected as being a subdirectory of output_dir"""

    # This should be fine
    data, _, _ = ford.parse_arguments(
        {"src_dir": ["/1/2/3"], "output_dir": "/3/4"}, "", "/prefix"
    )

    # This shouldn't be
    with pytest.raises(ValueError):
        data, _, _ = ford.parse_arguments(
            {"src_dir": ["/1/2/3"], "output_dir": "/1/2"}, "", "/prefix"
        )


def test_repeated_docmark():
    """Check that setting --quiet on the command line overrides project file"""

    settings = """\
    docmark: !
    predocmark: !
    """

    with pytest.raises(ValueError):
        ford.parse_arguments({}, dedent(settings))

    settings = """\
    docmark: !<
    predocmark_alt: !<
    """

    with pytest.raises(ValueError):
        ford.parse_arguments({}, dedent(settings))

    settings = """\
    docmark_alt: !!
    predocmark_alt: !!
    """

    with pytest.raises(ValueError):
        ford.parse_arguments({}, dedent(settings))