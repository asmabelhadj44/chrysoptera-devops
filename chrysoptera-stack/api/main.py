from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/readings")
def readings():
    return [
        {"site_id": 1, "solar_output_kw": 4.2},
        {"site_id": 2, "solar_output_kw": 3.8}
    ]
