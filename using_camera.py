import cv2
from pyzbar.pyzbar import decode
import requests
import mysql.connector
from datetime import datetime


# Function to connect to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",       # Replace with your database host
        user="root",   # Replace with your database username
        password="grishmasuresh",  # Replace with your database password
        database="brand"   # Replace with your database name
    )


# Function to insert details into the database
def insert_into_database(timestamp, brand):
    try:
        db = connect_to_database()
        cursor = db.cursor()
        query = """
        INSERT INTO barcode_details (timestamp, brand)
        VALUES (%s, %s)
        """
        cursor.execute(query, (timestamp, brand))
        db.commit()
        print("Details stored in the database successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()


# Function to get product details from the Barcode Lookup API
def get_product_details(barcode_data):
    api_key = 'cjynapuus5eq1bqobj93t55xn0f7jz'  # Replace with your Barcode Lookup API key
    url = f'https://api.barcodelookup.com/v3/products?barcode={barcode_data}&key={api_key}'

    # Make an API request to get product details
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        if products:
            product = products[0]

            # Extract required details
            brand = product.get('brand', 'Unknown')

            return {
                'Brand': brand
            }
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

                # Extract details and store them in the database
                if 'Error' not in product_details:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    brand = product_details.get('Brand', 'Unknown')
                    insert_into_database(timestamp, brand)

        cv2.imshow("Barcode Scanner", frame)  # Display the frame

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Example usage:
# Call the function to start scanning from the webcam
if __name__ == '__main__':
    scan_barcode_from_webcam()
