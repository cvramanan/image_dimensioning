import requests
from PIL import Image
import json
from io import BytesIO



    print(data)

    #write the data to a file
    with open('data.json', 'w') as f:
        json.dump(data, f)
    

else:
    print("Failed to query the API.")
