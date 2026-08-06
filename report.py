import datetime

def generate(results):
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	vuln_list = ""
	for r in results:
		vuln_list += f"<li><b>类型: </b>{r['status']} <br><b>URL: </b>{r['url']} <br><b>Payload: </b>{r['payload']}</li><br>"
	if not results:
		vuln_list = "<li>未发现任何漏洞。</li>" 
	html_content = f"""
<html>
<head><meta charset="utf-8"><title>多线程漏洞扫描报告</title></head>
<body style="font-family: sans-serif; padding: 20px;">
	<h1>🔍多线程漏洞自动化扫描报告</h1>
	<p><b>扫描时间：</b> {now}</p>
	<p><b>扫描目标：</b> http://localhost/test.php</p>
	<h2>检测结果汇总: </h2>
	</ul>
	<hr>
	<p style="color: gray; font-size: 12px;">报告由Python多线程扫描器自动生成</p>
</body>
</html>
"""
	with open("report.html", "w", encoding="utf-8") as f:
		f.write(html_content)
	print("[+] 报告已生成：report.html (共发现{len(results)}个漏洞)")
