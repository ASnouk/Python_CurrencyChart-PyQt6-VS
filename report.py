import os

from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# generate report
class generate_report:
    def __init__(self, data_db = [], type_db = ""):
        #  
        styles = getSampleStyleSheet() # дефолтовые стили
        # the magic is here
        styles['Normal'].fontName='DejaVuSerif'
        styles['Heading1'].fontName='DejaVuSerif' 
        pdfmetrics.registerFont(TTFont('DejaVuSerif','DejaVuSerif.ttf', 'UTF-8'))
              
        path = os.path.join(os.curdir, "report")
        report = path + "/Report_" + type_db + ".pdf"

        if not os.path.isdir(path):
                os.mkdir(path)
        
        style = styles["Heading1"]
        canv = Canvas(report, pagesize=A4)
        header = Paragraph("<bold><font size=23>Дата кращої покупки (" + type_db + ")</font></bold>", style)                

        t = Table(data_db)
        t.setStyle(TableStyle([('FONT', (0, 0), (-1, 0), 'DejaVuSerif', 16),
                               ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
        data_len = len(data_db)

        for each in range(data_len):
            if each % 2 == 0:
                bg_color = colors.whitesmoke
            else:
                bg_color = colors.lightgrey

            t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))

        aW = 540
        aH = 720

        w, h = header.wrap(aW, aH)
        header.drawOn(canv, 72, aH)
        aH = aH - h
        w, h = t.wrap(aW, aH)
        t.drawOn(canv, 72, aH-h)
        canv.save()

        # run file
        os.startfile(report)