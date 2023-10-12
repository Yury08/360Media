import uvicorn

if __name__ == '__main__':
    uvicorn.run("krwz_films.asgi:application", reload=True, port=8000, log_level="info", workers=4, lifespan='auto')
