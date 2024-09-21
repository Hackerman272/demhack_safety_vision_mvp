
import json
import os
from typing import List
from dotenv import load_dotenv
import openai
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def sentiment_gpt(str_content:str):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    functions = [
        {
            "name": "text_classifier",
            "description": "Determines if a given text from a web site regular, normal, or malicious.",
            "parameters": {
                "type": "object",
                "properties": {
                    "label": {
                        "type": "string",
                        "description": "The classification of the text (e.g., 'regular', 'normal', 'malicious')."
                    }
                },
                "required": ["label"]
            }
        }
    ]

    messages = [{"role": "user", "content": str_content}]

    # Create the chat completion with function calling
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        functions=functions,
        function_call={"name": "text_classifier"}
    )

    function_call = response.choices[0].message.function_call
    if function_call and function_call.name == "text_classifier":
        arguments = json.loads(function_call.arguments)
        return arguments.get("label")
    else:
        return None

if __name__ == "__main__":
    load_dotenv()
    """
    docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=chrome_options
    )

    url_to_analyze = "http://www.wicar.org/data/ms14_064_ole_notepad.html"
    # url_to_analyze = 'http://example.com'
    driver.get(url_to_analyze)
    time.sleep(5)
    page_text = driver.find_element("tag name", "body").text
    print(page_text)
    driver.quit()

    label = sentiment_gpt(page_text)
    print(f"Classification Label: {label}")
