import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import requests


# Function to extract barcode data from an image
def get_barcode_data(image_path):
    img = Image.open(image_path)
    barcodes = decode(img)
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        return barcode_data  # Return the first barcode data found
    return None


# Function to get product details from the Barcode Lookup API
def get_product_details(barcode_data):
    api_key = 'API_KEY'  # Replace with your Barcode Lookup API key
    url = f'https://api.barcodelookup.com/v3/products?barcode={barcode_data}&key={api_key}'

    # Make an API request to get product details
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        if products:
            # Get product details from the first result
            product = products[0]

            # Create a dictionary to store the product details, only if they exist and have content
            product_details = {}

            # Check and add fields only if they exist and have content
            if product.get('barcode_number'):
                product_details['UPC'] = product['barcode_number']
            if product.get('category'):
                product_details['Category'] = product['category']
            if product.get('product_name'):
                product_details['Title'] = product['product_name']
            if product.get('mpn'):
                product_details['MPN'] = product['mpn']
            if product.get('model'):
                product_details['Model'] = product['model']
            if product.get('asin'):
                product_details['ASIN'] = product['asin']
            if product.get('manufacturer'):
                product_details['Manufacturer'] = product['manufacturer']
            if product.get('brand'):
                product_details['Brand'] = product['brand']
            if product.get('age_group'):
                product_details['Age Group'] = product['age_group']
            if product.get('color'):
                product_details['Color'] = product['color']
            if product.get('format'):
                product_details['Format'] = product['format']
            if product.get('multipack'):
                product_details['Multipack'] = product['multipack']
            if product.get('size'):
                product_details['Size'] = product['size']
            if product.get('dimensions'):
                product_details['Dimensions'] = product['dimensions']
            if product.get('weight'):
                product_details['Weight'] = product['weight']
            if product.get('release_date'):
                product_details['Release Date'] = product['release_date']
            if product.get('description'):
                product_details['Description'] = product['description']
            if product.get('features') and product['features']:
                product_details['Features'] = product['features']
            if product.get('images') and product['images']:
                product_details['Images'] = product['images']

            return product_details if product_details else {'Error': 'No relevant details found for this barcode'}
        else:
            return {'Error': 'No product found for this barcode'}
    else:
        return {'Error': f"API request failed with status code {response.status_code}"}


# Function to print product details
def print_product_details(product_details):
    if product_details.get('Error'):
        print(product_details['Error'])
    else:
        for key, value in product_details.items():
            # Handle lists (like Features and Images)
            if isinstance(value, list):
                print(f"{key}:")
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"{key}: {value}")


# Example usage:
# 1. Scan barcode from an image
image_path = "images/working1.png"  # Replace with the path to your image file
barcode_data = get_barcode_data(image_path)

if barcode_data:
    print(f"Barcode Data: {barcode_data}")
    product_details = get_product_details(barcode_data)
    print("Product Details:")
    print_product_details(product_details)
else:
    print("No barcode found in the image.")
