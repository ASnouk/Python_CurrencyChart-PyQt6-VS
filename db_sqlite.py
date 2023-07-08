import re
import sqlite3 as dr

# get connection
def get_con():
    con = dr.connect("curs.db")
    return con

# add curs db
def add_db(data_db = [], curr_code = '', type_db = ''):    
    try:    
        # connect
        with get_con() as con:        
                cursor = con.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS CURS
                                (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,  
                                CURS_DATE INTEGER NOT NULL, 
                                CURR_CODE TEXT NOT NULL,
                                RATE REAL NOT NULL CHECK(RATE > 0),
                                FORC INTEGER NOT NULL CHECK(FORC > 0)
                                )
                        """)
                cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS UK_CURS ON CURS (CURS_DATE, CURR_CODE)")
                # create view
                cursor.execute("""
                        CREATE VIEW IF NOT EXISTS CURS_AVG_YEAR
                        AS
                        SELECT SUBSTR(k.CURS_DATE, 1, 4) as PART_DATE,
                                k.CURR_CODE,
                                avg(k.RATE) as AVG_RATE
                        FROM CURS k
                        GROUP BY SUBSTR(k.CURS_DATE, 1, 4), k.CURR_CODE;""")
                # create view
                cursor.execute("""
                        CREATE VIEW IF NOT EXISTS CURS_AVG
                        AS
                        SELECT f.PART_DATE,
                                f.CURR_CODE,
                                AVG(f.AVG_RATE) as AVG_RATE
                        FROM (
                        SELECT SUBSTR(k.CURS_DATE, 6,5) as PART_DATE,
                                k.CURR_CODE,
                                (k.RATE/a.AVG_RATE)*100 as AVG_RATE
                        FROM CURS k
                        INNER JOIN CURS_AVG_YEAR a ON a.PART_DATE = SUBSTR(k.CURS_DATE, 1, 4) AND a.CURR_CODE = k.CURR_CODE
                        ) f
                        GROUP BY f.PART_DATE, f.CURR_CODE
                        """)
                # create view
                cursor.execute("""
                        CREATE VIEW IF NOT EXISTS CURS_REPORT
                        AS
                        SELECT k.CURS_DATE,
                                k.CURR_CODE,
                                k.RATE,
                                a.AVG_RATE as AVG_RATE
                        FROM CURS k
                        INNER JOIN CURS_AVG a ON a.PART_DATE = SUBSTR(k.CURS_DATE, 6, 5) AND a.CURR_CODE = k.CURR_CODE
                        WHERE SUBSTR(k.CURS_DATE, 1, 4) IN (SELECT SUBSTR(MAX(date(kk.CURS_DATE)),1,4) FROM CURS kk)
                        ORDER BY 1""")
                
                # insert data
                for mas in data_db:
                        params = (mas[0].strftime("%Y-%m-%d"), curr_code, mas[1], 1)                        
                        cursor.execute("INSERT OR IGNORE INTO CURS(curs_date, curr_code, rate, forc) VALUES(?, ?, ?, ?)", params)        
                con.commit()
    except Exception as err:
        print(type_db + ': ' + re.sub("^\s+|\n|\r|\s+$", '', str(err)))


# load data report
def load_data_report(type_db = ''):
    data_report = []
    try:    
        # connect
        with get_con() as con:
                cursor = con.cursor()
                cursor.execute("select k.* from CURS_REPORT k")
                data = cursor.fetchall()
                #
                data_report.append(["Дата курса", "Код валюти","Курс","Відхилення,%"])
                for mas in data:
                        dat = mas[0][8:10] + "." + mas[0][5:7] + "." + mas[0][0:4]
                        data_report.append([dat, mas[1], mas[2], mas[3]])
    except Exception as err:
        print(type_db + ': ' + re.sub("^\s+|\n|\r|\s+$", '', str(err)))
    return data_report


