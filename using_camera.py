import cv2
from pyzbar.pyzbar import decode
import requests


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
            product = products[0]

            # Only include fields if they exist and have content
            product_details = {}

            if product.get('upc'):
                product_details['UPC'] = product['upc']
            if product.get('category'):
                product_details['Category'] = product['category']
            if product.get('title'):
                product_details['Title'] = product['title']
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
            if product.get('weights'):
                product_details['Weights'] = product['weights']
            if product.get('release_date'):
                product_details['Release Date'] = product['release_date']
            if product.get('description'):
                product_details['Description'] = product['description']
            if product.get('feature'):
                product_details['Feature'] = product['feature']
            if product.get('images') and product['images']:
                product_details['Image'] = product['images']

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
            print(f"{key}: {value}")


# Function to scan barcode from a live camera feed, avoiding repeated scans of the same barcode
def scan_barcode_from_webcam():
    cap = cv2.VideoCapture(0)  # Open webcam
    scanned_barcodes = set()  # Set to store scanned barcodes

    while True:
        ret, frame = cap.read()  # Read frame from webcam
        if not ret:
            break

        barcodes = decode(frame)  # Decode barcodes from the frame

        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')  # Extract barcode data

            if barcode_data not in scanned_barcodes:  # Check if this barcode is already scanned
                scanned_barcodes.add(barcode_data)  # Add barcode to set to prevent duplicate scanning
                x, y, w, h = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw rectangle around barcode
                cv2.putText(frame, f"Barcode: {barcode_data}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Get product details from Barcode Lookup API
                product_details = get_product_details(barcode_data)
                print("Product Details:")
                print_product_details(product_details)

        cv2.imshow("Barcode Scanner", frame)  # Display the frame

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Example usage:
scan_barcode_from_webcam()  # Call the function to start scanning from the webcam
