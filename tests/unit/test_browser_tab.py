import os
import sys

import pytest
from PySide6.QtWidgets import QApplication, QWidget, QToolBar, QLineEdit
from PySide6.QtWebEngineWidgets import QWebEngineView
from tinydb import TinyDB

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from my_package.browser_tab import BrowserTab

app = QApplication.instance() or QApplication([])

class DummyMainWindow(QWidget):
    """ダミーのMainWindowクラス."""
    def select_new_tab(self, *args, **kwargs):
        pass

@pytest.fixture
def dummy_main_window():
    """DummyMainWindowのフィクスチャ."""
    return DummyMainWindow()

@pytest.fixture
def browser_tab(dummy_main_window):
    """BrowserTabのフィクスチャ（初期URLは空文字列によりGoogleを表示）."""
    tab = BrowserTab(dummy_main_window)
    yield tab
    # ...必要に応じたクリーンアップ...

def test_db_instances(browser_tab):
    """DBがTinyDBとして生成されていることを検証."""
    assert isinstance(browser_tab.history_db, TinyDB)
    assert isinstance(browser_tab.bookmark_db, TinyDB)

def test_web_view_exists(browser_tab):
    """web_viewがQWebEngineViewとして生成されていることを検証."""
    assert hasattr(browser_tab, "web_view")
    assert isinstance(browser_tab.web_view, QWebEngineView)

def test_default_url(browser_tab):
    """初期URLが設定されている（空の場合はGoogle）ことを検証."""
    url_str = browser_tab.web_view.url().toString()
    # 初期URLがGoogleになっているか確認
    assert "google.com" in url_str.lower()

def test_tool_bar_exists(browser_tab):
    """ツールバーが生成されていることを検証."""
    assert hasattr(browser_tab, "toolbar")
    assert isinstance(browser_tab.toolbar, QToolBar)
    # URLバーが生成されているか確認
    assert hasattr(browser_tab, "url_bar")
    assert isinstance(browser_tab.url_bar, QLineEdit)

def test_search_url(browser_tab):
    """URLバーに入力後、search_urlで正しいURLが設定されることを検証."""
    test_url = "example.com"
    # シミュレーションのため直接テキスト設定
    browser_tab.url_bar.setText(test_url)
    browser_tab.search_url()
    url_str = browser_tab.web_view.url().toString()
    # プレフィックスが追加されているか確認
    assert url_str.startswith("http://") or url_str.startswith("https://")
    assert "example.com" in url_str
