import re
import mysql.connector as dr

# get connection
def get_con(data_set_find = ()):        
    con = dr.connect(host=data_set_find[1],
                     user=data_set_find[4],
                     password=data_set_find[5],
                     port=data_set_find[2])
    return con

# add curs db
def add_db(data_db = [], curr_code = '', data_set_find = (), type_db = ''):
    try:
        # connect
        with get_con(data_set_find) as con:        
            cursor = con.cursor()            
            # insert data
            for mas in data_db:
                params = (mas[0], curr_code, mas[1])                        
                cursor.execute("CALL " + data_set_find[6] + "." + data_set_find[7] + "(%s, %s, %s)", params)
            con.commit()
    except Exception as err:
        print(type_db + ': ' + re.sub("^\s+|\n|\r|\s+$", '', str(err)))


# load data report
def load_data_report(data_set_find = (), type_db = ''):
    data_report = []
    try:
        # connect
        with get_con(data_set_find) as con:        
            cursor = con.cursor()
            cursor.execute("select * from " + data_set_find[6] + "." + data_set_find[8])
            data = cursor.fetchall()
            #            
            data_report.append(["Дата курса", "Код валюти","Курс","Відхилення,%"])
            for mas in data:
                dat = mas[0].strftime("%d.%m.%Y")
                data_report.append([dat, mas[1], mas[2], mas[3]])                
    except Exception as err:
        print(type_db + ': ' + re.sub("^\s+|\n|\r|\s+$", '', str(err)))
    return data_report

