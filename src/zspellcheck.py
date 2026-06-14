# Just a wrapper file for Notepad== spellcheck stuff
# Import spellcheck
import os
import sys

from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLabel, QTextEdit, QVBoxLayout

from Finder import resolveTextWidget

sys.path.append(os.path.join(os.path.dirname(__file__), 'notepadequalequal'))

from notepadequalequal.correction import *

class SpellChecker(Spelling):
    def __init__(self, text_widget=None):
        super().__init__(text_widget)

    def z_spellcheck_selected(self, language_mode=None):
        resolved_widget = resolveTextWidget(self.text_area)
        if not resolved_widget:
            return
        cursor = resolved_widget.textCursor()
        if not cursor.hasSelection():
            return
        selected_text = cursor.selectedText()
        corrected_text = self.check_spelling(lang=language_mode, text=selected_text)
        cursor.insertText(corrected_text)

# Utilities
def approval_dialog(title, message, text):
    popup = QDialog(QApplication.activeWindow())
    popup.setWindowTitle(title)
    popup.resize(512, 342)

    layout = QVBoxLayout(popup)
    layout.addWidget(QLabel(message))

    text_widget = QTextEdit(popup)
    text_widget.setPlainText(text)
    layout.addWidget(text_widget)

    button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=popup)
    button_box.button(QDialogButtonBox.Ok).setText("Confirm")
    layout.addWidget(button_box)

    accepted_text = None

    def confirm():
        nonlocal accepted_text
        accepted_text = text_widget.toPlainText().rstrip("\n")
        popup.accept()

    button_box.accepted.connect(confirm)
    button_box.rejected.connect(popup.reject)

    if popup.exec() == QDialog.Accepted:
        return accepted_text
    return None
