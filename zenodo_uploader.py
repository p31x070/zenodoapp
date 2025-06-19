import os
import json
import requests
from dotenv import load_dotenv

# Base URL for Zenodo API
ZENODO_API_URL = "https://sandbox.zenodo.org/api/deposit/depositions"

def load_api_key():
    """Loads the Zenodo API key from the .env file."""
    load_dotenv()
    api_key = os.getenv("ZENODO_API_KEY")
    if not api_key:
        print("Error: ZENODO_API_KEY not found in .env file.")
        return None
    return api_key

def create_deposition(api_key):
    """Creates a new deposition on Zenodo."""
    headers = {"Content-Type": "application/json"}
    params = {'access_token': api_key}
    response = requests.post(ZENODO_API_URL, params=params, json={}, headers=headers)
    if response.status_code == 201:
        data = response.json()
        deposition_id = data['id']
        bucket_url = data['links']['bucket']
        print(f"Successfully created deposition with ID: {deposition_id}")
        return deposition_id, bucket_url
    else:
        print(f"Error creating deposition: {response.status_code} - {response.text}")
        return None, None

def upload_file(api_key, bucket_url, file_path):
    """Uploads a file to the specified bucket URL."""
    params = {'access_token': api_key}
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as fp:
        response = requests.put(
            f"{bucket_url}/{file_name}",
            data=fp,
            params=params
        )
    if response.status_code == 200 or response.status_code == 201:
        print(f"Successfully uploaded file: {file_name}")
        return True
    else:
        print(f"Error uploading file {file_name}: {response.status_code} - {response.text}")
        return False

def add_metadata(api_key, deposition_id, metadata):
    """Adds metadata to the specified deposition."""
    headers = {"Content-Type": "application/json"}
    params = {'access_token': api_key}
    data = {'metadata': metadata}
    response = requests.put(
        f"{ZENODO_API_URL}/{deposition_id}",
        params=params,
        data=json.dumps(data),
        headers=headers
    )
    if response.status_code == 200:
        print(f"Successfully added metadata to deposition ID: {deposition_id}")
        return True
    else:
        print(f"Error adding metadata to deposition ID {deposition_id}: {response.status_code} - {response.text}")
        return False

def publish_deposition(api_key, deposition_id):
    """Publishes the specified deposition."""
    params = {'access_token': api_key}
    publish_url = f"{ZENODO_API_URL}/{deposition_id}/actions/publish"
    response = requests.post(publish_url, params=params)
    if response.status_code == 202:
        print(f"Successfully published deposition ID: {deposition_id}")
        return True
    else:
        print(f"Error publishing deposition ID {deposition_id}: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Upload a PDF and metadata to Zenodo.")
    parser.add_argument("pdf_file", help="Path to the PDF file to upload.")
    parser.add_argument("metadata_file", help="Path to the JSON metadata file.")
    args = parser.parse_args()

    api_key = load_api_key()
    if not api_key:
        exit(1)

    try:
        with open(args.metadata_file, 'r') as f:
            metadata = json.load(f)
    except FileNotFoundError:
        print(f"Error: Metadata file not found at {args.metadata_file}")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {args.metadata_file}")
        exit(1)

    if not os.path.exists(args.pdf_file):
        print(f"Error: PDF file not found at {args.pdf_file}")
        exit(1)

    print("Starting Zenodo upload process...")
    deposition_id, bucket_url = create_deposition(api_key)

    if deposition_id and bucket_url:
        print(f"Attempting to upload PDF: {args.pdf_file}")
        if upload_file(api_key, bucket_url, args.pdf_file):
            print(f"Attempting to add metadata from: {args.metadata_file}")
            if add_metadata(api_key, deposition_id, metadata):
                print(f"Attempting to publish deposition ID: {deposition_id}")
                if publish_deposition(api_key, deposition_id):
                    print("Zenodo upload process completed successfully!")
                else:
                    print("Failed to publish deposition.")
            else:
                print("Failed to add metadata.")
        else:
            print("Failed to upload PDF file.")
    else:
        print("Failed to create deposition. Aborting.")
