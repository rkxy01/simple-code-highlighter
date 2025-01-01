from aqt.gui_hooks import editor_did_init_buttons
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QTextEdit, QPushButton

class CodeBlockDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Insert Code Block")
        
        layout = QVBoxLayout()
        
        self.language_dropdown = QComboBox()
        self.language_dropdown.addItems(["Python", "C++", "JavaScript", "HTML", "CSS", "Java"])
        layout.addWidget(self.language_dropdown)
        
        self.code_input = QTextEdit()
        layout.addWidget(self.code_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)
        
        self.setLayout(layout)

    def get_data(self):
        return self.language_dropdown.currentText(), self.code_input.toPlainText()


def format_block(editor, view):
    dialog = CodeBlockDialog(parent=editor.parentWindow)
    if dialog.exec():
        language, code = dialog.get_data()

        escaped_code = (
            code.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\"", "&quot;")
                .replace("\n", "&#10;")
        )
        
        js_code = f"""
            document.execCommand('insertHTML', false, 
            '<pre><code class="{language}">{escaped_code}</code></pre><br>');
        """
        view.eval(js_code)


def format_inline(editor, view):
    view.eval("wrap('<code>', '</code>');")


def setup_buttons(buttons, editor):
    modes = ['inline', 'block']

    for mode in modes:
        if mode == 'block':
            button = editor.addButton(
                "",
                mode,
                lambda editor=editor: format_block(editor, editor.web),
            )
        elif mode == 'inline':
            button = editor.addButton(
                "",
                mode,
                lambda editor=editor: format_inline(editor, editor.web),
            )

        buttons.append(button)

editor_did_init_buttons.append(setup_buttons)