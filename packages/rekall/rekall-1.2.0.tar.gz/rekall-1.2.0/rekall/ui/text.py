# Rekall Memory Forensics
# Copyright (C) 2012 Michael Cohen
# Copyright 2013 Google Inc. All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

"""This module implements a text based render.

A renderer is used by plugins to produce formatted output.
"""

try:
    import curses
    curses.setupterm()
except Exception:  # curses sometimes raises weird exceptions.
    curses = None

import logging
import re
import os
import string
import subprocess
import sys
import tempfile
import textwrap

from rekall import config
from rekall import registry
from rekall import utils

from rekall.ui import renderer as renderer_module


config.DeclareOption(
    "--pager", default=os.environ.get("PAGER"), group="Interface",
    help="The pager to use when output is larger than a screen full.")

config.DeclareOption(
    "--paging_limit", default=None, group="Interface", type="IntParser",
    help="The number of output lines before we invoke the pager.")

config.DeclareOption(
    "--nocolors", default=False, type="Boolean", group="Interface",
    help="If set suppress outputting colors.")


HIGHLIGHT_SCHEME = dict(
    important=("WHITE", "RED"),
    good=("GREEN", None),
    neutral=(None, None))


StyleEnum = utils.AttributeDict(
    address="address",
    value="value",
    compact="compact",
    full="full",
    hexdump="hexdump",
    cow="cow")


# This comes from http://docs.python.org/library/string.html
# 7.1.3.1. Format Specification Mini-Language
FORMAT_SPECIFIER_RE = re.compile(r"""
(?P<fill>[^{}<>=^bcdeEfFgGnLorsxX0-9])?  # The fill parameter. This can not be a
                                        # format string or it is ambiguous.
(?P<align>[<>=^])?     # The alignment.
(?P<sign>[+\- ])?      # Sign extension.
(?P<hash>\#)?          # Hash means to preceed the whole thing with 0x.
(?P<zerofill>0)?       # Should numbers be zero filled.
(?P<width>\d+)?        # The minimum width.
(?P<comma>,)?
(?P<precision>.\d+)?   # Precision
(?P<type>[bcdeEfFgGnorsxXL%])?  # The format string (Not all are supported).
""", re.X)


def ParseFormatSpec(formatstring):
    if formatstring == "[addrpad]":
        return dict(
            style="address",
            padding="0"
        )

    elif formatstring == "[addr]":
        return {"style": "address"}

    match = FORMAT_SPECIFIER_RE.match(formatstring)
    result = {}

    width = match.group("width")
    if width:
        result["width"] = int(width)

    align = match.group("align")
    if align == "<":
        result["align"] = "l"
    elif align == ">":
        result["align"] = "r"
    elif align == "^":
        result["align"] = "c"

    return result


class Formatter(string.Formatter):
    """A formatter which supports extended formating specs."""
    # This comes from http://docs.python.org/library/string.html
    # 7.1.3.1. Format Specification Mini-Language
    standard_format_specifier_re = re.compile(r"""
(?P<fill>[^{}<>=^bcdeEfFgGnLorsxX0-9])?  # The fill parameter. This can not be a
                                        # format string or it is ambiguous.
(?P<align>[<>=^])?     # The alignment.
(?P<sign>[+\- ])?      # Sign extension.
(?P<hash>\#)?          # Hash means to preceed the whole thing with 0x.
(?P<zerofill>0)?       # Should numbers be zero filled.
(?P<width>\d+)?        # The minimum width.
(?P<comma>,)?
(?P<precision>.\d+)?   # Precision
(?P<type>[bcdeEfFgGnorsxXL%])?  # The format string (Not all are supported).
""", re.X)

    def __init__(self, session=None):
        super(Formatter, self).__init__()
        self.session = session
        self._calculate_address_size()

    def _calculate_address_size(self):
        self.address_size = 14

        # Be careful to not force profile autodetection here for such a trivial
        # piece of information.
        if (self.session.HasParameter("profile") and
                self.session.profile.metadata("arch") == "I386"):
            self.address_size = 10

    def parse_extended_format(self, value, formatstring=None, header=False,
                              **options):
        """Parse the format string into the format specification.

        We support some extended forms of format string which we process
        especially here:

        [addrpad] - This is a padded address to width renderer.address_size.
        [addr] - This is a non padded address.
        [wrap:width] - This wraps a stringified version of the target in the
           cell.

        Args:
          formatstring: The formatstring we parse.
          options: An options dict. We may populate it with some options which
             are encoded in the extended format.

        Returns:
          A Cell instance.
        """
        _ = options
        extended_format = None

        # This means unlimited and uncontrolled width.
        if not formatstring:
            extended_format = "s"

        elif formatstring == "[addrpad]":
            if header:
                extended_format = "^%ss" % self.address_size
            else:
                extended_format = "#0%sx" % self.address_size

            if value == None:
                extended_format = "<%ss" % self.address_size

        elif formatstring == "[addr]":
            if header:
                extended_format = "^%ss" % self.address_size
            else:
                extended_format = ">#%sx" % self.address_size

        else:
            # Look for the wrap specifier.
            m = re.match(r"\[wrap:([^\]]+)\]", formatstring)
            if m:
                width = int(m.group(1))
                return Cell.wrap(utils.SmartUnicode(value), width)

        if extended_format is not None:
            return Cell(self.format_field(value, extended_format))

    def format_cell(self, value, formatstring="s", header=False, **options):
        """Format the value into a Cell instance.

        This also support extended formatting directives.

        Returns:
          A Cell instance.
        """
        res = self.parse_extended_format(
            value, formatstring=formatstring, header=header, **options)

        if res:
            return res

        if header:
            formatstring = formatstring.replace("#", "")
            formatstring = formatstring.replace("<", "")
            formatstring = formatstring.replace(">", "")
            formatstring = formatstring.replace("x", "s")
            if not formatstring.startswith("^"):
                formatstring = "^" + formatstring

        return Cell(self.format_field(value, formatstring=formatstring),
                    align=options.get("align", None),
                    width=options.get("width", None))

    def format_field(self, value, formatstring="", header=False, **_):
        """Format the value using the format_spec.

        The aim of this function is to remove the delegation to __format__() on
        the object. For our needs we do not want the object to be responsible
        for its own formatting since it is not aware of the renderer itself.

        A rekall.obj.BaseObject instance must support the following
        formatting operations:

        __unicode__
        __str__
        __repr__
        and may also support __int__ (for formatting in hex).
        """
        m = self.standard_format_specifier_re.match(formatstring)
        if not m:
            raise re.error("Invalid regex")

        fields = m.groupdict()

        if header:
            fields["align"] = "^"

        # Format the value according to the basic type.
        type = fields["type"] or "s"
        try:
            value = getattr(
                self, "format_type_%s" % type)(value, fields)
        except AttributeError:
            raise re.error("No formatter for type %s" % type)

        try:
            return format(value, formatstring)
        except ValueError:
            return str(value)

    def format_type_s(self, value, fields):
        try:
            # This is required to allow BaseObject to pass non unicode returns
            # from __unicode__ (e.g. NoneObject).
            result = value.__unicode__()
        except AttributeError:
            result = utils.SmartUnicode(value)

        formatstring = (u"{0:" + (fields.get("align") or "") +
                        (fields.get("width") or "") + "s}")
        return formatstring.format(result)

    def format_type_x(self, value, fields):
        _ = fields
        try:
            return int(value)
        except ValueError:
            return ""

    def format_type_d(self, value, fields):
        _ = fields
        try:
            return int(value)
        except ValueError:
            return ""

    def format_type_X(self, value, fields):
        _ = fields
        try:
            return int(value)
        except ValueError:
            return ""

    def format_type_r(self, value, fields):
        _ = fields
        return repr(value)

    def format_type_f(self, value, fields):
        _ = fields
        if isinstance(value, (float, int, long)):
            return float(value)

        return value

    def format_type_L(self, value, fields):
        """Support extended list format."""
        _ = fields
        return ", ".join([utils.SmartUnicode(x) for x in value])


class Pager(object):
    """A wrapper around a pager.

    The pager can be specified by the session. (eg.
    session.SetParameter("pager", 'less') or in an PAGER environment var.
    """
    # Default encoding is utf8
    encoding = "utf8"

    def __init__(self, session=None, term_fd=None):
        self.session = session

        # More is the least common denominator of pagers :-(. Less is better,
        # but most is best!
        self.pager_command = (session.GetParameter("pager") or
                              os.environ.get("PAGER"))

        if self.pager_command in [None, "-"]:
            raise AttributeError("Pager command must be specified")

        self.encoding = session.GetParameter("encoding", "UTF-8")
        self.fd = None
        self.paging_limit = self.session.GetParameter("paging_limit")
        self.data = ""

        # Partial results will be directed to this until we hit the
        # paging_limit, and then we send them to the real pager. This means that
        # short results do not invoke the pager, but render directly to the
        # terminal. It probably does not make sense to have term_fd as anything
        # other than sys.stdout.
        self.term_fd = term_fd or sys.stdout
        if not self.term_fd.isatty():
            raise AttributeError("Pager can only work on a tty.")

        self.colorizer = Colorizer(
            self.term_fd,
            nocolor=self.session.GetParameter("nocolors"),
        )

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        # Delete the temp file.
        try:
            if self.fd:
                self.fd.close()
                os.unlink(self.fd.name)
        except OSError:
            pass

    def GetTempFile(self):
        if self.fd is not None:
            return self.fd

        # Make a temporary filename to store output in.
        self.fd = tempfile.NamedTemporaryFile(prefix="rekall", delete=False)

        return self.fd

    def write(self, data):
        # Encode the data according to the output encoding.
        data = utils.SmartUnicode(data).encode(self.encoding, "replace")
        if sys.platform == "win32":
            data = data.replace("\n", "\r\n")

        if self.fd is not None:
            # Suppress terminal output. Output is buffered in self.fd and will
            # be sent to the pager.
            self.fd.write(data)

        # No paging limit specified - just dump to terminal.
        elif self.paging_limit is None:
            self.term_fd.write(data)
            self.term_fd.flush()

        # If there is not enough output yet, just write it to the terminal and
        # store it locally.
        elif len(self.data.splitlines()) < self.paging_limit:
            self.term_fd.write(data)
            self.term_fd.flush()
            self.data += data

        # Now create a tempfile and dump the rest of the output there.
        else:
            self.term_fd.write(
                self.colorizer.Render(
                    "Please wait while the rest is paged...",
                    foreground="YELLOW") + "\r\n")
            self.term_fd.flush()

            fd = self.GetTempFile()
            fd.write(self.data + data)

    def isatty(self):
        return self.term_fd.isatty()

    def flush(self):
        """Wait for the pager to be exited."""
        if self.fd is None:
            return

        self.fd.flush()

        try:
            args = dict(filename=self.fd.name)
            # Allow the user to interpolate the filename in a special way,
            # otherwise just append to the end of the command.
            if "%" in self.pager_command:
                pager_command = self.pager_command % args
            else:
                pager_command = self.pager_command + " %s" % self.fd.name

            # On windows the file must be closed before the subprocess
            # can open it.
            self.fd.close()

            subprocess.call(pager_command, shell=True)

        # Allow the user to break out from waiting for the command.
        except KeyboardInterrupt:
            pass

        finally:
            try:
                # This will delete the temp file.
                os.unlink(self.fd.name)
            except Exception:
                pass


class Colorizer(object):
    """An object which makes its target colorful."""

    COLORS = "BLACK RED GREEN YELLOW BLUE MAGENTA CYAN WHITE"
    #COLORS = "BLACK BLUE CYAN GREEN MAGENTA RED WHITE YELLOW"
    COLOR_MAP = dict([(x, i) for i, x in enumerate(COLORS.split())])

    terminal_capable = False

    def __init__(self, stream, nocolor=False):
        """Initialize a colorizer.

        Args:
          stream: The stream to write to.

          nocolor: If True we suppress using colors, even if the output stream
             can support them.
        """
        if stream is None:
            stream = sys.stdout

        if nocolor:
            self.terminal_capable = False
            return

        try:
            if curses and stream.isatty():
                curses.setupterm()

                self.terminal_capable = True
        except AttributeError:
            pass

    def tparm(self, capabilities, *args):
        """A simplified version of tigetstr without terminal delays."""
        for capability in capabilities:
            term_string = curses.tigetstr(capability)
            if term_string is not None:
                term_string = re.sub(r"\$\<[^>]+>", "", term_string)
                break

        try:
            return curses.tparm(term_string, *args)
        except Exception, e:
            logging.debug("Unable to set tparm: %s" % e)
            return ""

    def Render(self, target, foreground=None, background=None):
        """Decorate the string with the ansii escapes for the color."""
        if (not self.terminal_capable or
                foreground not in self.COLOR_MAP or
                foreground not in self.COLOR_MAP):
            return utils.SmartUnicode(target)

        escape_seq = ""
        if background:
            escape_seq += self.tparm(
                ["setab", "setb"], self.COLOR_MAP[background])

        if foreground:
            escape_seq += self.tparm(
                ["setaf", "setf"], self.COLOR_MAP[foreground])

        return (escape_seq + utils.SmartUnicode(target) +
                self.tparm(["sgr0"]))


class TextObjectRenderer(renderer_module.ObjectRenderer):
    """Baseclass for all TextRenderer object renderers."""

    # Fall back renderer for all objects.
    renders_type = "object"
    renderers = ["TextRenderer", "WideTextRenderer", "TestRenderer"]

    __metaclass__ = registry.MetaclassRegistry
    DEFAULT_STYLE = "full"

    @property
    def address_size(self):
        address_size = 14

        # TODO: The below will force profile autodetection. We need to do it
        # only when the profile is already autodetected.
        if self.session.profile.metadata("arch") == "I386":
            address_size = 10

        return address_size

    def format_address(self, address, **options):
        result = "%x" % address
        if options.get("padding") == "0":
            return ("0x" + "0" * max(0, self.address_size - 2 - len(result)) +
                    result)

        return " " * max(0, self.address_size - 2 - len(result)) + "0x" + result

    def render_header(self, name=None, style=StyleEnum.full, **options):
        """This should be overloaded to return the header Cell.

        Note that typically the same ObjectRenderer instance will be used to
        render all Cells in the same column.

        Args:
          name: The name of the Column.
          options: The options of the column (i.e. the dict which defines the
            column).

        Return:
          A Cell instance containing the formatted Column header.
        """
        header_cell = Cell(name, width=options.get("width", None))

        if style == "address" and header_cell.width < self.address_size:
            header_cell.rewrap(width=self.address_size, align="c")

        self.header_width = header_cell.width

        # Append a dashed line as a table header separator.
        header_cell.append_line("-" * self.header_width)

        return header_cell

    def render_full(self, target, **_):
        return Cell(unicode(target))

    def render_address(self, target, **options):
        return Cell(
            self.format_address(int(target), **options)
        )

    render_compact = render_full
    render_value = render_full

    def render_row(self, target, style=None, **options):
        """Render the target suitably.

        The default implementation calls a render_STYLE method based on the
        style keyword arg.

        Args:
          target: The object to be rendered.

          style: A value from StyleEnum, specifying how the object should
              be renderered.

          options: A dict containing rendering options. The options are created
            from the column options, overriden by the row options and finally
            the cell options.  It is ok for an instance to ignore some or all of
            the options. Some options only make sense in certain Renderer
            contexts.

        Returns:
          A Cell instance containing the rendering of target.
        """
        if not style:
            style = self.DEFAULT_STYLE

        method = getattr(self, "render_%s" % style, None)
        if not callable(method):
            raise NotImplementedError(
                "%s doesn't know how to render style %s." % (
                    type(self).__name__, style))

        cell = method(target, **options)
        return cell

    def render_hexdump(self, target, hex_width=8, **_):
        data = str(target)
        hexcell = Cell(width=hex_width * 3)
        datacell = Cell(width=hex_width)
        for _, hexdata, translated_data in utils.Hexdump(data, width=hex_width):
            hexcell.append_line(hexdata)
            datacell.append_line("".join(translated_data))

        return NestedCell(hexcell, datacell)

    def render_cow(self, *_, **__):
        """Renders a proud Swiss cow."""
        cow = (
            "                                |############          \n"
            "                                |#####  #####          \n"
            "                                |##        ##          \n"
            "              _                 |#####  #####          \n"
            "             / \\_               |############          \n"
            "            /    \\              |                      \n"
            "           /\\/\\  /\\  _          |       /;    ;\\       \n"
            "          /    \\/  \\/ \\         |   __  \\____//        \n"
            "        /\\  .-   `. \\  \\        |  /{_\\_/   `'\\____    \n"
            "       /  `-.__ ^   /\\  \\       |  \\___ (o)  (o)   }   \n"
            "      / _____________________________/          :--'   \n"
            "    ,-,'`@@@@@@@@       @@@@@@         \\_    `__\\      \n"
            "   ;:(  @@@@@@@@@        @@@             \\___(o'o)     \n"
            "   :: )  @@@@          @@@@@@        ,'@@(  `===='     \n"
            "   :: : @@@@@:          @@@@         `@@@:             \n"
            "   :: \\  @@@@@:       @@@@@@@)    (  '@@@'             \n"
            "   :; /\\      /      @@@@@@@@@\\   :@@@@@)              \n"
            "   ::/  )    {_----------------:  :~`,~~;              \n"
            "  ;; `; :   )                  :  / `; ;               \n"
            " ;;;  : :   ;                  :  ;  ; :               \n"
            " `'`  / :  :                   :  :  : :               \n"
            "     )_ \\__;                   :_ ;  \\_\\               \n"
            "     :__\\  \\                   \\  \\  :  \\              \n"
            "         `^'                    `^'  `-^-'             \n")

        cell = Cell(value=cow,
                    highlights=[(33, 45, "RED", "RED"),
                                (88, 93, "RED", "RED"),
                                (93, 95, "WHITE", "WHITE"),
                                (95, 100, "RED", "RED"),
                                (143, 145, "RED", "RED"),
                                (145, 153, "WHITE", "WHITE"),
                                (153, 155, "RED", "RED"),
                                (198, 203, "RED", "RED"),
                                (203, 205, "WHITE", "WHITE"),
                                (205, 210, "RED", "RED"),
                                (253, 265, "RED", "RED")])
        return cell


class AttributedStringRenderer(TextObjectRenderer):
    renders_type = "AttributedString"

    def render_address(self, *_, **__):
        raise NotImplementedError("This doesn't make any sense.")

    def render_full(self, target, **_):
        return Cell(value=target.value, highlights=target.highlights)

    render_compact = render_full

    def render_value(self, target, **_):
        return Cell(value=target.value)


class CellRenderer(TextObjectRenderer):
    """This renders a Cell object into a Cell object.

    i.e. it is just a passthrough object renderer for Cell objects. This is
    useful for rendering nested tables.
    """
    renders_type = "Cell"

    def render_row(self, target, **_):
        return Cell.Strip(target)


class BaseCell(object):
    """A Cell represents a single entry in a table.

    Cells always have a fixed number of characters in width and may have
    arbitrary number of characters (lines) for a height.

    The TextTable consists of an array of Cells:

    Cell Cell Cell Cell  <----- Headers.
    Cell Cell Cell Cell  <----- Table rows.

    The ObjectRenderer is responsible for turning an arbitrary object into a
    Cell object.
    """

    def __iter__(self):
        return iter(self.lines)

    def __unicode__(self):
        return u"\n".join(self.lines)


class NestedCell(BaseCell):
    def __init__(self, *cells, **kwargs):
        super(NestedCell, self).__init__()
        self.tablesep = kwargs.pop("tablesep", " ")
        if kwargs:
            raise AttributeError("Unsupported args %s" % kwargs)

        self.cells = []
        for cell in cells:
            if isinstance(cell, NestedCell):
                self.cells.extend(cell.cells)
            else:
                self.cells.append(cell)

        self.rebuild()

    def rebuild(self):
        self.height = 0
        self.width = 0
        for cell in self.cells:
            self.width += cell.width + len(self.tablesep)
            self.height = max(self.height, cell.height)

        self.width -= len(self.tablesep)

        self.lines = []
        for line_no in xrange(self.height):
            parts = []
            for cell in self.cells:
                try:
                    parts.append(cell.lines[line_no])
                except IndexError:
                    parts.append(" " * cell.width)

            self.lines.append(self.tablesep.join(parts))

    def rewrap(self, width=None, align="l"):
        """Rewraps a child cell to make up for the difference in width."""
        if not width:
            return

        if align == "l":
            child_cell = self.cells[-1]
            child_cell.rewrap(width=(width - self.width) + child_cell.width)
        elif align == "r":
            child_cell = self.cells[0]
            child_cell.rewrap(width=(width - self.width) + child_cell.width)
        elif align == "c":
            adjust = width - self.width
            self.cells[-1].rewrap(
                width=(adjust / 2) + self.cells[-1].width + adjust % 2)
            self.cells[0].rewrap(
                width=(adjust / 2) + self.cells[0].width)
        else:
            raise ValueError("Invalid alignment %s for NestedCell." % align)

        self.width = width


class Cell(BaseCell):
    _lines = None

    def __init__(self, value="", width=None, align=None, highlights=None,
                 colorizer=None, **_):
        super(Cell, self).__init__()

        self.paragraphs = value.splitlines()
        self.align = align or "l"
        self.colorizer = colorizer
        self.highlights = highlights or []

        if width:
            self.width = width
        elif self.paragraphs:
            self.width = max([len(x) for x in self.paragraphs]) or 1
        else:
            self.width = 1

    @property
    def lines(self):
        if not self._lines:
            self.rebuild()

        return self._lines

    def justify_line(self, line):
        adjust = self.width - len(line)

        if self.align == "l":
            return line + " " * adjust, 0
        elif self.align == "r":
            return " " * adjust + line, adjust
        elif self.align == "c":
            remainder = adjust % 2
            adjust /= 2
            return " " * adjust + line + " " * (adjust + remainder), adjust
        else:
            raise ValueError("Invalid cell alignment: %s." % self.align)

    def highlight_line(self, line, offset, last_highlight):
        if not self.colorizer.terminal_capable:
            return line

        if last_highlight:
            line = last_highlight + line

        limit = offset + len(line)
        adjust = 0

        for start, end, fg, bg in self.highlights:
            if offset <= start <= limit + adjust:
                escape_seq = ""
                if fg:
                    fg_id = self.colorizer.COLOR_MAP[fg]
                    escape_seq += self.colorizer.tparm(
                        ["setaf", "setf"], fg_id)

                if bg:
                    bg_id = self.colorizer.COLOR_MAP[bg]
                    escape_seq += self.colorizer.tparm(
                        ["setab", "setb"], bg_id)

                insert_at = start - offset + adjust
                line = line[:insert_at] + escape_seq + line[insert_at:]

                adjust += len(escape_seq)
                last_highlight = escape_seq

            if offset <= end <= limit + adjust:
                escape_seq = self.colorizer.tparm(["sgr0"])

                insert_at = end - offset + adjust
                line = line[:insert_at] + escape_seq + line[insert_at:]

                adjust += len(escape_seq)
                last_highlight = None

        # Always terminate active highlight at the linebreak because we don't
        # know what's being rendered to our right. We will resume
        # last_highlight on next line.
        if last_highlight:
            line += self.colorizer.tparm(["sgr0"])
        return line, last_highlight

    def rebuild(self):
        self._lines = []
        last_highlight = None
        if self.highlights:
            self.highlights.sort()
        offset = 0
        for paragraph in self.paragraphs:
            for line in textwrap.wrap(paragraph, self.width):
                line, adjust = self.justify_line(line)
                offset += adjust

                if self.colorizer and self.colorizer.terminal_capable:
                    line, last_highlight = self.highlight_line(
                        line=line, offset=offset, last_highlight=last_highlight)

                self._lines.append(line)

            offset += len(paragraph)

    def dirty(self):
        self._lines = None

    def rewrap(self, width=None, align=None):
        width = width or self.width or max(0, 0, *[len(line)
                                                   for line in self.lines])
        align = align or self.align or "l"

        if (width, align) == (self.width, self.align):
            return self

        self.width = width
        self.align = align
        self.dirty()

        return self

    def append_line(self, line):
        self.paragraphs.append(line)
        self.dirty()

    @property
    def height(self):
        """The number of chars this Cell takes in height."""
        return len(self.lines)


class TextColumn(object):
    """Implementation for text (mostly CLI) tables."""

    # The object renderer used for this column.
    object_renderer = None

    def __init__(self, table=None, renderer=None, session=None, type=None,
                 formatstring=None, **options):
        if session is None:
            raise RuntimeError("A session must be provided.")

        self.session = session
        self.table = table
        self.renderer = renderer
        self.header_width = 0

        # Arbitrary column options to be passed to ObjectRenderer() instances.
        # This allows a plugin to influence the output somewhat in different
        # output contexts.
        self.options = ParseFormatSpec(formatstring) if formatstring else {}
        # Explicit keyword arguments override formatstring.
        self.options.update(options)

        # For columns which do not explicitly set their type, we can not
        # determine the type until the first row has been written. NOTE: It is
        # not supported to change the type of a column after the first row has
        # been written.
        if type:
            self.object_renderer = self.renderer.get_object_renderer(
                type=type, target_renderer="TextRenderer", **options)

    def render_header(self):
        """Renders the cell header.

        Returns a Cell instance for this column header."""
        # If there is a customized object renderer for this column we use that.
        if self.object_renderer:
            header = self.object_renderer.render_header(**self.options)
        else:
            # Otherwise we just use the default.
            object_renderer = TextObjectRenderer(self.renderer, self.session)
            header = object_renderer.render_header(**self.options)

        header.rewrap(
            align="c",
            width=max(header.width, len(self.options.get("name", ""))))

        self.header_width = header.width

        return header

    def render_row(self, target, **options):
        """Renders the current row for the target."""
        # We merge the row options and the column options. This allows a call to
        # table_row() to override options.
        merged_opts = self.options.copy()
        merged_opts.update(options)

        if self.object_renderer is not None:
            object_renderer = self.object_renderer
        else:
            object_renderer = self.table.renderer.get_object_renderer(
                target, type=merged_opts.get("type"),
                target_renderer="TextRenderer", **options)

        result = object_renderer.render_row(target, **merged_opts)
        result.colorizer = self.renderer.colorizer

        if ("width" in self.options and not merged_opts.get("nowrap", False)
                or self.header_width > result.width):
            # Rewrap if we have an explicit width (and wrap wasn't turned off).
            # Also wrap to pad if the result is actually narrower than the
            # header, otherwise it messes up the columns to the right.
            result.rewrap(width=self.header_width,
                          align=merged_opts.get("align", "l"))

        return result

    @property
    def name(self):
        return self.options.get("name") or self.options.get("cname", "")


class TextTable(renderer_module.BaseTable):
    """A table is a collection of columns.

    This table formats all its cells using proportional text font.
    """

    column_class = TextColumn
    deferred_rows = None

    def __init__(self, **options):
        super(TextTable, self).__init__(**options)

        # Respect the renderer's table separator preference.
        self.options.setdefault("tablesep", self.renderer.tablesep)

        # Parse the column specs into column class implementations.
        self.columns = []

        for column_specs in self.column_specs:
            column = self.column_class(session=self.session, table=self,
                                       renderer=self.renderer, **column_specs)
            self.columns.append(column)

        self.sort_key_func = options.get(
            "sort_key_func",
            self._build_sort_key_function(options.get("sort")))

        if self.sort_key_func:
            self.deferred_rows = []

    def _build_sort_key_function(self, sort_cnames):
        """Builds a function that takes a row and returns keys to sort on."""
        if not sort_cnames:
            return None

        cnames_to_indices = {}
        for idx, column_spec in enumerate(self.column_specs):
            cnames_to_indices[column_spec["cname"]] = idx

        sort_indices = [cnames_to_indices[x] for x in sort_cnames]

        # Row is a tuple of (values, kwargs) - hence row[0][index].
        return lambda row: [row[0][index] for index in sort_indices]

    def write_row(self, *cells, **kwargs):
        """Writes a row of the table.

        Args:
          cells: A list of cell contents. Each cell content is a list of lines
            in the cell.
        """
        highlight = kwargs.pop("highlight", None)
        foreground, background = HIGHLIGHT_SCHEME.get(
            highlight, (None, None))

        # Iterate over all lines in the row and write it out.
        for line in NestedCell(tablesep=self.options.get("tablesep"), *cells):
            self.renderer.write(
                self.renderer.colorizer.Render(
                    line, foreground=foreground, background=background) + "\n")

    def render_header(self):
        """Returns a Cell formed by joining all the column headers."""
        # Get each column to write its own header and then we join them all up.
        return NestedCell(*[c.render_header() for c in self.columns],
                          tablesep=self.options.get("tablesep", " "))

    def get_row(self, *row, **options):
        """Format the row into a single Cell spanning all output columns.

        Args:
          *row: A list of objects to render in the same order as columns are
             defined.

        Returns:
          A single Cell object spanning the entire row.
        """
        return NestedCell(
            *[c.render_row(x, **options) for c, x in zip(self.columns, row)],
            tablesep=self.options.get("tablesep", " "))

    def render_row(self, row=None, highlight=None, annotation=False, **options):
        """Write the row to the output."""
        if annotation:
            self.renderer.format(*row)
        elif self.deferred_rows is None:
            return self.write_row(self.get_row(*row, **options),
                                  highlight=highlight)
        else:
            self.deferred_rows.append((row, options))

    def flush(self):
        if self.deferred_rows:
            self.session.report_progress("TextRenderer: sorting %(spinner)s")
            self.deferred_rows.sort(key=self.sort_key_func)

            for row, options in self.deferred_rows:
                self.write_row(self.get_row(*row, **options))


class UnicodeWrapper(object):
    """A wrapper around a file like object which guarantees writes in utf8."""

    _isatty = None

    def __init__(self, fd, encoding='utf8'):
        self.fd = fd
        self.encoding = encoding

    def write(self, data):
        data = utils.SmartUnicode(data).encode(self.encoding, "replace")
        self.fd.write(data)

    def flush(self):
        self.fd.flush()

    def isatty(self):
        if self._isatty is None:
            try:
                self._isatty = self.fd.isatty()
            except AttributeError:
                self._isatty = False

        return self._isatty


class TextRenderer(renderer_module.BaseRenderer):
    """Renderer for the command line that supports paging, colors and progress.
    """
    name = "text"

    tablesep = " "
    paging_limit = None
    progress_fd = None

    deferred_rows = None

    # Render progress with a spinner.
    spinner = r"/-\|"
    last_spin = 0
    last_message_len = 0

    table_class = TextTable

    def __init__(self, tablesep=" ", output=None, mode="a+b", fd=None,
                 **kwargs):
        super(TextRenderer, self).__init__(**kwargs)

        # Allow the user to dump all output to a file.
        self.output = output or self.session.GetParameter("output")
        if self.output:
            # We append the text output for each command. This allows the user
            # to just set it once for the session and each new command is
            # recorded in the output file.
            fd = open(self.output, mode)

        if fd == None:
            fd = self.session.fd

        if fd == None:
            try:
                fd = Pager(session=self.session)
            except AttributeError:
                fd = sys.stdout

        # Make sure that our output is unicode safe.
        self.fd = UnicodeWrapper(fd)
        self.formatter = Formatter(session=self.session)

        self.tablesep = tablesep

        # We keep the data that we produce in memory for while.
        self.data = []

        # Write progress to stdout but only if it is a tty.
        self.progress_fd = UnicodeWrapper(sys.stdout)
        if not self.progress_fd.isatty():
            self.progress_fd = None

        self.colorizer = Colorizer(
            self.fd,
            nocolor=self.session.GetParameter("nocolors"))

    def section(self, name=None, width=50):
        if name is None:
            self.write("*" * width + "\n")
        else:
            pad_len = width - len(name) - 2  # 1 space on each side.
            padding = "*" * (pad_len / 2)  # Name is centered.

            self.write("\n{0} {1} {2}\n".format(padding, name, padding))

    def format(self, formatstring, *data):
        super(TextRenderer, self).format(formatstring, *data)

        # Only clear the progress if we share the same output stream as the
        # progress.
        if self.fd is self.progress_fd:
            self.ClearProgress()

        self.write(self.formatter.format(formatstring, *data))

    def write(self, data):
        self.fd.write(data)

    def flush(self):
        super(TextRenderer, self).flush()
        self.data = []
        self.ClearProgress()
        self.fd.flush()

    def table_header(self, *args, **options):
        options["tablesep"] = self.tablesep
        super(TextRenderer, self).table_header(*args, **options)

        for line in self.table.render_header():
            if not self.table.options.get("suppress_headers"):
                self.write(line + "\n")

    def table_row(self, *args, **kwargs):
        """Outputs a single row of a table.

        Text tables support these additional kwargs:
          highlight: Highlights this raw according to the color scheme (e.g.
          important, good...)
        """
        super(TextRenderer, self).table_row(*args, **kwargs)
        self.RenderProgress(message=None)

    def _GetColumns(self):
        if curses:
            return curses.tigetnum('cols')

        return int(os.environ.get("COLUMNS", 80))

    def RenderProgress(self, message=" %(spinner)s", *args, **kwargs):
        if super(TextRenderer, self).RenderProgress(**kwargs):
            self.last_spin += 1
            if not message:
                return

            # Only expand variables when we need to.
            if "%(" in message:
                kwargs["spinner"] = self.spinner[
                    self.last_spin % len(self.spinner)]

                message = message % kwargs
            elif args:
                format_args = []
                for arg in args:
                    if callable(arg):
                        format_args.append(arg())
                    else:
                        format_args.append(arg)

                message = message % tuple(format_args)

            self.ClearProgress()

            message = " " + message + "\r"

            # Truncate the message to the terminal width to avoid wrapping.
            message = message[:self._GetColumns()]

            self.last_message_len = len(message)

            self._RenderProgress(message)

            return True

    def _RenderProgress(self, message):
        """Actually write the progress message.

        This can be overwritten by renderers to deliver the progress messages
        elsewhere.
        """
        if self.progress_fd is not None:
            self.progress_fd.write(message)
            self.progress_fd.flush()

    def ClearProgress(self):
        """Delete the last progress message."""
        if self.progress_fd is None:
            return

        # Wipe the last message.
        self.progress_fd.write("\r" + " " * self.last_message_len + "\r")
        self.progress_fd.flush()

    def open(self, directory=None, filename=None, mode="rb"):
        if filename is None and directory is None:
            raise IOError("Must provide a filename")

        if directory is None:
            directory, filename = os.path.split(filename)

        filename = utils.SmartStr(filename) or "Unknown%s" % self._object_id

        # Filter the filename for illegal chars.
        filename = re.sub(
            r"[^a-zA-Z0-9_.@{}\[\]\- ]",
            lambda x: "%" + x.group(0).encode("hex"),
            filename)

        if directory:
            filename = os.path.join(directory, "./", filename)

        return open(filename, mode)


class TestRenderer(TextRenderer):
    """A special renderer which makes parsing the output of tables easier."""
    name = "test"

    def __init__(self, **kwargs):
        super(TestRenderer, self).__init__(tablesep="||", **kwargs)


class WideTextRenderer(TextRenderer):
    """A Renderer which explodes tables into wide formatted records."""

    name = "wide"

    def __init__(self, **kwargs):
        super(WideTextRenderer, self).__init__(**kwargs)

        self.delegate_renderer = TextRenderer(**kwargs)

    def __enter__(self):
        self.delegate_renderer.__enter__()
        self.delegate_renderer.table_header(
            [("Key", "key", "[wrap:15]"),
             ("Value", "Value", "[wrap:80]")],
        )

        return super(WideTextRenderer, self).__enter__()

    def __exit__(self, exc_type, exc_value, trace):
        self.delegate_renderer.__exit__(exc_type, exc_value, trace)
        return super(WideTextRenderer, self).__exit__(
            exc_type, exc_value, trace)

    def table_header(self, *args, **options):
        options["suppress_headers"] = True
        super(WideTextRenderer, self).table_header(*args, **options)

    def table_row(self, *row, **options):
        self.section()
        values = [c.render_row(x) for c, x in zip(self.table.columns, row)]

        for c, item in zip(self.table.columns, values):
            column_name = (getattr(c.object_renderer, "name", None) or
                           c.options.get("name"))
            self.delegate_renderer.table_row(column_name, item, **options)


class TreeNodeObjectRenderer(TextObjectRenderer):
    renders_type = "TreeNode"

    def __init__(self, renderer=None, session=None, **options):
        self.max_depth = options.pop("max_depth", 10)
        child_spec = options.pop("child", None)
        if child_spec:
            child_type = child_spec.get("type", "object")
            self.child = self.ByName(child_type, renderer)(
                renderer, session=session, **child_spec)

            if not self.child:
                raise AttributeError("Child %s of TreeNode was not found." %
                                     child_type)
        else:
            self.child = None

        super(TreeNodeObjectRenderer, self).__init__(
            renderer, session=session, **options)

    def render_header(self, **options):
        if self.child:
            heading = NestedCell(self.child.render_header(**options))
        else:
            heading = super(TreeNodeObjectRenderer, self).render_header(
                **options)

        self.heading_width = heading.width
        return heading

    def render_row(self, target, depth=0, child=None, **options):
        if not child:
            child = {}

        if self.child:
            child_cell = self.child.render_row(target, **child)
        else:
            child_cell = super(TreeNodeObjectRenderer, self).render_row(
                target, **child)

        padding = Cell("." * depth)
        result = NestedCell(padding, child_cell)

        return result
