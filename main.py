import time, gsheet, bot, dashapp_real, dashapp_history
from fastapi import Request, FastAPI, WebSocket
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import HTMLResponse

# setup
app = FastAPI()
app.mount("/real", WSGIMiddleware(dashapp_real.app.server))
app.mount("/history", WSGIMiddleware(dashapp_history.app.server))

html= """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Monitor System</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
        <style>
            .content {
            max-width: 500px;
            margin: auto;
            }
        </style>
    </head>
    <body>
        <div class='content'>
            <h1>Monitor System using Dash and Plotly</h1>
            <h2>by Hazrien bin Nazman</h2>

            <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Dashboard
                </button>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="/real">Real Time</a></li>
                    <li><a class="dropdown-item" href="/history">History</a></li>
                </ul>
            </div>
        </div>  
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous"></script>
    </body>
</html>
"""

@app.get("/")
def read_root():
    # bot.main()
    return HTMLResponse(html)

@app.post("/tele")
async def telebot():
    bot.main()
    return {"Telegram": "Bot"}

@app.post("/data/")
async def create_item(request: Request):
    jitem = await request.json()
    
    datetime = time.strftime('%m/%d/%Y %H:%M:%S')

    jitem_data = jitem['data']
    data=[datetime]

    for x in jitem_data.values():
        data.append(x)

    print(data)
    gsheet.wks.append_table([data])

    gsheet.save_to_csv()

    return jitem['data']

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
