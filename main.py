import time, gsheet, bot, dashapp
from fastapi import Request, FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

# setup
app = FastAPI()
app.mount("/dashboard", WSGIMiddleware(dashapp.app.server))

@app.post("/")
def read_root():
    bot.main()
    return {"Hibiscus": "Sense"}

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

