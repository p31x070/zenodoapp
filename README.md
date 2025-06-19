# Zenodo Uploader

This Python script uploads a PDF article and its metadata to Zenodo.

## Prerequisites

- Python 3.x
- Pip (Python package installer)

## Setup

1.  **Clone the repository (or download the files).**
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your Zenodo API Key:**
    - Create a `.env` file in the project root.
    - Add your Zenodo API key to the `.env` file:
      ```
      ZENODO_API_KEY=YOUR_ACTUAL_ZENODO_API_KEY
      ```
    - **Important:** If you are testing, use the Zenodo Sandbox API key and the script will use the sandbox URLs. The script currently points to the sandbox environment. To use the production Zenodo environment, you'll need to change the URLs in `zenodo_uploader.py` from `sandbox.zenodo.org` to `zenodo.org`.

5.  **Prepare your metadata file:**
    - Create a JSON file (e.g., `metadata.json`) with the article's metadata. See the example below.

## `metadata.json` Example

```json
{
  "metadata": {
    "title": "My Awesome Research Paper",
    "upload_type": "publication",
    "publication_type": "article",
    "description": "This paper presents groundbreaking research on an important topic. It includes detailed methodology, results, and discussion.",
    "creators": [
      {
        "name": "Doe, John",
        "affiliation": "University of Research",
        "orcid": "0000-0001-2345-6789"
      },
      {
        "name": "Smith, Jane",
        "affiliation": "Institute of Science"
      }
    ],
    "keywords": [
      "research",
      "science",
      "zenodo",
      "python"
    ],
    "access_right": "open"
  }
}
```
For more details on metadata fields, refer to the [Zenodo API documentation](https://developers.zenodo.org/#deposit-metadata).

## Usage

Run the script from the command line, providing the path to your PDF file and your metadata JSON file:

```bash
python zenodo_uploader.py your_article.pdf your_metadata.json
```

**Example:**

```bash
python zenodo_uploader.py ./my_paper.pdf ./metadata.json
```

The script will:
1. Create a new deposition on Zenodo.
2. Upload your PDF file.
3. Add the metadata from your JSON file.
4. Publish the deposition.

You will see status messages printed to the console for each step.

## Important Notes

- This script currently uses the Zenodo Sandbox environment (`https://sandbox.zenodo.org`) for all API calls. This is for testing purposes.
- To upload to the live Zenodo repository, you will need to:
    1. Change the API endpoint URLs in `zenodo_uploader.py` from `sandbox.zenodo.org` to `zenodo.org`.
    2. Use a production Zenodo API key in your `.env` file.
- Ensure your `metadata.json` file is correctly formatted and contains all required fields as per Zenodo's requirements.
- Publishing is a final action. Once published, a deposition cannot be deleted directly through the API, though new versions can be created.

## Testing API Key Access

A test script `test_zenodo_api.py` is provided to verify that your Zenodo API key is correctly configured in the `.env` file and allows access to the Zenodo API.

To run the test:

1.  **Ensure you have completed the Setup steps**, especially installing dependencies and configuring your `ZENODO_API_KEY` in the `.env` file.
2.  **Run the test script from your terminal:**

    ```bash
    python test_zenodo_api.py
    ```

The script will attempt to connect to the Zenodo API (sandbox by default) and retrieve a list of your depositions.

-   If successful, you will see a message indicating that the API key is working (Status Code: 200).
-   If there's an issue (e.g., incorrect API key, missing key, network problem), an error message with the corresponding status code and details will be displayed. This can help you troubleshoot your setup.

This test uses the `/api/deposit/depositions` endpoint, which requires authentication.
