# -*- coding: utf-8 -*-
"""
Contains the default indenter.
"""
import logging
from pyqode.core.api.mode import Mode
from pyqode.qt import QtGui


def _logger():
    return logging.getLogger(__name__)


class IndenterMode(Mode):
    """
    Implements classic indentation/tabulation.

    It inserts/removes tabulations (a series of spaces defined by the
    tabLength settings) at the cursor position if there is no selection,
    otherwise it fully indents/un-indents selected lines.

    To trigger an indentation/un-indentation programatically, you must emit
    :attr:`pyqode.core.api.CodeEdit.indent_requested` or
    :attr:`pyqode.core.api.CodeEdit.unindent_requested`.
    """
    def __init__(self):
        super(IndenterMode, self).__init__()

    def on_state_changed(self, state):
        if state:
            self.editor.indent_requested.connect(self.indent)
            self.editor.unindent_requested.connect(self.unindent)
        else:
            self.editor.indent_requested.disconnect(self.indent)
            self.editor.unindent_requested.disconnect(self.unindent)

    def indent_selection(self, cursor):
        """
        Indent selected text

        :param cursor: QTextCursor
        """
        doc = self.editor.document()
        tab_len = self.editor.tab_length
        cursor.beginEditBlock()
        nb_lines = len(cursor.selection().toPlainText().splitlines())
        # if nb_lines == 0:
        #     nb_lines = 1
        block = doc.findBlock(cursor.selectionStart())
        assert isinstance(block, QtGui.QTextBlock)
        i = 0
        # indent every lines
        while i < nb_lines:
            txt = block.text()
            indentation = (len(txt) - len(txt.lstrip()) -
                           self.editor.min_indent_column)
            if indentation >= 0:
                nb_space_to_add = tab_len - (indentation % tab_len)
                cursor = QtGui.QTextCursor(block)
                cursor.movePosition(cursor.StartOfLine, cursor.MoveAnchor)
                if self.editor.use_spaces_instead_of_tabs:
                    for _ in range(nb_space_to_add):
                        cursor.insertText(" ")
                else:
                    cursor.insertText('\t')
            block = block.next()
            i += 1
        cursor.endEditBlock()

    def unindent_selection(self, cursor):
        """
        Un-indents selected text
        """
        doc = self.editor.document()
        tab_len = self.editor.tab_length
        cursor.beginEditBlock()
        nb_lines = len(cursor.selection().toPlainText().splitlines())
        block = doc.findBlock(cursor.selectionStart())
        assert isinstance(block, QtGui.QTextBlock)
        i = 0
        _logger().debug('unindent selection: %d lines', nb_lines)
        while i < nb_lines:
            txt = block.text()
            _logger().debug('line to unindent: %s', txt)
            _logger().debug('self.editor.use_spaces_instead_of_tabs: %r',
                            self.editor.use_spaces_instead_of_tabs)
            if self.editor.use_spaces_instead_of_tabs:
                indentation = (len(txt) - len(txt.lstrip()) -
                               self.editor.min_indent_column)
            else:
                indentation = len(txt) - len(txt.replace('\t', ''))
            _logger().debug('unindent line %d: %d spaces (min indent=%d)',
                            i, indentation, self.editor.min_indent_column)
            if indentation > 0:
                nb_spaces_to_remove = indentation - (indentation - (
                    indentation % tab_len))
                if not nb_spaces_to_remove:
                    nb_spaces_to_remove = tab_len
                cursor = QtGui.QTextCursor(block)
                cursor.movePosition(cursor.StartOfLine, cursor.MoveAnchor)
                for _ in range(nb_spaces_to_remove):
                    cursor.deleteChar()
            block = block.next()
            i += 1
        cursor.endEditBlock()
        self.editor.setTextCursor(cursor)
        return cursor

    def indent(self):
        """
        Indents text at cursor position.
        """
        cursor = self.editor.textCursor()
        assert isinstance(cursor, QtGui.QTextCursor)
        if cursor.hasSelection():
            self.indent_selection(cursor)
        else:
            # simply insert indentation at the cursor position
            tab_len = self.editor.tab_length
            cursor.beginEditBlock()
            if self.editor.use_spaces_instead_of_tabs:
                cursor.insertText(tab_len * " ")
            else:
                cursor.insertText('\t')
            cursor.endEditBlock()

    def atBlockStart(self, cursor):
        assert isinstance(cursor, QtGui.QTextCursor)
        return cursor.columnNumber() <= self.editor.min_indent_column

    def unindent(self):
        """
        Un-indents text at cursor position.
        """
        _logger().debug('unindent')
        cursor = self.editor.textCursor()
        _logger().debug('cursor has selection %r', cursor.hasSelection())
        if cursor.hasSelection():
            self.unindent_selection(cursor)
        else:
            tab_len = self.editor.tab_length
            # count the number of spaces deletable, stop at tab len
            spaces = 0
            trav_cursor = QtGui.QTextCursor(cursor)
            while spaces < tab_len or trav_cursor.atBlockStart():
                pos = trav_cursor.position()
                trav_cursor.movePosition(cursor.Left, cursor.KeepAnchor)
                char = trav_cursor.selectedText()
                if char == " ":
                    spaces += 1
                else:
                    break
                trav_cursor.setPosition(pos - 1)
            _logger().debug('unindent by %d space' % spaces)
            if spaces:
                cursor.beginEditBlock()
                for _ in range(spaces):
                    cursor.deletePreviousChar()
                cursor.endEditBlock()
            else:
                cursor.select(cursor.LineUnderCursor)
                _logger().debug('select whole line and unindent selection')
                _logger().debug(cursor.selectedText())
                cursor = self.unindent_selection(cursor)
                cursor.clearSelection()
                _logger().debug(cursor.block().text())
