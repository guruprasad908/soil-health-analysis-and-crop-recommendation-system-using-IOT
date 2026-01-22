import urllib.request
import json

try:
    # Test local connection
    print("Testing local connection to FastAPI server...")
    response = urllib.request.urlopen('http://localhost:8000/')
    data = json.loads(response.read())
    print(f"Local connection successful: {data}")
    
    # Test network connection
    print("\nTesting network connection to FastAPI server...")
    response = urllib.request.urlopen('http://10.238.141.218:8000/')
    data = json.loads(response.read())
    print(f"Network connection successful: {data}")
    
except Exception as e:
    print(f"Error: {e}")