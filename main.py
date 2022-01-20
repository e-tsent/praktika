import datetime
import design_el
from PyQt6 import QtWidgets
import sys
from PyQt6.QtWidgets import QMessageBox


class ElinaApp(QtWidgets.QMainWindow, design_el.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.done_btn)
    
    def done_btn(self):
        fname = self.lineEdit.text()
        lname = self.lineEdit_2.text()
        mname = self.lineEdit_3.text()
        birth = self.dateEdit.text()
        
        try:
            QMessageBox.about(self, "Обратите внимание", main(fname, mname, lname, birth))
        except:
            QMessageBox.about(self, "Произошла ошибка", "Проверьте корректность данных!")


def handle(days_to_renew):
    if days_to_renew == 0:
        _ = abs(days_to_renew)

        text = f'Сегодня Вам необходимо будет обратиться в ближайший МФЦ для замены паспорта. Если вы не поменяете паспорт в течении 90 дней, на Вас будет наложен штраф.'

        return text    
    
    elif days_to_renew < 0:
        _ = abs(days_to_renew)

        text = f'Через {skl(abs(days_to_renew))} Вам необходимо будет обратиться в ближайший МФЦ для замены паспорта. Если вы не поменяете паспорт в течении 90 дней, на Вас будет наложен штраф.'

        return text
    
    elif days_to_renew > 0:
        _ = abs(days_to_renew)

        text = f'Если Вы до сих пор не поменяли паспорт, сделайте это в ближайшем МФЦ.'

        if days_to_renew - 90 > 0:
            text += ' Не забудьте оплатить штраф (просрочено 90 дней).'
        
        return text


def skl(result):    
    if result % 10 == 1 and result % 100 != 11:
        return str(result) + ' день'
    elif result % 10 in [2, 3, 4] and result % 100 not in [12, 13, 14]:
        return str(result) + ' дня'
    elif result % 10 == 0 or result % 10 in [5, 6, 7, 8, 9] or result % 100 in [11, 12, 13, 14]:
        return str(result) + ' дней'


def main(fname, mname, lname, birth):
    birth = datetime.datetime.strptime(birth, r'%d.%m.%Y')

    now = datetime.datetime.today()

    age = now - birth

    age_int = age.days // 365

    if age_int in (20, 45):
        renew_now = True
    else:
        renew_now = False

    if not renew_now:
        if age_int < 20:
            _ = 20 - age_int
        elif age_int < 45:
            _ = 45 - age_int
            
        renew_date = datetime.datetime(now.year + _, birth.month, birth.day, 0, 0, 0)

    else:
        renew_date = datetime.datetime(now.year, birth.month, birth.day, 0, 0, 0)
    
    days_to_renew = (now - renew_date).days

    return f"""
Здравствуйте, {lname} {fname} {mname}
На данный момент Вам {age_int} лет.
{handle(days_to_renew)}
"""


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ElinaApp()
    window.show()
    app.exec()