import markdown, pathlib

md_path = r'D:\ClaudeCodeTest\archivio\dispensa-diritto-pubblico\SCHEMI_STUDIO.md'
html_path = r'D:\ClaudeCodeTest\archivio\dispensa-diritto-pubblico\SCHEMI_STUDIO.html'

content = pathlib.Path(md_path).read_text(encoding='utf-8')
body = markdown.markdown(content, extensions=['tables', 'fenced_code'])

css = """
body { font-family: Georgia, serif; max-width: 900px; margin: 40px auto; padding: 0 20px; color: #222; line-height: 1.6; }
h1 { color: #1a1a2e; border-bottom: 3px solid #1a1a2e; padding-bottom: 8px; }
h2 { color: #16213e; border-bottom: 2px solid #ccc; padding-bottom: 5px; margin-top: 40px; }
h3 { color: #0f3460; margin-top: 20px; }
ul { margin: 8px 0; padding-left: 20px; }
li { margin: 4px 0; }
strong { color: #0f3460; }
hr { border: none; border-top: 1px solid #ddd; margin: 30px 0; }
code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-size: 0.9em; }
@media print { body { margin: 20px; } h2 { page-break-before: always; } }
"""

html = "<!DOCTYPE html>\n<html lang='it'>\n<head><meta charset='utf-8'><title>Schemi Diritto Pubblico</title>\n<style>" + css + "</style></head>\n<body>" + body + "</body></html>"

pathlib.Path(html_path).write_text(html, encoding='utf-8')
print("File HTML creato:", html_path)
