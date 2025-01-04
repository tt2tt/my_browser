import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QPushButton, QHBoxLayout
from PySide6.QtGui import QAction

from browser_tab import BrowserTab
from table_tab import TableTab

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
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # メニューバーを作成
        menu_bar = self.menuBar()

        # 通常のメニューを追加
        history_menu = menu_bar.addMenu("履歴")

        # メニューにアクションを追加
        history_action = QAction("履歴", self)
        history_action.triggered.connect(lambda: self.add_new_tab("履歴"))

        history_menu.addAction(history_action)

        # タブ追加ボタン
        self.tab_counter = 1
        self.add_tab_button = QPushButton("+")
        self.add_tab_button.setFixedSize(25, 25)
        self.add_tab_button.clicked.connect(lambda: self.add_new_tab("新しいタブ"))

        # タブバーをカスタマイズ
        self.tabs.tabBar().setLayout(QHBoxLayout())
        layout = self.tabs.tabBar().layout()
        layout.addStretch() 
        layout.addWidget(self.add_tab_button)
        layout.setContentsMargins(0, 0, 0, 0)

        # 初期タブ
        self.add_new_tab("新しいタブ")

    # タブの追加
    def add_new_tab(self, tab_name):
        if tab_name == "新しいタブ":
            tab = BrowserTab()
        elif tab_name == "履歴":
            tab = TableTab()
        
        self.tab_counter += 1
        self.tabs.addTab(tab, tab_name)

    # タブの削除
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)


if __name__ == "__main__":
    # メインウインドウの呼び出し
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
