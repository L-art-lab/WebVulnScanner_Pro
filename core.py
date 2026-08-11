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
		response = requests.get(url, params=payload,timeout=15)
		if "users" in response.text:
			print("\n[!] 漏洞确认！目标存在SQL注入漏洞。")
			return{
			"status": "SQL注入漏洞",
			"url": response.url,
			"payload": payload
			}
		elif "<script>alert('XSS')</script>" in response.text:
			return {
			"status": "XSS漏洞",
			"url": response.url,
			"payload": payload
			}
		else:
			return None
	except Exception as e:
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