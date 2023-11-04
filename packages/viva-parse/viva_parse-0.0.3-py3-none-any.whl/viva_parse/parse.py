import re

available_roles = [
    "prompter",
    "assistant",
    "system"
]

def parse_messages(raw_text, roles=available_roles):
    pattern = re.compile(f"<\|({'|'.join(roles)})\|>(.*?)(?=<\|endoftext\|>)")

    # Matches two patterns: roles (either prompter or assistant) and their corresponding messages until <|endoftext|>
    matches = re.findall(pattern, raw_text)

    messages = [{"role": role, "message": message.strip()} for role, message in matches]
    messages = [parse_actions(message) for message in messages]
    return messages

def parse_actions(message):
    pattern = re.compile("<\|(?P<action>[^|]+)\|>(?P<params>[^!|]+)?(?:<!return!>(?P<return>[^|]+)?)?<\|endofaction\|>")

    msg = message["message"]
    message["actions"] = []

    for match in re.finditer(pattern, msg):
        action = match.group("action")
        params = match.group("params")
        return_match = match.group("return")
        
        action = {
            "name": action
        }
        
        if params:
            action["params"] = parse_params(params)
        
        if return_match:
            action["return"] = return_match.replace("<!return!>", "").strip()
            
            
        message["actions"].append(action)
    
    if not message["actions"]:
        del message["actions"]

    msg = re.sub(pattern, "", msg)
    message["message"] = msg.strip()

    return message

def parse_params(params_raw):
    pattern = re.compile("<\[(?P<param>[^\]]+)\]>(?P<value>[^<\[]+)")

    params = dict()
    for match in re.finditer(pattern, params_raw):
        params[match.group("param")] = match.group("value").strip()

    return params
