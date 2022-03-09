import PyPDF2
import urllib.request
import tempfile
import sqlite3


def fetchincidents(url):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    data = urllib.request.urlopen(
        urllib.request.Request(
            url, headers=headers)).read()
    fp = tempfile.TemporaryFile()
    fp.write(data)
    return fp


def extractincidents(fp):
    # fp = tempfile.TemporaryFile()
    # fp.write(incident_data)
    # fp.seek(0)
    pdfReader = PyPDF2.pdf.PdfFileReader(fp)
    totalPages = pdfReader.getNumPages()
    mainDataSet = []
    #   extract = []
    for i in range(totalPages):
        singlePageData = pdfReader.getPage(i).extractText()
        # print(singlePageData)
        singlePageData = singlePageData.replace(" \n", " ")
        singlePageData = singlePageData.strip().split("\n")
        # print(singlePageData)
        eachRowData = []
        if i == totalPages - 1:
            singlePageData = singlePageData[:-1]
        if i == 0:
            singlePageData = singlePageData[5:]
            singlePageData = singlePageData[:-2]
        for j in range(0, len(singlePageData), 5):
            # print(singlePageData[j+2].split(" "))
            # print(eachRowData)
            if len(singlePageData[j + 2].split(" ")) == 1 and ';' not in singlePageData[j + 2]:
                singlePageData.insert(j + 2, "Unknown")
                singlePageData.insert(j + 3, "Unknown")
            eachRowData.append(tuple(singlePageData[j:j + 5]))
         # print(eachRowData)
        extractedData = []
        for k in eachRowData:
            if len(k) == 5:
                extractedData.append(k)
        mainDataSet.extend(extractedData)
    # print(mainDataSet)
    return mainDataSet

def createdb(db='normanpd.db'):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute('''DROP TABLE IF EXISTS incidents''')
    cur.execute('''CREATE TABLE if not exists incidents (
                       incident_time TEXT,
                       incident_number TEXT,
                       incident_location TEXT,
                       nature TEXT,
                       incident_ori TEXT
                       )   ''')
    con.commit()
    con.close()
    return db

def populatedb(db, incidents):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.executemany('''INSERT INTO incidents(incident_time,incident_number,incident_location,nature,incident_ori) VALUES (?,?,?,?,?)''',incidents)
    dataSet = cur.execute('''SELECT * FROM incidents''')
    con.commit()
    con.close()
    return dataSet


def status(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute('''SELECT nature,count(nature) FROM incidents GROUP BY nature ORDER BY count(nature) DESC, nature ASC''')
    resultSet = cur.fetchall()
    #print(resultSet)
    for i in resultSet:
        print(i[0], "|", i[1])
    cur.close()
    return True
