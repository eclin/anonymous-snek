import json

def move(data):
    parsedData = json.loads(data)
    if parsedData["you"]["body"][0]["x"] < parsedData["board"]["food"][0]["x"]:
        return "right"
    elif parsedData["you"]["body"][0]["x"] > parsedData["board"]["food"][0]["x"]:
        return "left"
    else:
        if parsedData["you"]["body"][0]["y"] < parsedData["board"]["food"][0]["y"]:
            return "up"
        else:
            return "down"