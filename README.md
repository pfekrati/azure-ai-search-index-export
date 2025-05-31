# Azure AI Search Index Export

This script exports documents from an Azure AI Search index to a JSON file. It allows users to specify various options such as the fields to include, filters to apply, and the maximum number of documents to export.

## Features

- Export all documents or a subset based on specified criteria.
- Select specific fields to include in the output.
- Apply OData filter expressions to filter documents.
- Display a progress bar during the export process.

## Requirements

- Python 3.x
- Azure SDK for Python (`azure-search-documents`, `azure-core`)
- tqdm (for progress bar)

## Installation

You can install the required packages using pip:

pip install azure-search-documents azure-core tqdm

## Usage

To execute the script, use the following command in your terminal:

python export.py --service <service_name> --index <index_name> --key <api_key> --output <output_file> [--select <fields>] [--filter <filter_expression>] [--top <number>] [--no-progress]

### Parameters

- `--service`: The name of your Azure Search service.
- `--index`: The name of the index to export.
- `--key`: API key for authenticating to the Azure AI Search service.
- `--output`: Path to the output JSON file.
- `--select`: (Optional) Fields to include in the output (space-separated).
- `--filter`: (Optional) OData filter expression to filter documents.
- `--top`: (Optional) Maximum number of documents to export.
- `--no-progress`: (Optional) Hide the progress bar.

## Example

To export all documents from an index named "my-index" in the Azure Search service "my-search-service" and save them to "output.json", you would run:

python export.py --service my-search-service --index my-index --key my-api-key --output output.json

To export only specific fields and limit the export to 50 documents, you could use:

python export.py --service my-search-service --index my-index --key my-api-key --output output.json --select field1 field2 --top 50

This README provides a comprehensive overview of the script's functionality and usage examples for users.