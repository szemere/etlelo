#!/usr/bin/python3

etlap_link = "http://www.etlelo.hu/pdf/actual.pdf"
etlap = "actual.pdf"
regiok = [
  [26, 637, 562, 779],   # Hétfő
  [26, 507, 562, 640],   # Kedd
  [26, 377, 562, 509],   # Szerda
  [26, 245, 562, 379],   # Csütörtök
  [26, 114, 562, 249],   # Péntek
  [0,   0,   50,  50 ],
  [0,   0,   50,  50 ]
]

#    [a,b,c,d]
#
#                 UR(c,d)
#    +-------+-------+
#    |   1   |   2   |
#    |-------+-------|
#    |   3   |   4   |
#    +-------+-------+
#    (a,b)

def pdf_letoltese():
  import urllib.request
  urllib.request.urlretrieve(etlap_link, etlap)


def eheti():
  import os.path, time, datetime
  etlap_ideje = os.path.getmtime(etlap)

  etlap_hete = datetime.datetime.utcfromtimestamp(etlap_ideje).isocalendar()[1]
  mai_het = datetime.datetime.now().isocalendar()[1]

  return etlap_hete == mai_het


def le_van_toltve():
  import os.path
  return os.path.isfile(etlap)


def pdf_frissitese():
  if le_van_toltve():
    if eheti():
      return
  pdf_letoltese()

def fejlec_betoltese():
  import PyPDF2
  fejlec = open("static/fejlec.pdf", "rb")
  return PyPDF2.PdfFileReader(fejlec).getPage(0)

def nap_kivagasa(regio):
  import PyPDF2

  file_in = open("actual.pdf", "rb")
  file_out = open("day.pdf", "wb")
  pdf_in = PyPDF2.PdfFileReader(file_in)
  pdf_out = PyPDF2.PdfFileWriter()

  pageObj = pdf_in.getPage(1)
  pageObj.trimBox.upperLeft  = (regio[0], regio[1])
  pageObj.trimBox.lowerRight = (regio[2], regio[3])

  pageObj.cropBox.upperLeft  = (regio[0], regio[1])
  pageObj.cropBox.lowerRight = (regio[2], regio[3])

  fejlec = fejlec_betoltese()

  pdf_out.addPage(fejlec)
  pdf_out.addPage(pageObj)
  pdf_out.write(file_out)

  file_in.close()
  file_out.close()

def mai_nap_kivagasa():
  import datetime
  nap = datetime.datetime.today().weekday()
  nap_kivagasa(regiok[nap])

def main():
  pdf_frissitese()
  mai_nap_kivagasa()

if __name__ == "__main__":
    main()
