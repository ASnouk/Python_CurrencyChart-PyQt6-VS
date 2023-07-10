import re
import pyodbc as dr
import pymssql as dr2

# get connection
def get_con(data_set_find = ()):  
    if data_set_find[10].lower() == "pyodbc":        
        if data_set_find[9] == True:
            con = dr.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + data_set_find[1] + "," + str(data_set_find[2]) + 
                            ";DATABASE=" + data_set_find[3] + 
                            ";Trusted_Connection=yes;")
        else:                     
            con = dr.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + data_set_find[1] + "," + str(data_set_find[2]) + 
                            ";DATABASE=" + data_set_find[3] + 
                            ";UID=" + data_set_find[4] + ";PWD=" + data_set_find[5] + ";Encrypt=" + data_set_find[11] + ";")        
    elif data_set_find[10].lower() == "pymssql":        
        con = dr2.connect(host=data_set_find[1],
                          user=data_set_find[4],
                          password=data_set_find[5],
                          port=data_set_find[2],
                          database=data_set_find[3])        
    return con

# add curs db
def add_db(data_db = [], curr_code = '', data_set_find = (), type_db = ''):
    try:
        # connect
        with get_con(data_set_find) as con:        
            cursor = con.cursor()            
            # insert data
            for mas in data_db:
                params = (mas[0].strftime("%Y-%m-%d"), curr_code, mas[1])   
                if data_set_find[10].lower() == "pyodbc":                      
                    cursor.execute("{CALL " + data_set_find[6] + "." + data_set_find[7] + "(?, ?, ?) }", params)
                elif data_set_find[10].lower() == "pymssql":                                                
                    cursor.callproc(data_set_find[6] + "." + data_set_find[7], params)
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


