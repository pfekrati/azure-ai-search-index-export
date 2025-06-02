from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import json
import os
import argparse
import sys
from tqdm import tqdm

# filepath: c:\Users\pfekr\source\repos\azure-ai-search-index-export\import.py

def import_json_to_search_index(
    search_service_name,
    index_name,
    api_key,
    input_file,
    batch_size=1000,
    show_progress=True,
    merge_documents=False
):
    """
    Import documents from a JSON file into an Azure AI Search index.
    
    Parameters:
    -----------
    search_service_name : str
        The name of your Azure AI Search service
    index_name : str
        The name of the index to import into
    api_key : str
        API key for authenticating to the Azure AI Search service
    input_file : str
        Path to the input JSON file containing documents
    batch_size : int, optional
        Number of documents to upload in each batch (default: 1000)
    show_progress : bool, optional
        Whether to display a progress bar
    merge_documents : bool, optional
        If True, merge documents that already exist; if False, replace them
    
    Returns:
    --------
    int
        Number of documents successfully imported
    """
    try:
        # Set up the search client
        endpoint = f"https://{search_service_name}.search.windows.net/"
        credential = AzureKeyCredential(api_key)
        client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
        
        # Load documents from JSON file
        print(f"Loading documents from {input_file}...")
        with open(input_file, 'r', encoding='utf-8') as f:
            documents = json.load(f)
        
        if not documents:
            print("No documents found in the input file.")
            return 0
            
        total_docs = len(documents)
        print(f"Found {total_docs} documents to import into index '{index_name}'")
        
        # Initialize progress bar if requested
        pbar = None
        if show_progress:
            try:
                pbar = tqdm(total=total_docs)
            except ImportError:
                print("tqdm library not found. Progress bar will not be displayed.")
        
        # Upload documents in batches
        uploaded_count = 0
        failed_count = 0
        
        # Process in batches
        for i in range(0, total_docs, batch_size):
            batch = documents[i:i + batch_size]
            
            try:
                upload_mode = 'mergeOrUpload' if merge_documents else 'upload'
                results = client.upload_documents(documents=batch, indexing_action=upload_mode)
                
                # Count successes and failures
                success_count = sum(1 for r in results if r.succeeded)
                fail_count = len(results) - success_count
                
                uploaded_count += success_count
                failed_count += fail_count
                
                # Update progress
                if pbar:
                    pbar.update(len(batch))
                elif show_progress:
                    print(f"Uploaded {uploaded_count}/{total_docs} documents...", end="\r")
                    
            except Exception as batch_error:
                print(f"\nError uploading batch starting at document {i}: {str(batch_error)}")
                failed_count += len(batch)
        
        if pbar:
            pbar.close()
        elif show_progress:
            print()
        
        print(f"Import complete. Successfully imported {uploaded_count} documents.")
        if failed_count > 0:
            print(f"Failed to import {failed_count} documents.")
            
        return uploaded_count
        
    except Exception as e:
        print(f"Error importing documents: {str(e)}")
        return 0

def main():
    parser = argparse.ArgumentParser(description='Import documents from JSON file to Azure AI Search index')
    parser.add_argument('--service', required=True, help='Azure Search service name')
    parser.add_argument('--index', required=True, help='Index name')
    parser.add_argument('--key', required=True, help='API key')
    parser.add_argument('--input', required=True, help='Input JSON file')
    parser.add_argument('--batch-size', type=int, default=1000, help='Batch size for uploads (default: 1000)')
    parser.add_argument('--merge', action='store_true', help='Merge with existing documents instead of replacing')
    parser.add_argument('--no-progress', action='store_true', help='Hide progress bar')
    
    args = parser.parse_args()
    
    import_json_to_search_index(
        args.service,
        args.index,
        args.key,
        args.input,
        args.batch_size,
        not args.no_progress,
        args.merge
    )

if __name__ == "__main__":
    main()