import os
import joblib
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

model_dir = os.path.join(os.path.dirname(__file__), "model")
vectorizer = joblib.load(os.path.join(model_dir, "vectorizer.joblib"))
model = joblib.load(os.path.join(model_dir, "model.joblib"))

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


class Message(BaseModel):
    text: str


@app.get("/")
def index():
    return FileResponse(os.path.join(static_dir, "index.html"))


@app.post("/classify")
def classify(message: Message):
    vector = vectorizer.transform([message.text])
    prediction = model.predict(vector)[0]
    probabilities = model.predict_proba(vector)[0]
    return {
        "prediction": prediction,
        "confidence": round(max(probabilities) * 100, 1),
        "ham_prob": round(probabilities[0] * 100, 1),
        "spam_prob": round(probabilities[1] * 100, 1),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
