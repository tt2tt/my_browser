from PySide6.QtWidgets import QWidget, QVBoxLayout, QToolBar, QPushButton, QLineEdit, QFileDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineDownloadRequest
from tinydb import TinyDB, Query
from datetime import datetime
import qtawesome as qta

class BrowserTab(QWidget):
    def __init__(self, main_window, url=""):
        super().__init__()
        self.layout = QVBoxLayout()
        self.web_view = QWebEngineView()

        # 別クラス
        self.main_window = main_window

        # DB設定（日本語をそのまま保存）
        self.history = TinyDB("./data/history.json")
        self.bookmark = TinyDB("./data/bookmark.json")

        # 初期ページの設定
        if url == "":
            self.web_view.setUrl("https://www.google.com")
        else:
            self.web_view.setUrl(url)

        # PDF表示機能の有効化
        self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)

        # ダウンロード要求のシグナル接続
        self.web_view.page().profile().downloadRequested.connect(self.on_download_requested)

        # ページタイトルの変更を検知
        self.web_view.titleChanged.connect(self.on_title_changed)

        # ツールバーを作成
        self.toolbar = QToolBar("メインツールバー")

        # 戻るボタン
        self.back_button = QPushButton("")
        self.back_button.setIcon(qta.icon("fa5s.arrow-left", color="white"))
        self.back_button.clicked.connect(self.web_view.back)
        self.toolbar.addWidget(self.back_button)

        # 進むボタン
        self.forward_button = QPushButton("")
        self.forward_button.setIcon(qta.icon("fa5s.arrow-right", color="white"))
        self.forward_button.clicked.connect(self.web_view.forward)
        self.toolbar.addWidget(self.forward_button)

        # 再読込みボタンを作成
        self.reload_button = QPushButton("")
        self.reload_button.setIcon(qta.icon("fa5s.undo", color="white"))
        self.reload_button.clicked.connect(self.reload_page)
        self.toolbar.addWidget(self.reload_button)

        # URLバー
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("URLを入力して下さい")
        self.url_bar.returnPressed.connect(self.load_url)
        self.toolbar.addWidget(self.url_bar)

        # ブックマークボタン
        self.bookmark_button = QPushButton("")
        self.bookmark_button.setIcon(qta.icon("fa5s.star", color="white"))
        self.bookmark_button.clicked.connect(self.add_bookmark)
        self.toolbar.addWidget(self.bookmark_button)

        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.web_view)
        self.setLayout(self.layout)

    # URLの検索
    def load_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.web_view.setUrl(QUrl(url))

    # 画面変更時の処理
    def on_title_changed(self):
        # ページのタイトルとURLを取得
        title = self.web_view.title()
        url = self.web_view.url().toString()

        # アドレスバーのURLを変更
        self.url_bar.setText(url)

        # Webページに遷移時の処理
        if "http" not in title and "Google" not in title:
            # タブ名を同期
            self.main_window.tab_name_synchronization(title[1:9])

            # 履歴の保存
            self.history.insert({"datetime":datetime.now().strftime("%Y年 %B %d日 (%A) %H:%M"), "title": title, "url": url})

    # 再読み込み
    def reload_page(self):
        self.web_view.reload()

    # ブックマーク追加
    def add_bookmark(self):
        # ページのタイトルとURLを取得
        title = self.web_view.title()
        url = self.web_view.url().toString()

        # ブックマークの保存
        self.bookmark.insert({"datetime":datetime.now().strftime("%Y年 %B %d日 (%A) %H:%M"), "title": title, "url": url})
        self.bookmark_button.setIcon(qta.icon("fa5s.star", color="blue"))

    # ダウンロード
    def on_download_requested(self, download: QWebEngineDownloadRequest):
        # 保存先、保存ファイル名の選択
        save_path, _ = QFileDialog.getSaveFileName(self, "Save File",download.downloadDirectory() + r"/" + download.suggestedFileName())

        if save_path:
            # ダウンロード先を指定して開始
            download.setDownloadFileName(save_path)
            download.accept()
