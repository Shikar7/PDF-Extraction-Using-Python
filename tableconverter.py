import tabula
import pandas as pd

# Define the path to your PDF file
pdf_path = 'doc1.pdf'
excel_path = 'outputlastc.xlsx'

area =[232.16,53.28,781.92,478.08]



def extract_tables_from_pages(pdf_path, start_page, end_page):
    return tabula.read_pdf(pdf_path, pages=f'{start_page}-{end_page}', multiple_tables=True)


tables = tabula.read_pdf(pdf_path, pages=1,area=area, multiple_tables=True,lattice=True)  # Use 'pages="1"' for the first page only
table = tabula.read_pdf(pdf_path, pages ='all',multiple_tables = True)
lengthof = len(table)

tables_remaining_pages = tabula.read_pdf(pdf_path,pages='all',lattice= True,pandas_options={'header':None})
tables_remaining_pages[0].drop(tables_remaining_pages[0].index[:53],inplace=True)

if tables:
    # Combine all extracted tables into a single DataFrame
    df1 = pd.concat(tables,ignore_index=True, axis=0)
    df2 = pd.concat(tables_remaining_pages,ignore_index=True)

    # Print DataFrame to verify structure
    print("DataFrame created:")
    print(df1.head())
    print(df2.head())
    df2.reindex(columns=df1.columns)
    df3 = pd.concat([df1,df2],ignore_index=True)
#     # Save DataFrame to Excel
    df3.to_excel(excel_path, index=False)
    print(f"Table extracted and saved to {excel_path}")
else:
    print("No tables found in the PDF.")
