import os
import sys
import json
import calendar
import webbrowser
import datetime as dt
from dateutil.relativedelta import relativedelta

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QColor, QIcon, QBrush
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget
from MainWindow_ui import Ui_MainWindow

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class Error_MessageBox_Window(QWidget):
    def __init__(self, text_error, is_exit=True):
        super().__init__()
        dialog = QMessageBox.critical(self, "Error", text_error, QMessageBox.StandardButton.Ok)
        if dialog == QMessageBox.StandardButton.Ok and is_exit:
            sys.exit()

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.subplots_adjust(left=0.05, bottom=0.12, right=0.98, top=0.98)        
        super(MplCanvas, self).__init__(fig)

##################################
# MainWindow
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # year        
        for x in range(5):
            self.year_box.addItem(format(dt.date.today().year - x, ""))
        # month 
        self.month_box.setCurrentIndex(dt.date.today().month - 1)
        # day        
        self.day_box.setCurrentIndex(dt.date.today().day - 1)

        # graf
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)  
        self.navi_toolbar = NavigationToolbar(self.canvas, self)
        self.verticalLayout_graf.addWidget(self.canvas)
        self.verticalLayout_graf.addWidget(self.navi_toolbar)
                
        self.update_plot()
        self.show()        

        # connect
        self.updateButton.clicked.connect(self.update_plot)    

        self.day_box.currentIndexChanged.connect(self.on_day_box_index_changed)
        self.month_box.currentIndexChanged.connect(self.on_month_box_index_changed)
        self.year_box.currentTextChanged.connect(self.on_year_box_value_changed)
        self.loadButton.clicked.connect(self.on_loadButton_clicked)


    # calc data
    def calc_data(self):

        self.xdata = []
        self.ydata = []
        self.data_year = int(self.year_box.currentText()) - int(self.minus_year.value())
        date_min = dt.datetime.today()
        date_max_ = dt.datetime.today()
        if self.check_day.isChecked():
            date_now = dt.datetime.strptime(self.day_box.currentText() + dt.datetime.today().strftime(".%m.%Y"), '%d.%m.%Y').date()
            date_min = date_now + dt.timedelta(days=int(self.minus_day.value()*-1))
            date_max = date_now + dt.timedelta(days=int(self.plus_day.value()))

        if self.check_month.isChecked():
            date_now = dt.datetime.strptime(dt.datetime.today().strftime("%d.") + self.month_box.currentText()[:2] + dt.datetime.today().strftime(".%Y"), '%d.%m.%Y').date()
            date_min = date_now + relativedelta(months=int(self.minus_month.value()*-1))
            date_max = date_now + relativedelta(months=int(self.plus_month.value()))

        if date_now.year > date_min.year:
            corr_year_min = -1
        else:
            corr_year_min = 0                

        if date_max.year > date_now.year:
            corr_year_max = 1
        else:
            corr_year_max = 0                

        # load data
        try:
            file_settings_ukr = 'Офіційний курс гривні щодо іноземних валют.json'
            file_settings_eng = 'Official hrivnya exchange rates.json'
            is_file_settings_ukr = True
            is_file_settings_eng = True
            if not os.path.isfile(file_settings_ukr):
                is_file_settings_ukr = False
            if not os.path.isfile(file_settings_eng):
                is_file_settings_eng = False               
            if is_file_settings_ukr == False and is_file_settings_eng == False :
                Error_MessageBox_Window(text_error="File 'Офіційний курс гривні щодо іноземних валют.json or Official hrivnya exchange rates.json' not found").show()

            # Opening JSON file
            if is_file_settings_eng: 
                file_name = file_settings_eng
                currency_code = 'Letter code'
                date_code = 'Date'
                rate_code = 'Official hrivnya exchange rates, UAH'
                forc_code = 'Unit'
            elif is_file_settings_ukr:
                file_name = file_settings_ukr
                currency_code = 'Код літерний'
                date_code = 'Дата'
                rate_code = 'Офіційний курс гривні, грн'
                forc_code = 'Кількість одиниць'

            f = open(file=file_name, mode="r", encoding="utf8")
            data = json.loads(f.read())
            # calc
            for year_n in range(self.data_year, self.data_year + int(self.minus_year.value()) + 1, 1):
                data_x = []
                data_y = []
                for data_json in data:
                    if dt.datetime.strptime(date_min.strftime("%d.%m.") + str(year_n + corr_year_min), '%d.%m.%Y').date() \
                        <= dt.datetime.strptime(data_json[date_code], '%d.%m.%Y').date() \
                        <= dt.datetime.strptime(date_max.strftime("%d.%m.") + str(year_n + corr_year_max), '%d.%m.%Y').date() \
                            and data_json[currency_code] == self.curr_box.currentText()[:3]:
                        data_x.append(data_json[date_code][:5])
                        data_y.append(data_json[rate_code]/data_json[forc_code])
                self.xdata.append(data_x)
                self.ydata.append(data_y)
            # average  
            if self.check_average.isChecked():
                ydata_temp = []
                for mas in self.ydata:                
                    if len(mas) > 0:
                        ydata_el = []
                        sum_average = sum(mas)/len(mas)
                        for el in mas:
                            ydata_el.append(1 if sum_average == 0 else el / sum_average)
                        ydata_temp.append(ydata_el)
                    else:    
                        ydata_temp.append([])
                self.ydata = ydata_temp        

            # Closing file
            f.close()
        except Exception as err:
            print(err)
        
    # update plot
    def update_plot(self):           
        self.calc_data()             
        self.canvas.axes.cla()  # Clear the canvas.
        for num, mas in enumerate(self.ydata):                        
            if len(mas) > 0:
                self.canvas.axes.plot(self.xdata[num], mas, label=self.data_year)                
                self.canvas.axes.grid(linestyle = 'dashed')                
                if self.check_dot.isChecked():
                    for a,b in zip(self.xdata[num], mas): # подписи значений
                        self.canvas.axes.text(a, b, str(b))
            self.data_year +=1
                
        self.canvas.axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                fancybox=True, shadow=True, ncol=5) 
        
        self.canvas.axes.tick_params(axis='x', labelsize=7)                
        self.canvas.draw() 
        

    #  check day month year
    def check_day_month_year(self):
        self.is_check_day_month_year = True
        m_day = self.day_box.currentIndex() + 1
        m_month = self.month_box.currentIndex() + 1
        m_year = int (self.year_box.currentText())
        if m_month in (4,6,9,11) and m_day > 30:
            Error_MessageBox_Window("Для указанного месяца указана некорректный день", is_exit=False).show()            
            self.is_check_day_month_year = False
        
        if m_month == 2:
            if calendar.isleap(m_year):
                if m_day > 29:
                    Error_MessageBox_Window("Для указанного месяца указана некорректный день", is_exit=False).show()
                    self.is_check_day_month_year = False
            else:
                if m_day > 28:
                    Error_MessageBox_Window("Для указанного месяца указана некорректный день", is_exit=False).show()                
                    self.is_check_day_month_year = False

    ######################################
    # event - day_box - currentIndexChanged
    def on_day_box_index_changed(self):
        self.check_day_month_year()

    ######################################
    # event - month_box - currentIndexChanged
    def on_month_box_index_changed(self):
        self.check_day_month_year()       

    ######################################
    # event - year_box - currentTextChanged
    def on_year_box_value_changed(self):
        self.check_day_month_year()        

   ######################################
    # event - loadButton - Clicked
    def on_loadButton_clicked(self):
        webbrowser.open("https://bank.gov.ua/control/uk/curmetal/currency/search/form/period")        


# primary block code
app = QApplication(sys.argv)
window = MainWindow()
window.setWindowIcon(QIcon("icon.ico"))
window.show()
sys.exit(app.exec())