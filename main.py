import core
import report

if __name__ == "__main__":
	print("[*] Web漏洞扫描器启动中...")
	result = core.run_scan()
	report.generate(result)
