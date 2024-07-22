from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/welcome", response_class=HTMLResponse, include_in_schema=False)
def index():
    html_content = """
    <html>
        <head>
            <title>Welcome to the TFBS API</title>
        </head>
        <body>
            <h2><b>Welcome to the TFBS API</b></h2>
            <p>This API allows you to find Transcription Factor Binding Sites (TFBS) in promoter sequences of given genes.</p>
            <h3>Available Endpoints:</h3>
            <ul>
                <li><b>GET /health</b> - Check the health status of the API</li>
                <li><b>POST /tfbs</b> - Find TFBS in promoter sequences of given genes</li>
            </ul>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
