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

        # ツールバーを作成
        self.toolbar = QToolBar("メインツールバー")
        self.addToolBar(self.toolbar)

        # 戻るボタン
        self.back_button = QPushButton("戻る")
        self.back_button.clicked.connect(browser_tab.web_view.back)
        self.toolbar.addWidget(self.back_button)

        # 進むボタン
        self.forward_button = QPushButton("進む")
        self.forward_button.clicked.connect(browser_tab.web_view.forward)
        self.toolbar.addWidget(self.forward_button)

        # 再読込みボタンを作成
        self.reload_button = QPushButton("再読み込み")
        self.reload_button.clicked.connect(browser_tab.reload_page)
        self.toolbar.addWidget(self.reload_button)

        # URLバー
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("URLを入力して下さい")
        self.url_bar.returnPressed.connect(lambda: browser_tab.load_url(self.url_bar.text()))
        self.toolbar.addWidget(self.url_bar)

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
