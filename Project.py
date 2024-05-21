import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cryptography.fernet import Fernet

def encrypt_file(key, input_file, output_file):
    # Read plaintext from input file
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # Encrypt plaintext
    cipher = Fernet(key)
    ciphertext = cipher.encrypt(plaintext)

    # Write encrypted data to output file
    with open(output_file, 'wb') as f:
        f.write(ciphertext)

search_term = input("Enter Your Search Term:- ")

# Start Chrome webdriver
driver = webdriver.Chrome()
driver.get('https://www.amazon.in')

# Wait for the search box to be present
search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'twotabsearchtextbox')))
search_box.send_keys(search_term)

# Click on the search button
submit_button = driver.find_element(By.ID, 'nav-search-submit-button')
submit_button.click()

# Wait for the products to be present
products = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-component-type="s-search-result"]')))

# Create an empty list to store data
data = []

# Iterate over each product
for product in products:
    try:
        title = product.find_element(By.XPATH, './/h2/a/span').text
    except:
        title = "Not Available"
    try:
        mrp = product.find_element(By.XPATH, './/span[@class="a-price-symbol"]/following-sibling::span').text
    except:
        mrp = "Not Available"
    
    try:
        availability = "Available"
    except:
        pass
    
    try:
        url = product.find_element(By.XPATH, './/h2/a').get_attribute('href')
    except:
        url = "Not Available"

    data.append([title, mrp,  availability, url])

driver.quit()

# Create a DataFrame from the list of data
df = pd.DataFrame(data, columns=['Title', 'MRP',  'Availability', 'URL'])

# Write DataFrame to CSV file
csv_file = 'kurti.csv'
df.to_csv(csv_file, index=False)

print("CSV file created successfully.")

# Encrypt CSV file
key = Fernet.generate_key()  # Generate a random encryption key
encrypted_file = 'encrypted_kurti.csv'
encrypt_file(key, csv_file, encrypted_file)

print("File encrypted successfully.")
print("Encryption key:", key.hex())
