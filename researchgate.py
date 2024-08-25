import pandas as pd
import pdfplumber
import json



with pdfplumber.open("iicai05.pdf") as pdf:
    data = []
    for page in pdf.pages[1:]:
        page_data = {
            "page_number": page.page_number,
            "text": page.extract_text()
        }
        data.append(page_data)



with open("output.json", "w") as json_file:
    json.dump(data, json_file)

dataframe1 = pd.DataFrame(data)  
#print(dataframe1)
dataframe1.to_excel('newfile.xlsx')





    

