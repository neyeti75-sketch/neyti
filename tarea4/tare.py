from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, QFontDialog, QShortcut, QListWidget
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QDateTime
import sys

class EditorRosita(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌸 Editor Rosita Avanzado 🌸")
        self.setStyleSheet("background-color:#ffd6ec;")
        self.resize(600, 500)

        self.undo_stack, self.redo_stack = [], []

        self.text = QTextEdit()
        self.text.setStyleSheet("background:#fff0f6;color:#d63384;border-radius:8px;")
        self.text.textChanged.connect(self.save_state)

        self.list_saved = QListWidget()  # Lista para guardar textos con fecha/hora

        self.btn_deshacer = self.make_btn("↩️ Deshacer", self.undo)
        self.btn_rehacer = self.make_btn("↪️ Rehacer", self.redo)
        self.btn_clear = self.make_btn("🧹 Limpiar", self.clear_text)
        self.btn_font = self.make_btn("💖 Cambiar letra", self.change_font)
        self.btn_save = self.make_btn("💾 Guardar", self.save_text)

        h = QHBoxLayout()
        for b in [self.btn_deshacer, self.btn_rehacer, self.btn_clear, self.btn_font, self.btn_save]:
            h.addWidget(b)

        layout = QVBoxLayout(self)
        layout.addLayout(h)
        layout.addWidget(self.text)
        layout.addWidget(self.list_saved)  # Agregamos la lista
        self.save_state()

        # 🌸 Atajos de teclado
        self.shortcut(QKeySequence.Undo, self.undo)
        self.shortcut(QKeySequence.Redo, self.redo)
        self.shortcut("Ctrl+L", self.clear_text)
        self.shortcut("Ctrl+S", self.save_text)
        self.shortcut("Ctrl+T", self.change_font)  # Nuevo atajo para cambiar fuente

    def make_btn(self, txt, fn):
        b = QPushButton(txt); b.clicked.connect(fn)
        b.setStyleSheet("""
            QPushButton {
                background:#ffb6d9; color:white; font-weight:bold; font-size:14px;
                border:none; border-radius:12px; padding:6px 14px;
            }
            QPushButton:hover { background:#ff8ac4; }
        """); return b

    def shortcut(self, seq, fn):
        sc = QShortcut(QKeySequence(seq), self); sc.activated.connect(fn); return sc

    def save_state(self):
        txt = self.text.toPlainText()
        if not self.undo_stack or self.undo_stack[-1] != txt:
            self.undo_stack.append(txt); self.redo_stack.clear()

    def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.text.blockSignals(True)
            self.text.setPlainText(self.undo_stack[-1])
            self.text.blockSignals(False)

    def redo(self):
        if self.redo_stack:
            s = self.redo_stack.pop(); self.undo_stack.append(s)
            self.text.blockSignals(True)
            self.text.setPlainText(s)
            self.text.blockSignals(False)

    def clear_text(self):
        self.text.clear(); self.save_state()

    def change_font(self):
        f, ok = QFontDialog.getFont()
        if ok: self.text.setFont(f)

    def save_text(self):
        contenido = self.text.toPlainText().strip()
        if contenido:
            fecha_hora = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
            self.list_saved.addItem(f"[{fecha_hora}] {contenido}")

app = QApplication(sys.argv)
w = EditorRosita()
w.show()
app.exec_()
