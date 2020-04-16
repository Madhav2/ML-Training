import pandas as pd
import os
import requests

os.chdir('E:/Data Science/Ggk assignments')

# Creating a csv file 
#num1 = [21, 25, 56, 87, 74]
#num2 = [58, 69, 2, 41, 75]
#data = pd.DataFrame(list(zip(num1, num2)), columns=['num1', 'num2'])
#data.to_csv('data.csv', index=False)

data = pd.read_csv('data.csv')

# GET request
mul_results = []
for i in range(len(data)):
    params = {'num1' : data.num1[i],
              'num2' : data.num2[i]}
    response = requests.get('http://127.0.0.1:5000/add', params=params)
    if (response.status_code == 200):
        mul_results.append(int(response.text))
    else:
        mul_results.append(None)
        print(response.status_code)
result = pd.DataFrame(mul_results, columns=['add_result'])
result.to_csv('get_add_result.csv', index=False)

# POST request
response = requests.post('http://127.0.0.1:5000/add', data=data.to_json())
if (response.status_code == 200):
    result = pd.DataFrame(response.json())
    result.to_csv('post_add_result.csv', index=False)
else:
    print(response.status_code)    
