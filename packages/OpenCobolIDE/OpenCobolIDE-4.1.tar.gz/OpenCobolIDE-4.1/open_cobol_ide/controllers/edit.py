"""
Contains the EditController.

"""
import logging
from pyqode.core.api import TextHelper, ColorScheme
from pyqode.qt import QtCore, QtGui, QtWidgets
from .base import Controller
from ..compiler import FileType
from ..view.dialogs.preferences import DlgPreferences
from ..settings import Settings
from ..view.editors import CobolCodeEdit, GenericCodeEdit, \
    update_editor_settings


def _logger():
    return logging.getLogger(__name__)


class EditController(Controller):
    """
    Controls the edit view (and the edit menu).
    """
    #: the list of supported editor types
    editor_types = [CobolCodeEdit, GenericCodeEdit]

    @property
    def current_editor(self):
        """
        :rtype: pyqode.cobol.widgets.CobolCodeEdit
        """
        return self.ui.tabWidgetEditors.currentWidget()

    def __init__(self, app):
        super().__init__(app)
        self.ui.tabWidgetEditors.last_tab_closed.connect(
            self.app.view.show_home_page)
        self.ui.tabWidgetEditors.currentChanged.connect(
            self._current_changed)
        self.ui.tableWidgetOffsets.show_requested.connect(
            self.ui.dockWidgetOffsets.show)
        self.ui.actionPreferences.triggered.connect(self.edit_preferences)
        self.ui.actionPreferences.setShortcut(QtGui.QKeySequence.Preferences)
        if self.ui.actionPreferences.shortcut().toString().strip() == '':
            self.ui.actionPreferences.setShortcut('F2')
        self._setup_status_bar()
        self.ui.tabWidgetEditors.tab_closed.connect(self._on_tab_closed)
        self.ui.consoleOutput.apply_color_scheme(
            ColorScheme(Settings().color_scheme))

    def _on_tab_closed(self, tab):
        _logger().info('editor closed: %s', tab.file.path)

    def _setup_status_bar(self):
        """
        Adds some labels to the tool bar:
            - format (free or fixed)
            - encoding
            - cursor position (line:column)
        """
        # encoding
        self._lbl_encoding = QtWidgets.QLabel()
        self._lbl_encoding.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._lbl_encoding.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self._lbl_encoding.setText('UTF-8')
        # format
        self._lbl_format = QtWidgets.QLabel()
        self._lbl_format.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._lbl_format.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self._lbl_format.setText(
            'Free format' if Settings().free_format else 'Fixed format')
        # cursor position
        self._lbl_cursor = QtWidgets.QLabel()
        self._lbl_cursor.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._lbl_cursor.setAlignment(QtCore.Qt.AlignHCenter |
                                      QtCore.Qt.AlignVCenter)
        self._lbl_cursor.setText('1:1')
        self.ui.statusbar.addPermanentWidget(self._lbl_format)
        self.ui.statusbar.addPermanentWidget(self._lbl_cursor)
        self.ui.statusbar.addPermanentWidget(self._lbl_encoding)
        self.ui.statusbar.setStyleSheet(
            'QStatusBar::item { border: 0px solid black };')

    def add_editor(self, path, name, mimetype):
        """
        Adds an editor widget to the main tab widget.

        :param path: path of the file to open
        :param name: name of the tab
        :param mimetype: mimetype of the file to open.
        :return:
        """
        _logger().info('add editor: %s', path)
        editor = self._editor_from_mimetype(mimetype)
        update_editor_settings(editor)
        status = editor.file.open(path)
        index = self.ui.tabWidgetEditors.add_code_edit(editor, name)
        if status:
            self.app.cobol.display_file_type(editor)
        self.ui.tabWidgetEditors.setTabToolTip(index, path)
        editor.cursorPositionChanged.connect(self._update_status_bar_labels)
        self._update_status_bar_labels()
        return editor

    def _editor_from_mimetype(self, mimetype):
        """
        Creates an editor instance from a mimetype.
        :param mimetype: mimetype
        """
        for klass in self.editor_types:
            if mimetype in klass.mimetypes:
                if klass == CobolCodeEdit:
                    return klass(self.app.cobol.create_bt_compile(),
                                 self.app.cobol.create_bt_run())
                return klass()
        editor = self.editor_types[-1]()
        return editor

    def _current_changed(self, new_index):
        """
        Updates ui when the current editor changed.

        :param new_index: index of the new current editor.
        """
        if new_index == -1:
            # no more editors, just reset the window title
            self.main_window.setWindowTitle(
                self.app.title)
        else:
            editor = self.ui.tabWidgetEditors.currentWidget()
            self.main_window.setWindowTitle(
                '%s [%s] - %s' % (
                    editor.file.name, editor.file.path, self.app.title))
            # update tools (outline and offsets table)
            self.ui.twNavigation.set_editor(editor)
            self.ui.tableWidgetOffsets.set_editor(editor)
            # update current editor menu
            self.ui.mnuActiveEditor.clear()
            self._mnu = self.current_editor.get_context_menu()
            self.ui.mnuActiveEditor.addActions(
                self._mnu.actions())
            # update file type menu
            self.app.cobol.display_file_type(editor)
            # update cobol related actions (run/compile
            try:
                is_executable = (self.app.edit.current_editor.file_type ==
                                 FileType.EXECUTABLE)
            except AttributeError:
                self.ui.menuCobol.setEnabled(False)
                self.app.cobol.enable_compile(False)
                self.app.cobol.enable_run(False)
            else:
                self.ui.menuCobol.setEnabled(True)
                self.app.cobol.enable_compile(
                    not self.ui.consoleOutput.is_running)
                self.app.cobol.enable_run(
                    is_executable and not self.ui.consoleOutput.is_running)
            _logger().info('current editor changed: %s', editor.file.path)

    def _update_status_bar_labels(self):
        """
        Updates the status bar labels (format, encoding, cursor position).
        """
        if self.current_editor:
            l, c = TextHelper(self.current_editor).cursor_position()
            self._lbl_cursor.setText('%d:%d' % (l + 1, c + 1))
            self._lbl_encoding.setText(self.current_editor.file.encoding)
            self._lbl_format.setText(
                'Free format' if Settings().free_format else 'Fixed format')

    def edit_preferences(self):
        try:
            DlgPreferences.edit_preferences(self.main_window)
        except ValueError:
            # dialog canceled
            _logger().info('settings dialog canceled')
        else:
            _logger().info('applying settings')
            self.app.update_app_style()
            self.app.home.update_style()
            QtGui.QIcon.setThemeName(Settings().icon_theme)
            for i in range(self.ui.tabWidgetEditors.count()):
                editor = self.ui.tabWidgetEditors.widget(i)
                update_editor_settings(editor)
                self.ui.consoleOutput.apply_color_scheme(
                    ColorScheme(Settings().color_scheme))
                editor.rehighlight()
