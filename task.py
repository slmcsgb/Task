import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.concordia.ca/academics/graduate.html"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully connected to the website.")
else:
    print(f"Failed to connect to the website. Status code: {response.status_code}")
    exit()

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')


# Initialize a list to store program data
program_data = []

# Find all elements with class 'section-title alphabar-title'
program_elements = soup.find_all('div', class_='section-title alphabar-title')

# Loop through each program element
for element in program_elements:
    title_tag = element.find('a')  # Find the <a> tag within the element
    if title_tag:
        title_text = title_tag.text.strip()  # Extract the title text
        program_url = title_tag.get('href')  # Extract the URL

        # Convert relative URL to absolute URL
        if program_url:
            full_url = urljoin(url, program_url)
            program_data.append((title_text, full_url))
        else:
            program_data.append((title_text, "No URL available"))

# Print the extracted program data (for debugging)
if program_data:
    for program in program_data:
        print(f"Title: {program[0]}, URL: {program[1]}")
else:
    print("No program data found.")

# Construct HTML table with proper structure and formatting
html_table = """
<table border='1'>
    <thead>
        <tr>
            <th>Title</th>
            <th>URL</th>
        </tr>
    </thead>
    <tbody>
"""

# Populate HTML table with program data
for program in program_data:
    html_table += f"""
        <tr>
            <td>{program[0]}</td>
            <td><a href="{program[1]}">{program[1]}</a></td>
        </tr>
    """

html_table += """
    </tbody>
</table>
"""

# Print HTML table with preserved formatting
print("<pre>{}</pre>".format(html_table))

# Define the file path for saving the HTML file in the same directory as the Python script
file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "index.html")

# Write the HTML content to the file
try:
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(html_table)
    print("HTML file saved in the same folder as the Python script.")
except Exception as e:
    print(f"Failed to save HTML file. Error: {e}")