import os
import docx
import pandas as pd

# Setting the working directory
os.chdir('E:/Data Science/Ggk assignments')

doc = docx.Document('P3Input.docx')

mul_result = []
for para in doc.paragraphs:
    values = list(map(int, para.text.split(",")))
    mul_result.append(values[0] * values[1])

mul_result = pd.DataFrame(mul_result, columns=['Multiplication_result'])
mul_result.to_excel('result.xlsx')
