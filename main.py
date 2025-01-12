import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QPushButton, QHBoxLayout
from PySide6.QtGui import QAction

from my_package.browser_tab import BrowserTab
from my_package.table_tab import TableTab
from my_package.sub_package.my_logger import MyLogger

class MainWindow(QMainWindow):
    """
    メインウインドウクラス
    """
    def __init__(self):
        """
        クラスの初期化
        """
        super().__init__()
        # メインウインドウ設定
        self.setWindowTitle("マイブラウザ")
        self.resize(800, 600)

        # インスタンス変数初期化
        self.tabs = ""
        self.tab_counter = ""

        self.cerate_widget()

    def cerate_widget(self):
        """
        ウィジェット作成
        """
        self.cerate_tab_setting()
        self.cerate_menu_bar()

    def cerate_tab_setting(self):
        """
        QTabWidgetの設定
        """
        # オブジェクト作成
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # タブ設定
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tab_counter = 0

        # タブ追加ボタンの設定
        self.tabs.tabBar().setLayout(QHBoxLayout())
        tab_layout = self.tabs.tabBar().layout()
        tab_layout.addStretch() 
        self.add_tab_button = QPushButton("+")
        self.add_tab_button.setFixedSize(25, 25)
        self.add_tab_button.clicked.connect(lambda: self.select_new_tab("新しいタブ"))
        tab_layout.addWidget(self.add_tab_button)
        tab_layout.setContentsMargins(0, 0, 0, 0)

    def cerate_menu_bar(self):
        """
        メニューバー作成
        """
        # オブジェクト作成
        menu_bar = self.menuBar()

        # 項目を追加
        history_menu = menu_bar.addMenu("履歴")

        # 処理を追加
        history_action = QAction("履歴", self)
        history_action.triggered.connect(lambda: self.select_new_tab("履歴"))
        bookmark_action = QAction("ブックマーク", self)
        bookmark_action.triggered.connect(lambda: self.select_new_tab("ブックマーク"))
        history_menu.addAction(history_action)
        history_menu.addAction(bookmark_action)

    def select_new_tab(self, tab_name = "", url = ""):
        """
        作成するタブの種類を選択
        attributes:
            tab_name: タブ名
            url: 検索URL
        """
        if tab_name == "新しいタブ":
            tab = BrowserTab(main_window)
        elif tab_name == "履歴":
            tab = TableTab(main_window, tab_name)
        elif tab_name == "ブックマーク":
            tab = TableTab(main_window, tab_name)
        elif url != "":  # 履歴やブックマークからのページ遷移
            tab = BrowserTab(main_window,url=url)

        self.add_new_tab(tab, tab_name)

    def add_new_tab(self, tab, tab_name):
        """
        タブ追加
        attributes:
            tab: タブで使用するウィジェット
            tab_name: タブ名
        """
        self.tabs.addTab(tab, tab_name)
        self.tabs.setCurrentIndex(self.tab_counter) 
        self.tab_counter += 1

    def synchronization_tab_name(self, page_name):
        """
        タブ名とページ名の同期
        attributes:
            page_name: 現在のページ名
        """
        current_index = self.tabs.currentIndex()
        self.tabs.setTabText(current_index, page_name)

    def close_tab(self, tab_index):
        """
        タブクローズ
        attributes:
            tab_index: タブ番号
        """
        if self.tabs.count() > 1:
            self.tabs.removeTab(tab_index)

def on_exit():
    """
    終了時の処理
    """
    logger.info("処理終了")

def exception_handler(exctype, value, traceback):
    """
    例外処理
    """
    logger.error("例外が発生しました", exc_info=(exctype, value, traceback))


if __name__ == "__main__":
    # ロガーの呼び出し
    logger = MyLogger(log_file="./log/app.log", when="D", interval=1, backup_count=7).get_logger()
    logger.info("処理開始")

    # 例外処理
    sys.excepthook = exception_handler

    # メインウインドウの呼び出し
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(on_exit)
    main_window = MainWindow()
    main_window.select_new_tab("新しいタブ")
    main_window.show()
    sys.exit(app.exec())
