def move(data):
    if data["you"]["body"][0]["x"] < data["board"]["food"][0]["x"]:
        return "right"
    elif data["you"]["body"][0]["x"] > data["board"]["food"][0]["x"]:
        return "left"
    else:
        if data["you"]["body"][0]["y"] < data["board"]["food"][0]["y"]:
            return "up"
        else:
            return "down"