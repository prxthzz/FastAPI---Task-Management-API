"""
Test script for Task Management API
"""

import requests
import json
from time import sleep

# Base URL for the API
BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section title"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_response(title, method, endpoint, response):
    """Print formatted API response"""
    print(f"{method} {endpoint}")
    print(f"   Status Code: {response.status_code}")
    if response.status_code != 204:  # 204 No Content
        try:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2, default=str)}")
        except:
            print(f"   Response: {response.text}")
    print()

def test_health_check():
    """Test health check endpoint"""
    print_section("1. HEALTH CHECK")
    response = requests.get(f"{BASE_URL}/")
    print_response("Health Check", "GET", "/", response)
    return response.status_code == 200

def test_create_tasks():
    """Test creating multiple tasks"""
    print_section("2. CREATE TASKS")
    
    tasks_data = [
        {
            "title": "Implement user authentication",
            "description": "Add JWT-based authentication to the API with role-based access control"
        },
        {
            "title": "Fix database connection timeout",
            "description": "Resolve timeout issues occurring during peak hours"
        },
        {
            "title": "Write API documentation",
            "description": "Create comprehensive API documentation with examples"
        },
        {
            "title": "Deploy to production",
            "description": "Set up CI/CD pipeline and deploy application to production server"
        }
    ]
    
    created_tasks = []
    for i, task_data in enumerate(tasks_data, 1):
        response = requests.post(f"{BASE_URL}/tasks", json=task_data)
        print_response(f"Create Task {i}", "POST", "/tasks", response)
        if response.status_code == 201:
            created_tasks.append(response.json())
    
    return created_tasks

def test_get_task_by_id(task_id):
    print_section("3. GET TASK BY ID")
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print_response("Get Task by ID", "GET", f"/tasks/{task_id}", response)
    return response

def test_list_all_tasks():
    print_section("4. LIST ALL TASKS")
    response = requests.get(f"{BASE_URL}/tasks")
    print_response("List All Tasks", "GET", "/tasks", response)
    return response

def test_list_tasks_by_status(status):
    print_section(f"5. LIST TASKS BY STATUS - {status.upper()}")
    response = requests.get(f"{BASE_URL}/tasks", params={"status": status})
    print_response(f"List Tasks ({status})", "GET", f"/tasks?status={status}", response)
    return response

def test_update_task(task_id, update_data):
    print_section("6. UPDATE TASK")
    response = requests.patch(f"{BASE_URL}/tasks/{task_id}", json=update_data)
    print_response("Update Task", "PATCH", f"/tasks/{task_id}", response)
    return response

def test_get_statistics():
    print_section("7. GET TASK STATISTICS")
    response = requests.get(f"{BASE_URL}/tasks/stats/summary")
    print_response("Task Statistics", "GET", "/tasks/stats/summary", response)
    return response

def test_delete_task(task_id):
    print_section("8. DELETE TASK")
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    print_response("Delete Task", "DELETE", f"/tasks/{task_id}", response)
    return response

def test_invalid_task_id():
    print_section("9. ERROR HANDLING - INVALID TASK ID")
    invalid_id = "invalid-task-id-12345"
    response = requests.get(f"{BASE_URL}/tasks/{invalid_id}")
    print_response("Get Invalid Task", "GET", f"/tasks/{invalid_id}", response)
    return response.status_code == 404

def test_validation_error():
    print_section("10. ERROR HANDLING - VALIDATION ERROR")
    invalid_task = {
        "title": "",  # Empty title should fail validation
        "description": "This should fail"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=invalid_task)
    print_response("Create Task (Invalid)", "POST", "/tasks", response)
    return response.status_code == 422

def run_all_tests():
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*12 + "TASK MANAGEMENT API - FULL TEST SUITE" + " "*9 + "║")
    print("╚" + "="*58 + "╝")
    
    results = {}
    
    # Test 1: Health Check
    results["Health Check"] = test_health_check()
    sleep(0.5)
    
    # Test 2: Create Tasks
    created_tasks = test_create_tasks()
    results["Create Tasks"] = len(created_tasks) == 4
    
    if created_tasks:
        first_task = created_tasks[0]
        task_id = first_task["id"]
        
        sleep(0.5)
        
        # Test 3: Get Task by ID
        response = test_get_task_by_id(task_id)
        results["Get Task by ID"] = response.status_code == 200
        sleep(0.5)
        
        # Test 4: List All Tasks
        response = test_list_all_tasks()
        results["List All Tasks"] = response.status_code == 200
        sleep(0.5)
        
        # Test 5: Update Task Status to in_progress
        update_data = {"status": "in_progress"}
        response = test_update_task(task_id, update_data)
        results["Update Task"] = response.status_code == 200
        sleep(0.5)
        
        # Test 5b: List pending tasks
        response = test_list_tasks_by_status("pending")
        results["List Pending Tasks"] = response.status_code == 200
        sleep(0.5)
        
        # Test 6: Get Statistics
        response = test_get_statistics()
        results["Get Statistics"] = response.status_code == 200
        sleep(0.5)
        
        # Test 7: Update Task Status to completed
        print_section("UPDATE TASK TO COMPLETED")
        update_data = {"status": "completed"}
        response = test_update_task(task_id, update_data)
        sleep(0.5)
        
        # Test 8: List completed tasks
        response = test_list_tasks_by_status("completed")
        results["List Completed Tasks"] = response.status_code == 200
        sleep(0.5)
        
        # Test 9: Delete Task
        response = test_delete_task(task_id)
        results["Delete Task"] = response.status_code == 204
        sleep(0.5)
    
    # Test Error Handling
    results["Invalid Task ID"] = test_invalid_task_id()
    sleep(0.5)
    
    results["Validation Error"] = test_validation_error()
    
    # Print Summary
    print_section("TEST SUMMARY")
    print("Test Results:")
    print("-" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {test_name:.<40} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("-" * 60)
    print(f"\nTotal: {passed + failed} tests | Passed: {passed} | Failed: {failed}")
    
    if failed == 0:
        print("\n ALL TESTS PASSED! API is working perfectly!\n")
    else:
        print(f"\n {failed} test(s) failed.\n")
    
    return failed == 0

if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print("\nERROR: Cannot connect to API at http://localhost:8000")
        print("   Make sure the server is running: python app.py\n")
        exit(1)
    except Exception as e:
        print(f"\nERROR: {str(e)}\n")
        exit(1)
