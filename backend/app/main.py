from fastapi import FastAPI

app = FastAPI(
    title="AI Translation Platform",
    version="1.0.0",
    description="Enterprise AI Translation Platform API",
)


@app.get("/")
def root():
    return {"message": "AI Translation Platform API is running 🚀"}
