def poll_visualizer(polls, poll_name, response):
    for opt in polls[poll_name]["options"]:
        response += f"- {opt['option']}\n"

    return response