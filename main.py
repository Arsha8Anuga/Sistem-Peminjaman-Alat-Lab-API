from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def test():
    return {"key" : "hello world"}

if __name__ == "__main__" :
    uvicorn.run(app="main:app", host="localhost", port=5173, reload=True)

