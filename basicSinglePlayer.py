def move(data):
    # get all possible moves that we can take without colliding
    moves = possibleMoves(data)
    # there are no moves so we just return up since it doesnt matter
    if not moves:
        return "up"
    # if we can take a a certain move and moving in that direction would bring us closer to the food then we take that move
    # TODO: pick closest food instead of index 0
    if ("right" in moves) and (data["you"]["body"][0]["x"] < data["board"]["food"][0]["x"]):
        return "right"
    elif ("left" in moves) and (data["you"]["body"][0]["x"] > data["board"]["food"][0]["x"]):
        return "left"
    else:
        if ("down" in moves) and (data["you"]["body"][0]["y"] < data["board"]["food"][0]["y"]):
            return "down"
        else:
            return "up"

def possibleMoves(data):
    moves = ["up", "down", "left", "right"]
    # new coordinates of the head after taking each possible move
    up = {"x": data["you"]["body"][0]["x"], "y": data["you"]["body"][0]["y"] - 1}
    down = {"x": data["you"]["body"][0]["x"], "y": data["you"]["body"][0]["y"] + 1}
    left = {"x": data["you"]["body"][0]["x"] - 1, "y": data["you"]["body"][0]["y"]}
    right = {"x": data["you"]["body"][0]["x"] + 1, "y": data["you"]["body"][0]["y"]}

    # restrict movements if at the edge of the arena
    if data["you"]["body"][0]["x"] == 0:
        moves.remove("left")
    elif data["you"]["body"][0]["x"] == data["board"]["width"] - 1:
        moves.remove("right")
    if data["you"]["body"][0]["y"] == 0:
        moves.remove("up")
    elif data["you"]["body"][0]["y"] == data["board"]["height"] - 1:
        moves.remove("down")

    # check for collision against all snakes
    # TODO: consider that the other snakes are also taking a move so:
    # 1. we avoid headon collisions with bigger snakes
    # 2. we can ignore collisions with the tails of snakes that are not about to consume a food
    for snakes in data["board"]["snakes"]:
        for body in snakes:
            if "up" in moves and up == body:
                moves.remove("up")
            if "down" in moves and down == body:
                moves.remove("down")
            if "left" in moves and left == body:
                moves.remove("left")
            if "right" in moves and right == body:
                moves.remove("right")
    return moves              

