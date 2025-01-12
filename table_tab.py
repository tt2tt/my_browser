from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView, QPushButton
from tinydb import TinyDB, Query

class TableTab(QWidget):
    """
    テーブル画面クラス
    """
    def __init__(self, main_window, tab_name):
        """
        クラスの初期化
        attributes:
            main_window: メインウインドウ
            tab_name: タブ名
        """
        super().__init__()
        # 引数受け取り
        self.main_window = main_window
        self.tab_name = tab_name

        # インスタンス変数初期化
        self.selected_db = ""
        self.table_layout = ""
        self.table = ""

        self.select_db()
        self.create_widget()

    def select_db(self):
        """
        DB選択メソッド
        """
        if self.tab_name == "履歴":
            self.selected_db = TinyDB("./data/history.json")
        elif self.tab_name == "ブックマーク":
            self.selected_db = TinyDB("./data/bookmark.json")

    def create_widget(self):
        """
        ウィジェット作成
        """
        self.table_layout = QVBoxLayout()
        
        self.table_setting()
        self.create_table()
        self.add_table_cilick_trigger()

        self.table_layout.addWidget(self.table)
        self.setLayout(self.table_layout)


    def table_setting(self):
        """
        QTableWidgetの設定
        """
        # テーブルウィジェットを作成
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["日時", "ページ", "URL", "遷移", "削除"])

        # テーブルの列幅をウィンドウサイズに合わせて調整
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

    def create_table(self):
        """
        テーブルの作成
        """
        self.table.setRowCount(0)

        for i, record in enumerate(self.selected_db.all()):
            self.table.insertRow(i)

            # 各セルにデータを設定
            self.table.setItem(i, 0, QTableWidgetItem(record.get("datetime", "")))
            self.table.setItem(i, 1, QTableWidgetItem(record.get("title", "")))
            self.table.setItem(i, 2, QTableWidgetItem(record.get("url", "")))
            self.table.setItem(i, 3, QTableWidgetItem("遷移"))
            self.table.setItem(i, 4, QTableWidgetItem("削除"))

    def add_table_cilick_trigger(self):
        """
        テーブルにクリック時の処理を追加
        """
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self.on_cell_clicked)

    def on_cell_clicked(self, row, column):
        """
        テーブルクリック時の処理
        """
        if column == 3:
            # メインウインドウのタブ選択メソッドの呼び出し
            self.main_window.select_new_tab(url = self.selected_db.all()[row]["url"])
        if column == 4:
            self.delete_record(self.selected_db.all()[row].doc_id)

    def delete_record(self, id):
        """
        データの削除
        """
        self.selected_db.remove(doc_ids=[int(id)])
        self.create_table()
