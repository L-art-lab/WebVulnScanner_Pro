import requests
from concurrent.futures import ThreadPoolExecutor

PAYLOADS = []
with open("payloads.txt", "r", encoding="utf-8") as f:
	for line in f:
		line = line.strip()
		if line and not line.startswith("#"):
			if "=" in line:
				key, value =line.split("=",1)
				PAYLOADS.append({key: value})

def scan_one_payload(url,payload):
	try:
		response = requests.get(url, params=payload, timeout=15) 
		if "SELECT * FROM users" in response.text:
			return {"status": "SQL注入漏洞", "url": response.url, "payload": payload}
		elif "<script>alert('XSS')</script>" in response.text:
			return {"status": "XSS漏洞", "url": response.url, "payload": payload}
		elif response.status_code == 200 and len(response.text) > 10:
			return {"status": "敏感文件/路径泄露", "url": response.url, "payload": payload}
		else:
			return None
	except requests.exceptions.Timeout:
		print(f"[-] 超时跳过：{url}")
		return None
	except requests.exceptions.ConnectionError:
		print(f"[-] 连接失败跳过：{url}")
		return None
	except Exception as e:
		print(f"[-] 发生未知错误：{e}")
		return None
def run_scan():
    import requests
    from concurrent.futures import ThreadPoolExecutor

    url = "http://localhost:8000/test.php"
    PAYLOADS = []
    
    # 从 payloads.txt 读取所有攻击语句
    with open("payloads.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if "=" in line:
                    key, value = line.split("=", 1)
                    PAYLOADS.append({key: value})
    
    print(f"[*] 启动多线程扫描，共 {len(PAYLOADS)} 个任务...")
    results = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_payload = {
            executor.submit(scan_one_payload, url, p): p 
            for p in PAYLOADS
        }
        
        for future in future_to_payload:
            result = future.result()
            if result:
                results.append(result)
    
    return results