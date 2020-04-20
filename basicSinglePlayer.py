import random

def move(data):
    # get all possible moves that we can take without colliding
    moves = possibleMoves(data)
    print(f"Possible Moves: {moves}")
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
        elif ("up" in moves) and (data["you"]["body"][0]["y"] > data["board"]["food"][0]["y"]):
            return "up"
    # none of the moves bring us closer to the food so we pick a random one
    # TODO: have some decision making here so that its not random
    # 1. iterate through all the food instead of just index 0?       
    return random.choice(moves)

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

    for snakes in data["board"]["snakes"]:
        # if the snakes health is 100 then it just ate so the tail will not move next turn
        # add another copy of the tail to the end of the snake to avoid colliding with it
        if snakes["health"] == 100:
            snakes["body"].append(snakes["body"][-1].copy())
        # if snake is longer than us then we want to avoid head to head collision
        # add all possible points opposing snake could turn to (doesnt matter if the points are invalid)
        if snakes["id"] != data["you"]["id"] and len(snakes["body"]) >= len(data["you"]["body"]):
            snakes["body"].insert({"x": snakes["body"][0]["x"], "y": data["you"]["body"][0]["y"] - 1})
            snakes["body"].insert({"x": snakes["body"][0]["x"], "y": data["you"]["body"][0]["y"] + 1})
            snakes["body"].insert({"x": snakes["body"][0]["x"] - 1, "y": data["you"]["body"][0]["y"]})
            snakes["body"].insert({"x": snakes["body"][0]["x"] + 1, "y": data["you"]["body"][0]["y"]})

    # check for collision against all snakes
    for snakes in data["board"]["snakes"]:
        for body in snakes["body"]:
            if "up" in moves and up == body:
                moves.remove("up")
            if "down" in moves and down == body:
                moves.remove("down")
            if "left" in moves and left == body:
                moves.remove("left")
            if "right" in moves and right == body:
                moves.remove("right")
    return moves              

