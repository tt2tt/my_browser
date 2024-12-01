import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QToolBar, QPushButton

from browser_tab import BrowserTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # メインウインドウ設定
        self.setWindowTitle("マイブラウザ")
        self.resize(800, 600)

        # タブウィジェット
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.setMovable(True)

        # ツールバーを作成
        self.toolbar = QToolBar("メインツールバー")
        self.addToolBar(self.toolbar)

        # 初期タブ
        self.browser_tab = BrowserTab()
        self.tabs.addTab(self.browser_tab, "新しいタブ")

        # タブ番号
        self.tab_counter = 1

        # タブ追加ボタン
        add_tab_action = QPushButton("タブ追加")
        add_tab_action.clicked.connect(self.add_new_tab)
        self.toolbar.addWidget(add_tab_action)

    def add_new_tab(self):
        self.tab_counter += 1
        self.browser_tab = BrowserTab()
        self.tabs.addTab(self.browser_tab, "新しいタブ")


if __name__ == "__main__":
    # メインウインドウの呼び出し
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
