from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView, QPushButton
from tinydb import TinyDB, Query

class TableTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        # メインウインドウ
        self.main_window = main_window

        # DB設定（日本語をそのまま保存）
        self.history = TinyDB("./data/history.json")

        self.layout = QVBoxLayout()

        # テーブルウィジェットを作成
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["日時", "ページ", "URL", "遷移"])

        # テーブルの列幅をウィンドウサイズに合わせて調整
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        # テーブルを更新
        self.update_table()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def update_table(self):
        """テーブルを更新"""
        self.table.setRowCount(0)

        for i, record in enumerate(self.history.all()):
            self.table.insertRow(i)

            # 各セルにデータを設定
            self.table.setItem(i, 0, QTableWidgetItem(record.get("datetime", "")))
            self.table.setItem(i, 1, QTableWidgetItem(record.get("title", "")))
            self.table.setItem(i, 2, QTableWidgetItem(record.get("url", "")))
            self.table.setItem(i, 3, QTableWidgetItem("遷移"))
        
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self.on_cell_clicked)

    # セルクリック時の処理
    def on_cell_clicked(self, row, column):
        if column == 3:
            self.main_window.add_new_tab(url = self.history.get(doc_id=row + 1)["url"])
