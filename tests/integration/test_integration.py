import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from main import MainWindow
from my_package.browser_tab import BrowserTab
from my_package.table_tab import TableTab

@pytest.fixture
def main_window():
    # ...existing setup...
    window = MainWindow()
    yield window
    window.close()

def test_tab_addition(main_window):
    initial_count = main_window.tabs.count()
    main_window.select_new_tab("新しいタブ")
    assert main_window.tabs.count() == initial_count + 1

def test_history_tab(main_window):
    initial_count = main_window.tabs.count()
    main_window.select_new_tab("履歴")
    # 新しく追加されたタブがTableTabのインスタンスか確認
    widget = main_window.tabs.currentWidget()
    assert isinstance(widget, TableTab)
    assert main_window.tabs.count() == initial_count + 1

def test_bookmark_tab(main_window):
    initial_count = main_window.tabs.count()
    main_window.select_new_tab("ブックマーク")
    # 新しく追加されたタブがTableTabのインスタンスか確認
    widget = main_window.tabs.currentWidget()
    assert isinstance(widget, TableTab)
    assert main_window.tabs.count() == initial_count + 1

def test_url_navigation(main_window):
    test_url = "http://example.com"
    main_window.select_new_tab(url=test_url)
    # URL指定で追加されたタブはBrowserTabのインスタンスとなるはず
    widget = main_window.tabs.currentWidget()
    assert isinstance(widget, BrowserTab)
    # ※ 実際のURLチェックは環境依存のため、ここではインスタンス型のみ検証
