from fastapi import FastAPI, WebSocket
from faster_whisper import WhisperModel

app = FastAPI()

# Load Faster Whisper model (adjust parameters as needed)
model = model = WhisperModel("small", device="cpu")

@app.get("/")
async def root():
    return {"message": "Welcome to Demon-flask! This is a real-time translation API."}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("WebSocket connection established!")
    
    try:
        while True:
            # Receive audio data from the client
            audio_data = await websocket.receive_bytes()

            # Process audio with Faster Whisper
            segments, _ = model.transcribe(audio_data, language="en", task="translate")

            # Combine translated text and send back to the client
            translated_text = " ".join([segment.text for segment in segments])
            await websocket.send_text(translated_text)
    except Exception as e:
        await websocket.close()
        print(f"WebSocket closed: {e}")

