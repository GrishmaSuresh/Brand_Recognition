# Barcode Scanner with Product Lookup

This Python project uses OpenCV to scan barcodes from a webcam and the Barcode Lookup API to fetch product details.

## Features

- **Live Barcode Scanning**: Uses the webcam to scan barcodes in real-time.
- **Barcode Lookup**: Fetches product details from the Barcode Lookup API based on the scanned barcode.
- **Multiple Product Fields**: Retrieves various details like UPC, title, category, brand, and more.

## Requirements

- Python 3.x
- OpenCV
- PyZbar (for barcode decoding)
- Requests (for API calls)
- A valid API key for Barcode Lookup

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/barcode-scanner.git
   ```
2. Install dependencies:

```bash
  pip install opencv-python pyzbar requests
```
3. Replace 'API_KEY' in the get_product_details function with your Barcode Lookup API key.

## Usage
1. Ensure your webcam is connected.

2. Run the script:

```bash
python barcode_scanner.py
```

3. The webcam feed will open, and scanned barcodes will be processed to fetch and display product details.

4. Press q to quit the webcam feed.

## How It Works
- **Barcode Scanning:** The camera feed is processed using OpenCV, and the PyZbar library decodes any detected barcodes.
- **Product Lookup:** Once a barcode is scanned, it is sent to the Barcode Lookup API, which returns product details if available.
- **Avoiding Duplicate Scans:** The system tracks previously scanned barcodes to avoid processing the same barcode multiple times during a session.

## Example Output
After scanning a barcode, the following product details (if available) will be printed:

```yaml
Product Details:
UPC: 123456789012
Title: Sample Product
Category: Electronics
Brand: Example Brand
Model: XYZ123
...
```

## Troubleshooting
- **No API Key:** Make sure you've signed up for the Barcode Lookup API and replaced 'API_KEY' with your valid key.
- **Webcam Not Working:** Ensure your camera is properly connected and functioning.
- **Slow or No Response from API:** Check your internet connection or verify that the Barcode Lookup API service is operational.
  
## License
MIT License
