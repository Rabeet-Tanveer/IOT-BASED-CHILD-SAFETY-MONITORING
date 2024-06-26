import requests
import time

def Capture(image_name):
    url = "http://127.0.0.1:8084/static_simple.html"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Find the image URL from the HTML content
            image_url = "http://127.0.0.1:8084/"  # Base URL of the website
            html_content = response.text
            start_index = html_content.find('<img src="') + len('<img src="')
            end_index = html_content.find('"', start_index)
            image_relative_url = html_content[start_index:end_index]
            image_url += image_relative_url

            # Download the image
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                with open(image_name, "wb") as f:
                    f.write(image_response.content)
                print("Image downloaded successfully as '" + image_name + "'")
                return True
            else:
                print("Failed to download image:", image_response.status_code)
        else:
            print("Failed to fetch HTML content:", response.status_code)
        
        return False


    except Exception as e:
        print("An error occurred:", str(e))
    
    return False
