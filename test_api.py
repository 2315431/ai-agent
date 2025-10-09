#!/usr/bin/env python3
"""
Comprehensive API Test Script for Content Repurposing Agent
Tests all endpoints automatically and provides detailed error analysis
"""

import requests
import json
import time
from datetime import datetime
import uuid
import os

# Configuration
BASE_URL = "https://ai-agent-ikc8.onrender.com"
TEST_USERNAME = "admin"
TEST_PASSWORD = "admin"

class APITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        self.test_results = []
        
    def log_result(self, test_name, success, response_data, error=None):
        """Log test result"""
        result = {
            "test_name": test_name,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data,
            "error": error
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if error:
            print(f"   Error: {error}")
        if response_data and isinstance(response_data, dict):
            print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
        print()

    def test_health_check(self):
        """Test basic health endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                self.log_result("Health Check", True, data)
                return True
            else:
                self.log_result("Health Check", False, None, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Health Check", False, None, str(e))
            return False

    def test_root_endpoint(self):
        """Test root endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                self.log_result("Root Endpoint", True, data)
                return True
            else:
                self.log_result("Root Endpoint", False, None, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Root Endpoint", False, None, str(e))
            return False

    def test_basic_test(self):
        """Test basic test endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/test")
            if response.status_code == 200:
                data = response.json()
                self.log_result("Basic Test", True, data)
                return True
            else:
                self.log_result("Basic Test", False, None, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Basic Test", False, None, str(e))
            return False

    def test_authentication(self):
        """Test authentication"""
        try:
            response = self.session.post(f"{self.base_url}/auth/login?username={TEST_USERNAME}&password={TEST_PASSWORD}")
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
                self.log_result("Authentication", True, {"token_received": bool(self.access_token)})
                return True
            else:
                self.log_result("Authentication", False, None, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Authentication", False, None, str(e))
            return False

    def test_demo_generate(self):
        """Test demo content generation"""
        try:
            payload = {
                "text": "artificial intelligence and machine learning in business",
                "type": "linkedin_post"
            }
            response = self.session.post(f"{self.base_url}/demo/generate", json=payload)
            if response.status_code == 200:
                data = response.json()
                self.log_result("Demo Generate", True, data)
                return True
            else:
                self.log_result("Demo Generate", False, None, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Demo Generate", False, None, str(e))
            return False

    def test_ai_generate(self):
        """Test AI content generation"""
        try:
            payload = {
                "text": "business and events management for corporate meetings",
                "type": "linkedin_post",
                "audience": "professionals",
                "tone": "professional"
            }
            response = self.session.post(f"{self.base_url}/ai/generate", json=payload)
            if response.status_code == 200:
                data = response.json()
                self.log_result("AI Generate", True, data)
                return True
            else:
                self.log_result("AI Generate", False, None, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("AI Generate", False, None, str(e))
            return False

    def test_content_sources(self):
        """Test content sources listing"""
        try:
            response = self.session.get(f"{self.base_url}/content/sources")
            if response.status_code == 200:
                data = response.json()
                self.log_result("Content Sources", True, {"count": len(data), "sources": data})
                return True
            else:
                self.log_result("Content Sources", False, None, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Content Sources", False, None, str(e))
            return False

    def test_debug_all_sources(self):
        """Test debug all sources endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/debug/all-sources")
            if response.status_code == 200:
                data = response.json()
                self.log_result("Debug All Sources", True, {"count": len(data), "sources": data})
                return True
            else:
                self.log_result("Debug All Sources", False, None, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Debug All Sources", False, None, str(e))
            return False

    def test_database_init(self):
        """Test database initialization"""
        try:
            response = self.session.post(f"{self.base_url}/admin/init-db")
            if response.status_code == 200:
                data = response.json()
                self.log_result("Database Init", True, data)
                return True
            else:
                self.log_result("Database Init", False, None, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Database Init", False, None, str(e))
            return False

    def test_file_upload(self):
        """Test file upload"""
        try:
            # Create a test file
            test_content = "This is a test blog post about artificial intelligence and machine learning in business. AI is transforming industries and creating new opportunities for growth and innovation."
            test_filename = f"test_blog_{uuid.uuid4().hex[:8]}.txt"
            
            files = {"file": (test_filename, test_content, "text/plain")}
            data = {
                "source_type": "text",
                "title": "Test Blog Post",
                "description": "Automated test upload"
            }
            
            response = self.session.post(f"{self.base_url}/content/upload", files=files, data=data)
            if response.status_code == 200:
                data = response.json()
                self.log_result("File Upload", True, data)
                return True
            else:
                self.log_result("File Upload", False, None, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("File Upload", False, None, str(e))
            return False

    def test_different_content_types(self):
        """Test different content types"""
        content_types = ["linkedin_post", "twitter_thread", "instagram_carousel", "newsletter_section"]
        
        for content_type in content_types:
            try:
                payload = {
                    "text": f"Test content for {content_type} about business automation",
                    "type": content_type,
                    "audience": "business owners",
                    "tone": "professional"
                }
                response = self.session.post(f"{self.base_url}/ai/generate", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    self.log_result(f"Generate {content_type}", True, data)
                else:
                    self.log_result(f"Generate {content_type}", False, None, f"Status: {response.status_code}")
            except Exception as e:
                self.log_result(f"Generate {content_type}", False, None, str(e))

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive API Tests")
        print("=" * 50)
        
        # Basic connectivity tests
        self.test_health_check()
        self.test_root_endpoint()
        self.test_basic_test()
        
        # Authentication
        self.test_authentication()
        
        # Content generation tests
        self.test_demo_generate()
        self.test_ai_generate()
        self.test_different_content_types()
        
        # Database initialization
        self.test_database_init()
        
        # Content management tests
        self.test_debug_all_sources()
        self.test_content_sources()
        
        # File operations
        self.test_file_upload()
        
        # Re-test content sources after upload
        self.test_content_sources()
        
        # Generate summary
        self.generate_summary()

    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test_name']}: {result['error']}")
        
        print("\n🎯 RECOMMENDATIONS:")
        if failed_tests == 0:
            print("  🎉 All tests passed! Your API is working perfectly.")
        elif failed_tests <= 2:
            print("  ⚠️  Minor issues detected. Check failed tests above.")
        else:
            print("  🚨 Multiple issues detected. Review and fix failed tests.")
        
        # Save detailed results
        with open("test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        print(f"\n📄 Detailed results saved to: test_results.json")

def main():
    """Main function"""
    print("Content Repurposing Agent - API Test Suite")
    print(f"Testing URL: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    tester = APITester(BASE_URL)
    tester.run_all_tests()

if __name__ == "__main__":
    main()
