import os
import json
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError

OWNER = "girish-kumar07"
REPO = "LeetCode-DSA"
PORT = 8765

TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN is not set.")


class Handler(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):

        if self.path != "/upload":
            self.send_json(404, {"error": "Endpoint not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            data = json.loads(raw.decode("utf-8"))

            number = str(data["number"]).strip()
            title = str(data["title"]).strip()
            difficulty = str(data["difficulty"]).strip().capitalize()
            code = str(data["code"])

            if difficulty not in ("Easy", "Medium", "Hard"):
                raise ValueError("Invalid difficulty.")

            folder_name = (
                f"{int(number):04d}-"
                + title.lower().replace(" ", "-")
            )

            github_path = (
                f"{difficulty}/{folder_name}/solution.py"
            )

            encoded = base64.b64encode(
                code.encode("utf-8")
            ).decode("utf-8")

            url = (
                f"https://api.github.com/repos/"
                f"{OWNER}/{REPO}/contents/{github_path}"
            )

            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/json",
                "User-Agent": "LeetCode-Automation"
            }

            # Check whether the file already exists
            request = Request(url, headers=headers, method="GET")

            try:
                with urlopen(request) as response:
                    existing = json.loads(
                        response.read().decode("utf-8")
                    )
                    sha = existing.get("sha")

            except HTTPError as error:
                if error.code == 404:
                    sha = None
                else:
                    raise

            payload = {
                "message": f"Add LeetCode #{number} - {title}",
                "content": encoded
            }

            if sha:
                payload["sha"] = sha

            request = Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="PUT"
            )

            with urlopen(request) as response:
                result = json.loads(
                    response.read().decode("utf-8")
                )

            action = "updated" if sha else "created"

            self.send_json(200, {
                "success": True,
                "action": action,
                "path": github_path,
                "commit": result["commit"]["sha"]
            })

        except Exception as error:
            self.send_json(500, {
                "success": False,
                "error": str(error)
            })


print(f"LeetCode automation server running on http://127.0.0.1:{PORT}")
print("Keep this terminal open.")

server = HTTPServer(("127.0.0.1", PORT), Handler)
server.serve_forever()