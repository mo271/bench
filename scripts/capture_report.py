import http.server
import threading
import os
from requests_html import HTMLSession

PORT = 8088
SCRIPT_DIR = "docs/"
HTML_FILE = 'index.html'

def run_server(server_dir, port):
    """Starts a simple web server in a background thread."""
    os.chdir(server_dir)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.ThreadingHTTPServer(("", port), handler)

    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print(f"")
    return httpd

def capture_html():
    """Captures rendered HTML using requests-html."""
    httpd = run_server(SCRIPT_DIR, PORT)
    session = HTMLSession()
    output_html = ""

    try:
        url = f"http://localhost:{PORT}/{HTML_FILE}"
        r = session.get(url)
        r.html.render(sleep=1, wait=10, timeout=20)

        # Find the first 'table' element on the page.
        # The 'first=True' argument returns the element directly, not a list.
        table_element = r.html.find('table', first=True)

        # Check if the table was actually found before trying to access it.
        if table_element:
            output_html = table_element.html
            pass
        else:
            output_html = "mmh"



    except Exception as e:
        output_html = f"failed: {e}"
    finally:
        session.close()
        httpd.shutdown()
        print("")

    return output_html


if __name__ == "__main__":
    final_html_output = capture_html()
    print(final_html_output)