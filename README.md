# Azure AI Search Index Export and Import

This project provides scripts for exporting documents from an Azure AI Search index to a JSON file and importing documents from a JSON file into an Azure AI Search index. It allows users to specify various options such as fields to include, filters to apply, batch sizes, and more.

## Features

### Export Features
- Export all documents or a subset based on specified criteria
- Select specific fields to include in the output
- Apply OData filter expressions to filter documents
- Display a progress bar during the export process

### Import Features
- Import documents from a JSON file into an Azure AI Search index
- Upload documents in configurable batch sizes
- Merge with existing documents or replace them
- Display a progress bar during the import process

## Requirements

- Python 3.x
- Azure SDK for Python (`azure-search-documents`, `azure-core`)
- tqdm (for progress bar)

## Installation

You can install the required packages using pip:

```
pip install azure-search-documents azure-core tqdm
```

## Usage

### Export Usage

To export documents from an index, use the following command:

```
python export.py --service <service_name> --index <index_name> --key <api_key> --output <output_file> [--select <fields>] [--filter <filter_expression>] [--top <number>] [--no-progress]
```

#### Export Parameters

- `--service`: The name of your Azure Search service
- `--index`: The name of the index to export
- `--key`: API key for authenticating to the Azure AI Search service
- `--output`: Path to the output JSON file
- `--select`: (Optional) Fields to include in the output (space-separated)
- `--filter`: (Optional) OData filter expression to filter documents
- `--top`: (Optional) Maximum number of documents to export
- `--no-progress`: (Optional) Hide the progress bar

### Import Usage

To import documents into an index, use the following command:

```
python import.py --service <service_name> --index <index_name> --key <api_key> --input <input_file> [--batch-size <size>] [--merge] [--no-progress]
```

#### Import Parameters

- `--service`: The name of your Azure Search service
- `--index`: The name of the index to import into
- `--key`: API key for authenticating to the Azure AI Search service
- `--input`: Path to the input JSON file containing documents
- `--batch-size`: (Optional) Number of documents to upload in each batch (default: 1000)
- `--merge`: (Optional) Merge with existing documents instead of replacing
- `--no-progress`: (Optional) Hide the progress bar

## Examples

### Export Example

To export all documents from an index named "my-index" and save them to "output.json":

```
python export.py --service my-search-service --index my-index --key my-api-key --output output.json
```

To export only specific fields and limit the export to 50 documents:

```
python export.py --service my-search-service --index my-index --key my-api-key --output output.json --select field1 field2 --top 50
```

### Import Example

To import documents from "documents.json" into an index named "my-index":

```
python import.py --service my-search-service --index my-index --key my-api-key --input documents.json
```

To import documents and merge them with existing ones using a smaller batch size:

```
python import.py --service my-search-service --index my-index --key my-api-key --input documents.json --batch-size 500 --merge
```