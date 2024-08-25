import tabula 
file = "iicai05.pdf"

tables = tabula.read_pdf(file,pages='all',multiple_tables=True)
print(len(tables))

tabula.convert_into("iicai05.pdf", "File1.csv", output_format="csv", pages='all')

