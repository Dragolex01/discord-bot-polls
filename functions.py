def poll_visualizer(polls, poll_name, response):
    for option in polls[poll_name]["options"]:
        response += f"- {option['option']}\n"

    return response