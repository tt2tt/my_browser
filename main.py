# 標準ライブラリ
import os
import sys

# 外部ライブラリ
import PySide6
from PySide6.QtWidgets import QApplication,QWidget,QVBoxLayout,QMainWindow,QLineEdit,QPushButton,QHBoxLayout,QTabWidget
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings


# ブラウザ
class Browser(QMainWindow):
    def __init__(self,url="https://www.google.com"):
        # 親クラスの初期化
        super().__init__()
        self.widget = QWidget(self)

        # Webページの読み込み
        self.webview = QWebEngineView()

        # PDFの表示
        self.webview.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.webview.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        
        # 初期ページの設定
        self.webview.load(QUrl(url))
        self.webview.urlChanged.connect(self.url_changed)

        # ナビゲーション部分
        self.add_tab = QPushButton("タブ追加")
        self.back_button = QPushButton("<")
        self.back_button.clicked.connect(self.webview.back)
        self.forward_button = QPushButton(">")
        self.forward_button.clicked.connect(self.webview.forward)
        self.refresh_button = QPushButton("再読み込み")
        self.refresh_button.clicked.connect(self.webview.reload)

        # アドレスバー部分
        self.url_text = QLineEdit()
        self.search_button = QPushButton("検索")
        self.search_button.clicked.connect(self.url_set)

        # トップレイアウトの作成
        self.toplayout = QHBoxLayout()
        self.toplayout.addWidget(self.url_text)
        self.toplayout.addWidget(self.search_button)
        self.toplayout.addWidget(self.back_button)
        self.toplayout.addWidget(self.forward_button)
        self.toplayout.addWidget(self.refresh_button)
        self.toplayout.addWidget(self.add_tab)
        self.add_tab.clicked.connect(window.add_new_tab)

        # レイアウトの作成
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.toplayout)
        self.layout.addWidget(self.webview)

        # メインレイアウトの指定
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    # アドレスバーのURL変更
    def url_changed(self, url):
        self.url_text.setText(url.toString())

    # 検索の実行
    def url_set(self):
        self.webview.setUrl(QUrl(self.url_text.text()))


# メインウインドウ
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ウインドウタイトル設定
        self.setWindowTitle("My Browser")

        # タブウィジェットの作成
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # メインウィンドウにタブウィジェットを配置
        self.setCentralWidget(self.tabs)

    # タブの追加
    def add_new_tab(self):
        browser_tab = Browser()
        index = self.tabs.addTab(browser_tab, "New Tab")
        self.tabs.setCurrentIndex(index)
        print(self.tabs.count())

    # タブの削除
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)


# メイン処理
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.add_new_tab()
    window.show()
    sys.exit(app.exec())
