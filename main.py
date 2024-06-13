import csv
import time
import base64
import requests  # To fetch images from URLs
from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "you_api_key"
client = OpenAI()

def get_base64_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        content_type = response.headers['Content-Type']
        if content_type in ['image/png', 'image/jpeg', 'image/gif', 'image/webp']:
            if len(response.content) < 20 * 1024 * 1024:  # Check if the image is below 20 MB
                return base64.b64encode(response.content).decode("utf-8")
            else:
                raise ValueError("Image size exceeds 20 MB limit.")
        else:
            raise ValueError("Unsupported image format.")
    else:
        raise ValueError("Failed to fetch image from URL.")

def exponential_backoff_retry(func, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            return func()
        except Exception as e:
            wait_time = 2 ** retries
            print(f"Error: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            retries += 1
    raise Exception("Max retries exceeded")

def main():
    with open(r'path_to_your_csv_with_prompts_and_image_file_locations', mode='r') as infile, open(r'path_to_output_file', mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            if len(row) < 2:
                continue  # Skip rows that don't have at least two columns
            prompt, image_url = row[:2]  # Only take the first two columns
            try:
                print(f"Processing prompt: {prompt}")
                encoded_image = get_base64_image(image_url)
                prompt_messages = [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt  # The text prompt from the CSV
                            },
                            {
                                "type": "image_url",
                                "image_url": f"data:image/jpeg;base64,{encoded_image}"  # The encoded image
                            }
                        ]
                    }
                ]
                params = {"model": "gpt-4-vision-preview", "messages": prompt_messages, "max_tokens": 4096}
                
                def api_call():
                    return client.chat.completions.create(**params)
                
                result = exponential_backoff_retry(api_call)
                response = result.choices[0].message.content
                writer.writerow([image_url, response])
                print(f"Successfully processed prompt: {prompt}")
            except ValueError as ve:
                writer.writerow([image_url, f"Error: {ve}"])
                print(f"Error processing prompt: {prompt}. Error: {ve}")
            except Exception as e:
                writer.writerow([image_url, f"Unexpected error: {e}"])
                print(f"Unexpected error processing prompt: {prompt}. Error: {e}")

if __name__ == "__main__":
    main()
