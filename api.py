from fastapi import FastAPI
from starlette.responses import HTMLResponse
from scrapers.composer import get_composer_content
from scrapers.portfolio_visualizer import get_pv_content

app = FastAPI()

@app.get("/")
async def return_main_page():
    html = """
        <h1>Welcome!</h1>
        <p>This is a tool that api bridge between a scraper that has the following possible endpoints:</p>
        <br><br/>
        <ul>IP:PORT/composer/?symphony_id=xyz</ul>
        <ul>...</ul>
        """
    return HTMLResponse(html)

@app.get("/composer/")
async def get_composer_symphony_holdings(symphony_id: str):
    webpage_content = await get_composer_content(symphony_id)
    return HTMLResponse(content=webpage_content, status_code=200)

@app.get("/pv/")
async def get_pv_holdings(link: str, name: str):
    webpage_content = await get_pv_content(link, name)
    return HTMLResponse(content=webpage_content, status_code=200)

if __name__ == "__main__":
     import uvicorn
     uvicorn.run(app, host="127.0.0.1", port=8000)