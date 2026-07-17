import requests

def fetch_data(url, headers=None, binary=False):
    try:
        # Send GET request with optional headers
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        # Raise HTTPError if the status code is 4xx or 5xx
        response.raise_for_status()
        if binary:
            return response.content

        return response.text

    except requests.exceptions.HTTPError as http_err:
        raise RuntimeError(f"HTTP error occurred: {http_err}") from http_err

    except requests.exceptions.ConnectionError as conn_err:
        raise RuntimeError(f"Connection error occurred: {conn_err}") from conn_err

    except requests.exceptions.Timeout as timeout_err:
        raise RuntimeError(f"Request timed out: {timeout_err}") from timeout_err

    except requests.exceptions.RequestException as req_err:
        raise RuntimeError(f"An error occurred: {req_err}") from req_err