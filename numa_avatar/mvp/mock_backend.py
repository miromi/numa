#!/usr/bin/env python3
"""
简单的模拟后端服务，用于测试Avatar功能
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

class MockBackendHandler(BaseHTTPRequestHandler):
    """模拟后端服务处理器"""
    
    def do_GET(self):
        """处理GET请求"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == "/docs":
            # 健康检查端点
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Mock Backend Service</h1>")
        elif path == "/api/tasks/1":
            # 获取任务详情
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            task_data = {
                "id": 1,
                "title": "测试任务",
                "description": "这是一个测试任务，用于验证Avatar功能",
                "application_id": 1,
                "code_branch": "feature/test-task"
            }
            self.wfile.write(json.dumps(task_data).encode())
        elif path == "/api/applications/1":
            # 获取应用信息
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            app_data = {
                "id": 1,
                "name": "测试应用",
                "git_repo_url": "https://github.com/example/test-app.git"
            }
            self.wfile.write(json.dumps(app_data).encode())
        elif path == "/api/topics/tasks":
            # 获取任务topic
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            topic_data = {
                "id": 1,
                "name": "tasks"
            }
            self.wfile.write(json.dumps(topic_data).encode())
        else:
            # 404 Not Found
            self.send_response(404)
            self.end_headers()
    
    def do_PUT(self):
        """处理PUT请求"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path.startswith("/api/tasks/") and path.endswith("/status"):
            # 更新任务状态
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response_data = {"status": "success"}
            self.wfile.write(json.dumps(response_data).encode())
        else:
            # 404 Not Found
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """处理POST请求"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path.startswith("/api/tasks/") and path.endswith("/logs"):
            # 上报任务日志
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response_data = {"status": "success"}
            self.wfile.write(json.dumps(response_data).encode())
        else:
            # 404 Not Found
            self.send_response(404)
            self.end_headers()

def run_mock_backend(port=7301):
    """运行模拟后端服务"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MockBackendHandler)
    print(f"Starting mock backend server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_mock_backend()