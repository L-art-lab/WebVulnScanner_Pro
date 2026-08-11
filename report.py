import datetime

def generate(results):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. 生成报告主体内容（表格版）
    if results:
        rows = ""
        for r in results:
            # 获取状态和 Payload
            status = r.get("status", "未知漏洞")
            url = r.get("url", "未知URL")
            
            # 处理 Payload 显示（防止报错）
            payload_dict = r.get("payload", {})
            payload_str = str(payload_dict)
            
            # 根据漏洞类型设置颜色
            if "SQL" in status:
                color = "#ffcccc"  # 红色底
            elif "XSS" in status:
                color = "#fff3cd"  # 黄色底
            else:
                color = "#f8f9fa"  # 灰色底
                
            rows += f"""
            <tr style="background-color: {color};">
                <td>{status}</td>
                <td style="word-break: break-all;">{url}</td>
                <td><code>{payload_str}</code></td>
            </tr>
            """
    else:
        rows = "<tr><td colspan='3' style='text-align:center;'>🛡️ 未发现任何漏洞，目标较为安全。</td></tr>"

    # 2. 构建完整的 HTML 页面
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>多线程漏洞扫描报告</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; }}
            h1 {{ color: #2c3e50; }}
            .meta {{ color: #7f8c8d; font-size: 14px; margin-bottom: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #34495e; color: white; }}
            code {{ background: #eee; padding: 2px 6px; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <h1>🔍 Web漏洞自动化扫描报告</h1>
        <div class="meta">
            <p><b>扫描时间：</b> {now}</p>
            <p><b>扫描目标：</b> http://localhost/test.php</p>
            <p><b>任务总数：</b> {len(results)} 个已确认漏洞</p>
        </div>
        
        <h2>📋 漏洞详情列表</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 20%;">漏洞类型</th>
                    <th style="width: 50%;">触发 URL</th>
                    <th style="width: 30%;">攻击载荷 (Payload)</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        <hr>
        <p style="color: gray; font-size: 12px; text-align: center;">报告由 Python 多线程扫描器自动生成</p>
    </body>
    </html>
    """

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    if len(results) > 0:
        print(f"[+] 报告已生成：report.html 共发现 {len(results)} 个漏洞")
    else:
        print("[+] 报告已生成：report.html (未发现任何漏洞)")