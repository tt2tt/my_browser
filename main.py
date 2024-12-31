import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QToolBar, QPushButton, QLineEdit, QTabBar, QHBoxLayout

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

        # タブ追加ボタン
        self.tab_counter = 1
        self.add_tab_button = QPushButton("+")
        self.add_tab_button.setFixedSize(25, 25)
        self.add_tab_button.clicked.connect(self.add_new_tab)

        # タブバーをカスタマイズ
        self.tabs.tabBar().setLayout(QHBoxLayout())
        layout = self.tabs.tabBar().layout()
        layout.addStretch() 
        layout.addWidget(self.add_tab_button)
        layout.setContentsMargins(0, 0, 0, 0)

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
