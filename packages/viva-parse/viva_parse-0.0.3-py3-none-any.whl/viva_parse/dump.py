def dump(messages):
    result = ""
    for message in messages:
        result += f"<|{message['role']}|>"

        if 'actions' in message:
            for action in message['actions']:
                result += f"<|{action['name']}|>"
                if 'params' in action:
                    for param, value in action['params'].items():
                        result += f"<[{param}]> {value}"
                if 'return' in action:
                    result += f"<!return!> {action['return']}"
                result += "<|endofaction|>"
        if 'message' in message:
            result += f" {message['message']}"

        result += "<|endoftext|>"

    return result
