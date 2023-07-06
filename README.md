# Python_CurrencyChart-PyQt6-VS
Python PyQt6 project VS Code - Створення графіків курсів НБУ по роках для спостереження за тенденціями змін.

IDE - Visual Studio Code

1) Add Extensions
-> Python
-> Pylance
-> Qt for Python

У командному рядку терміналу CMD
2) Додаємо бібліотеки
-> pip install PyQt6
-> pip install pyqt6-tools
-> pip install python-dateutil
-> pip install matplotlib

3) Qt Designer
Запускаємо -> pyqt6-tools designer або окремо встановлюємо
   https://build-system.fman.io/qt-designer-download

4) Перетворення *.ui файлу у файл типу *.py
-> На файлі MainWindow.ui - права клавіша миші - Compile Qt UI File (uic)

---------------------------------------------------
Створення EXE файла
1) Ставимо pyinstaller
-> pip install pyinstaller

2) Build один EXE файл без консолі зі своєю іконкою (збірка буде у папці \dist\)
-> cd ......
-> pyinstaller -F -w -i "...\CurrencyChart\icon.ico" "...\CurrencyChart\main.py"

Перед кожною збіркою відаляємо \dist\ та \build\ та main.spec

---------------------------------------------------------------------------------
Завантаження первинних курсів
---------------------------------------------------------------------------------
- https://bank.gov.ua/control/uk/curmetal/currency/search/form/period
- Вказати період та експорт JSON