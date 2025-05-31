from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import json
import os
import argparse
import sys
from tqdm import tqdm

def export_search_index_to_json(
    search_service_name,
    index_name,
    api_key,
    output_file,
    select_fields=None,
    filter_expression=None,
    top=None,
    show_progress=True
):
    """
    Export all documents from an Azure AI Search index to a JSON file.
    
    Parameters:
    -----------
    search_service_name : str
        The name of your Azure AI Search service
    index_name : str
        The name of the index to export
    api_key : str
        API key for authenticating to the Azure AI Search service
    output_file : str
        Path to the output JSON file
    select_fields : list, optional
        List of fields to include in the output. If None, all fields are included.
    filter_expression : str, optional
        OData filter expression to filter documents
    top : int, optional
        Maximum number of documents to export. If None, all documents are exported.
    show_progress : bool, optional
        Whether to display a progress bar
    
    Returns:
    --------
    int
        Number of documents exported
    """
    try:
        # Set up the search client
        endpoint = f"https://{search_service_name}.search.windows.net/"
        credential = AzureKeyCredential(api_key)
        client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
        
        # Get document count to estimate progress
        count_result = client.search("*", include_total_count=True, top=0)
        total_docs = count_result.get_count()
        
        if top:
            total_docs = min(total_docs, top)
            
        print(f"Found {total_docs} documents in index '{index_name}'")
        
        # Initialize progress bar if requested
        pbar = None
        if show_progress:
            try:
                pbar = tqdm(total=total_docs)
            except ImportError:
                print("tqdm library not found. Progress bar will not be displayed.")
        
        # Prepare search options
        search_options = {
            "include_total_count": True
        }
        if select_fields:
            search_options["select"] = select_fields
        if filter_expression:
            search_options["filter"] = filter_expression
        
        # Set page size for efficiency
        page_size = 1000  # Max page size
        search_options["top"] = page_size
        
        # Get all documents (handling pagination)
        all_docs = []
        skip = 0
        
        while True:
            search_options["skip"] = skip
            results = client.search("*", **search_options)
            
            # Convert results to dictionaries for JSON serialization
            page_docs = []
            for doc in results:
                doc_dict = {k: v for k, v in doc.items()}
                page_docs.append(doc_dict)
            
            if not page_docs:
                break
                
            all_docs.extend(page_docs)
            skip += len(page_docs)
            
            # Update progress bar
            if pbar:
                pbar.update(len(page_docs))
            elif show_progress:
                print(f"Exported {len(all_docs)}/{total_docs} documents...", end="\r")
            
            # If we specified a top value and we've reached it
            if top and len(all_docs) >= top:
                all_docs = all_docs[:top]
                break
                
            # If we got fewer docs than requested (end of results)
            if len(page_docs) < page_size:
                break
        
        if pbar:
            pbar.close()
        elif show_progress:
            print()
        
        # Write to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_docs, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully exported {len(all_docs)} documents to {output_file}")
        return len(all_docs)
        
    except Exception as e:
        print(f"Error exporting documents: {str(e)}")
        return 0

def main():
    parser = argparse.ArgumentParser(description='Export Azure AI Search index to JSON file')
    parser.add_argument('--service', required=True, help='Azure Search service name')
    parser.add_argument('--index', required=True, help='Index name')
    parser.add_argument('--key', required=True, help='API key')
    parser.add_argument('--output', required=True, help='Output JSON file')
    parser.add_argument('--select', nargs='+', help='Fields to include (space separated)')
    parser.add_argument('--filter', help='OData filter expression')
    parser.add_argument('--top', type=int, help='Maximum number of documents to export')
    parser.add_argument('--no-progress', action='store_true', help='Hide progress bar')
    
    args = parser.parse_args()
    
    export_search_index_to_json(
        args.service,
        args.index,
        args.key,
        args.output,
        args.select,
        args.filter,
        args.top,
        not args.no_progress
    )

if __name__ == "__main__":
    main()