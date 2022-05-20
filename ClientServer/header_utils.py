LENGTH_HEADER_SIZE = 8
USER_HEADER_SIZE = 16


def format_message(username, message):
    if not message:
        return None
    length_header = f'{len(message):<{LENGTH_HEADER_SIZE}}'
    user_header = f'{username:<{USER_HEADER_SIZE}}'
    return f'{length_header}{user_header}{message}'
