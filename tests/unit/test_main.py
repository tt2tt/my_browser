import os
import sys

import pytest
from PySide6.QtWidgets import QApplication

# main.pyがあるディレクトリをパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from main import MainWindow

app = QApplication.instance() or QApplication([])

@pytest.fixture
def main_window():
    """...existing setup code..."""
    window = MainWindow()
    yield window
    window.close()

def test_window_title(main_window):
    """MainWindowのタイトルが正しく設定されていることを確認"""
    assert main_window.windowTitle() == "マイブラウザ"

def test_initial_tab_addition(main_window):
    """タブ追加処理の動作確認"""
    initial_tab_count = main_window.tabs.count()
    main_window.select_new_tab("新しいタブ")
    assert main_window.tabs.count() == initial_tab_count + 1
