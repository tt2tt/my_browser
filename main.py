import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QToolBar, QPushButton, QLineEdit
from browser_tab import BrowserTab

class MainWindow(QMainWindow):
    def __init__(self, browser_tab):
        super().__init__()
        # メインウインドウ設定
        self.setWindowTitle("マイブラウザ")
        self.resize(800, 600)

        # タブウィジェット
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # ツールバーを作成
        self.toolbar = QToolBar("メインツールバー")
        self.addToolBar(self.toolbar)

        # URLバー
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("URLを入力して下さい")
        self.url_bar.returnPressed.connect(lambda: browser_tab.load_url(self.url_bar.text()))
        self.toolbar.addWidget(self.url_bar)

        # タブ追加ボタン
        self.tab_counter = 1
        add_tab_action = QPushButton("タブ追加")
        add_tab_action.clicked.connect(self.add_new_tab)
        self.toolbar.addWidget(add_tab_action)

        # 初期タブ
        self.tabs.addTab(browser_tab, "新しいタブ")

    # タブの追加
    def add_new_tab(self):
        self.tab_counter += 1
        self.browser_tab = BrowserTab()
        self.tabs.addTab(self.browser_tab, "新しいタブ")

    # タブの削除
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)


if __name__ == "__main__":
    # メインウインドウの呼び出し
    app = QApplication(sys.argv)
    browser_tab = BrowserTab()
    main_window = MainWindow(browser_tab)
    main_window.show()
    sys.exit(app.exec())
