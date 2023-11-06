from quart import Quart, request, jsonify
from Helpers.GenerateToken import generate_token
from Helpers.Cosine import CalculateSimilarity

app = Quart(__name__)

def run() -> None:
    app.run()

@app.post("/generate_token")
async def echo():
    data = await request.get_json()
    dd = generate_token(data['input'])
    return {"token": dd}

@app.post("/calculate_similarity")
async def calc():
    data = await request.get_json()
    result = CalculateSimilarity(data['posts'], data['userprofile'])
    return {"similarity_dict": result}