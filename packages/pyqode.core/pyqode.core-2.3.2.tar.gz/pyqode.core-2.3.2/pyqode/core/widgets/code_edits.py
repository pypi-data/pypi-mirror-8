"""
This module contains core code edits:

    - TextEdit: code edit specialised for plain text
    - GenericCodeEdit: generic code editor, not that smart and slow.
      Use it as a fallback and look other pyqode packages for language
      specific cod edits.

"""
import sys
from pyqode.core.api import CodeEdit, Panel, SyntaxHighlighter, \
    IndentFoldDetector


class TextCodeEdit(CodeEdit):
    """
    CodeEdit specialised for plain text.

    Especially useful for long text file such as log files because it's syntax
    highlighter does not do anything.
    """
    class TextSH(SyntaxHighlighter):
        def highlight_block(self, text, user_data):
            pass

    mimetypes = ['text/x-plain', 'text/x-log']

    def __init__(self, parent, server_script,
                 interpreter=sys.executable, args=None,
                 create_default_actions=True):
        from pyqode.core import panels
        from pyqode.core import modes
        super(TextCodeEdit, self).__init__(parent, create_default_actions)
        self.backend.start(server_script, interpreter, args)

        # append panels
        self.panels.append(panels.FoldingPanel())
        self.panels.append(panels.LineNumberPanel())
        self.panels.append(panels.SearchAndReplacePanel(),
                           Panel.Position.BOTTOM)
        self.panels.append(panels.EncodingPanel(),
                           Panel.Position.TOP)

        # append modes
        self.modes.append(modes.AutoCompleteMode())
        self.add_separator()
        self.modes.append(modes.CaseConverterMode())
        self.modes.append(modes.FileWatcherMode())
        self.modes.append(modes.CaretLineHighlighterMode())
        self.modes.append(modes.RightMarginMode())
        self.modes.append(TextCodeEdit.TextSH(self.document()))
        self.modes.append(modes.ZoomMode())
        self.modes.append(modes.OccurrencesHighlighterMode())
        self.modes.append(modes.CodeCompletionMode())
        self.modes.append(modes.AutoIndentMode())
        self.modes.append(modes.IndenterMode())
        self.modes.append(modes.SymbolMatcherMode())


class GenericCodeEdit(CodeEdit):
    """
    This generic code edit uses the PygmentSH for syntax highlighting and
    commpletion engine based on the document words. It is not very smart and
    is probably 2 times slower than a native specialised code edit.
    It is meant to be used as a fallback editor in case you're missing a
    specialised editor.
    """
    # generic
    mimetypes = []

    def __init__(self, parent, server_script,
                 interpreter=sys.executable, args=None,
                 create_default_actions=True):
        super(GenericCodeEdit, self).__init__(parent, create_default_actions)
        from pyqode.core import panels
        from pyqode.core import modes

        self.backend.start(server_script, interpreter, args)

        # append panels
        self.panels.append(panels.FoldingPanel())
        self.panels.append(panels.LineNumberPanel())
        self.panels.append(panels.SearchAndReplacePanel(),
                           Panel.Position.BOTTOM)
        self.panels.append(panels.EncodingPanel(),
                           Panel.Position.TOP)

        # append modes
        self.modes.append(modes.AutoCompleteMode())
        self.add_separator()
        self.modes.append(modes.CaseConverterMode())
        self.modes.append(modes.FileWatcherMode())
        self.modes.append(modes.CaretLineHighlighterMode())
        self.modes.append(modes.RightMarginMode())
        self.modes.append(modes.PygmentsSyntaxHighlighter(self.document()))
        self.modes.append(modes.ZoomMode())
        self.modes.append(modes.CodeCompletionMode())
        self.modes.append(modes.AutoIndentMode())
        self.modes.append(modes.IndenterMode())
        self.modes.append(modes.SymbolMatcherMode())
        self.modes.append(modes.OccurrencesHighlighterMode())
        self.modes.append(modes.SmartBackSpaceMode())
        self.modes.append(modes.ExtendedSelectionMode())

        self.syntax_highlighter.fold_detector = IndentFoldDetector()

    def setPlainText(self, txt, mime_type, encoding):
        self.syntax_highlighter.set_lexer_from_filename(self.file.path)
        super(GenericCodeEdit, self).setPlainText(txt, mime_type, encoding)
