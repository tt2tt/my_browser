from PySide6.QtWidgets import QWidget, QVBoxLayout, QToolBar, QPushButton, QLineEdit, QFileDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineDownloadRequest
from tinydb import TinyDB, Query
from datetime import datetime
import qtawesome as qta

class BrowserTab(QWidget):
    """
    ブラウザクラス
    """
    def __init__(self, main_window, url=""):
        """
        クラスの初期化
        attributes:
            main_window: メインウインドウ
            url: 検索URL
        """
        super().__init__()
        # 引数受け取り
        self.main_window = main_window
        self.url = url

        # インスタンス変数初期化
        self.history_db = ""
        self.bookmark_db = ""
        self.Query = ""
        self.web_view = ""
        self.title = ""
        self.url = ""
        self.toolbar = ""
        self.url_bar = ""
        self.bookmark_button = ""

        self.db_setting()
        self.cerate_widget()

    def db_setting(self):
        """
        DB設定
        """
        # DB設定（日本語をそのまま保存）
        self.history_db = TinyDB("./data/history.json")
        self.bookmark_db = TinyDB("./data/bookmark.json")
        self.Query = Query()
        
    def cerate_widget(self):
        """
        ウィジェット作成
        """
        browser_layout = QVBoxLayout()
        self.web_view = QWebEngineView()

        self.web_engine_setting()
        self.select_initial_page()
        self.set_page_information()
        self.cerate_tool_bar()

        browser_layout.addWidget(self.toolbar)
        browser_layout.addWidget(self.web_view)
        self.setLayout(browser_layout)

    def web_engine_setting(self):
        """
        QWebEngine設定
        """
        # PDF表示機能の有効化
        self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)

        # ダウンロード要求のシグナル接続
        self.web_view.page().profile().downloadRequested.connect(self.on_download_requested)

        # ページタイトルの変更を検知
        self.web_view.titleChanged.connect(self.on_title_changed)

    def select_initial_page(self):
        """
        初期ページ選択
        """
        if self.url == "":
            self.web_view.setUrl("https://www.google.com")
        else:
            self.web_view.setUrl(self.url)

    def set_page_information(self):
        """
        ページ情報設定
        """
        self.title = self.web_view.title()
        self.url = self.web_view.url().toString()

    def cerate_tool_bar(self):
        """
        ツールバー作成
        """
        self.toolbar = QToolBar("メインツールバー")

        # 戻るボタン
        back_button = QPushButton("")
        back_button.setIcon(qta.icon("fa5s.arrow-left", color="white"))
        back_button.clicked.connect(self.web_view.back)
        self.toolbar.addWidget(back_button)

        # 進むボタン
        forward_button = QPushButton("")
        forward_button.setIcon(qta.icon("fa5s.arrow-right", color="white"))
        forward_button.clicked.connect(self.web_view.forward)
        self.toolbar.addWidget(forward_button)

        # 再読込みボタンを作成
        reload_button = QPushButton("")
        reload_button.setIcon(qta.icon("fa5s.undo", color="white"))
        reload_button.clicked.connect(self.reload_page)
        self.toolbar.addWidget(reload_button)

        # URLバー
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("URLを入力して下さい")
        self.url_bar.returnPressed.connect(self.search_url)
        self.toolbar.addWidget(self.url_bar)

        # ブックマークボタン
        self.bookmark_button = QPushButton("")
        self.bookmark_button.setIcon(qta.icon("fa5s.star", color="white"))
        self.bookmark_button.clicked.connect(self.add_bookmark)
        self.toolbar.addWidget(self.bookmark_button)

    def search_url(self):
        """
        URL検索
        """
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.web_view.setUrl(QUrl(url))

    # 画面変更時の処理
    def on_title_changed(self):
        """
        ページ名変更時の処理
        """
        self.set_page_information()
        self.synchronization_address_bar()
        self.exclusion_google()

    def exclusion_google(self):
        """
        Googleの初期ページ等を処理から場外
        """
        if "http" not in self.title and "Google" not in self.title and "google" not in self.title:
            # メインウインドウからタブ名同期メソッドの呼び出し
            self.main_window.synchronization_tab_name(self.title[1:9])
            self.add_history()

    def add_history(self):
        """
        履歴保存
        """
        self.history_db.insert({"datetime":datetime.now().strftime("%Y年 %B %d日 (%A) %H:%M"), "title": self.title, "url": self.url})

    def judge_added_bookmark(self):
        """
        ブックマーク追加済み判定
        """
        bookmark_titles = [bookmark["title"] for bookmark in self.bookmark_db.all()]

        if self.title in bookmark_titles:
            self.bookmark_button.setIcon(qta.icon("fa5s.star", color="blue"))
            self.bookmark_button.clicked.connect(self.remove_bookmark)

    def synchronization_address_bar(self):
        """
        アドレスバー同期
        """
        self.url_bar.setText(self.url)

    def reload_page(self):
        """
        ページ再読み込み
        """
        self.web_view.reload()

    def add_bookmark(self):
        """
        ブックマーク追加
        """
        self.bookmark_db.insert({"datetime":datetime.now().strftime("%Y年 %B %d日 (%A) %H:%M"), "title": self.title, "url": self.url})
        self.bookmark_button.setIcon(qta.icon("fa5s.star", color="blue"))
        self.bookmark_button.clicked.connect(self.remove_bookmark)

    def remove_bookmark(self):
        """
        ブックマーク削除
        """
        self.bookmark_db.remove(self.Query.title == self.title)
        self.bookmark_button.setIcon(qta.icon("fa5s.star", color="white"))
        self.bookmark_button.clicked.connect(self.add_bookmark)

    def on_download_requested(self, download: QWebEngineDownloadRequest):
        """
        ファイル保存
        """
        save_path, _ = QFileDialog.getSaveFileName(self, "Save File",download.downloadDirectory() + r"/" + download.suggestedFileName())

        if save_path:
            download.setDownloadFileName(save_path)
            download.accept()
