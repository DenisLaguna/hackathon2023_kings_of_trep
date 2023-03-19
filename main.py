import sys
from PyQt5 import QtWidgets
import design
import pandas as pd


class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button_click)

    def button_click(self):
        self.listWidget.clear()
        data = pd.read_csv("burnout.csv")
        result = find_burnout(data)
        for i in range(len(result)):
            item = str(i+1) + ", " + result[i]
            self.listWidget.addItem(item)


def find_burnout(data: pd.DataFrame) -> list:
    target_words = ["fix bug", "fix bugs", "fix errors", 'fix error', "review this"]
    k = 0
    tmp = {}
    for name, values in data['Total_message'].iteritems():
        if abs(values - data['Total_message'].mean()) > data['Total_message'].std():
            k += 1
            tmp[name] = k
            k = 0
        else:
            tmp[name] = k
    cols = ['1 plus', '1 minus']
    data['sum_stats'] = data[cols].sum(axis=1)
    for name, values in data['sum_stats'].iteritems():
        if abs(values - data['sum_stats'].mean()) > data['sum_stats'].std():
            k += 1
            tmp[name] += k
            k = 0
        else:
            tmp[name] += k

    for name, values in data['Time of activity'].iteritems():
        if abs(values - data['Time of activity'].mean()) > data['Time of activity'].std():
            k += 1
            tmp[name] += k
            k = 0
        else:
            tmp[name] += k

    for name, values in data['Commit word'].iteritems():
        for val in values:
            if val.lower() in target_words:
                k += 1
                tmp[name] += k
                k = 0
            else:
                tmp[name] += k
    name_burnout = []
    for key in tmp:
        if tmp[key] >= 3:
            name_burnout.append(data.at[key, 'name'])
    return name_burnout


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
