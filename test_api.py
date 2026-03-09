import requests

# Test API endpoints
base_url = "http://localhost:5000/api"

try:
    # Test health endpoint
    response = requests.get(f"{base_url}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    
    # Test gender distribution
    response = requests.get(f"{base_url}/gender-distribution")
    print(f"Gender data: {response.status_code} - {response.json()}")
    
    # Test with filters
    response = requests.get(f"{base_url}/gender-distribution?school=GP&subject=Math")
    print(f"Filtered gender data: {response.status_code} - {response.json()}")
    
except requests.exceptions.ConnectionError:
    print("❌ Backend API is not running on localhost:5000")
    print("Please start the backend with: cd src/backend/api && python app.py")
except Exception as e:
    print(f"❌ Error testing API: {e}")
