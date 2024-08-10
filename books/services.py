import requests

# def search_books(query, search_type='title', page=1, limit=25):
#     base_url = 'https://openlibrary.org/search.json'
#     params = {
#         search_type: query,
#         'page': page,
#         'limit': limit
#     }
#     try:
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()  # Will raise an HTTPError for bad responses
#         return response.json()
#     except requests.RequestException as e:
#         # Handle exceptions and log errors if needed
#         return {'error': str(e)}

def search_books(query, search_type='title', start_index=0, max_results=25):
    base_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': f'{search_type}:{query}',
        'startIndex': start_index,
        'maxResults': max_results,
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}
