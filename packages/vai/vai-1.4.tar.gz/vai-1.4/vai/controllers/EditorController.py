import os

from vaitk import gui
from .. import Search
from .. import linting
from ..Lexer import Lexer
from .. import models
from .. import commands

class EditorController:
    def __init__(self, editor, global_state, buffer_list):
        self._editor = editor
        self._global_state = global_state
        self._buffer_list = buffer_list
        self._lexer = Lexer()

        self._buffer_list.currentBufferChanged.connect(self.registerCurrentBuffer)

    def registerCurrentBuffer(self, *args):
        self._editor.edit_area.buffer = self._buffer_list.current
        self._editor.status_bar_controller.buffer = self._buffer_list.current
        self._editor.side_ruler_controller.buffer = self._buffer_list.current
        self._editor.info_hover_box.buffer = self._buffer_list.current
        self._lexer.setModel(self._buffer_list.current.document)

    def forceQuit(self):
        for b in self._buffer_list.buffers:
            if b.document.filename() is None:
                continue

            models.EditorState.instance().setCursorPosForPath(
                    os.path.abspath(b.document.filename()),
                    b.cursor.pos)

        models.EditorState.instance().save()
        models.Configuration.save()
        gui.VApplication.vApp.exit()

    def doSave(self):
        self._doSave()
        self._doLint()

    def doSaveAs(self, filename):
        self._doSave(filename)
        self._doLint()

    def doInsertFile(self, filename):
        buffer = self._buffer_list.current

        command = commands.InsertFileCommand(buffer, filename)

        result = command.execute()
        if result.success:
            buffer.command_history.push(command)

    def tryQuit(self):
        if any([b.isModified() for b in self._buffer_list.buffers]):
            self._editor.status_bar.setMessage("Document has been modified. " +
                                               "Use :q! to quit without saving " +
                                               "or :qw to save and quit.", 3000)
        else:
            self.forceQuit()

    def searchForward(self, search_text):
        if search_text == '':
            if self._global_state.current_search is not None:
                search_text = self._global_state.current_search[0]

        if search_text != '':
            self._global_state.current_search = (search_text, Search.SearchDirection.FORWARD)
            Search.find(self._buffer_list.current, search_text, Search.SearchDirection.FORWARD)

    def searchBackward(self, search_text):
        if search_text == '':
            if self._global_state.current_search is not None:
                search_text = self._global_state.current_search[0]

        if search_text != '':
            self._global_state.current_search = (search_text, Search.SearchDirection.BACKWARD)
            Search.find(self._buffer_list.current, search_text, Search.SearchDirection.BACKWARD)

    def selectPrevBuffer(self):
        self._buffer_list.selectPrev()

    def selectNextBuffer(self):
        self._buffer_list.selectNext()

    def doSaveAndExit(self):
        self._doSave()
        self.forceQuit()

    def openFile(self, filename):
        buffer = self._buffer_list.bufferForFilename(filename)
        if buffer is not None:
            self._buffer_list.select(buffer)
            return

        current_buffer = self._buffer_list.current
        new_buffer = models.Buffer()
        status_bar = self._editor.status_bar

        try:
            new_buffer.document.open(filename)
        except FileNotFoundError:
            new_buffer.document.setFilename(filename)
            status_bar.setMessage("%s [New file]" % filename, 3000)
        except Exception as e:
            new_buffer.document.setFilename(filename)
            status_bar.setMessage("%s [Error: %s]" % (filename, str(e)), 3000)

        if current_buffer.isEmpty() and not current_buffer.isModified():
            self._buffer_list.replaceAndSelect(current_buffer, new_buffer)
        else:
            self._buffer_list.addAndSelect(new_buffer)

        recovered_cursor_pos = models.EditorState.instance().cursorPosForPath(os.path.abspath(filename))
        if recovered_cursor_pos is not None:
            new_buffer.cursor.toPos(recovered_cursor_pos)

        self._doLint()

    def createEmptyBuffer(self):
        self._buffer_list.addAndSelect(models.Buffer())

    def setMode(self, mode):
        self._global_state.edit_mode = mode

    # Private

    def _doLint(self):
        document = self._buffer_list.current.document

        linter1 = linting.PyFlakesLinter(document)
        all_info = linter1.runOnce()

        meta_info = {}

        for info in all_info:
            meta_info[info.line] = info

        document.lineMetaInfo("LinterResult").setDataForLines(meta_info)

    def _doSave(self, filename=None):
        status_bar = self._editor.status_bar
        document = self._buffer_list.current.document

        if filename is not None and len(filename) == 0:
            status_bar.setMessage("Error! Unspecified file name.", 3000)
            return

        status_bar.setMessage("Saving...")
        gui.VApplication.vApp.processEvents()

        try:
            if filename:
                document.saveAs(filename)
            else:
                document.save()
        except models.TextDocument.MissingFilenameException:
            status_bar.setMessage("Error! Cannot save unnamed file. Please specify a filename with :w filename", 3000)
            return
        except Exception as e:
            status_bar.setMessage("Error! Cannot save file. %s" % str(e), 3000)
            return
        else:
            status_bar.setMessage("Saved %s" % document.filename(), 3000)

        document.lineMetaInfo("Change").clear()

