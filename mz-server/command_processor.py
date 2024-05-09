# command_processor.py

def process_command(data):
    """
    Processes commands received from the client based on the 'action' field in the data.

    Args:
        data (dict): The data received from the client, expected to be a dictionary.

    Returns:
        dict: The response dictionary containing the status and a message.
    """
    action = data.get('action')
    if action == 'login':
        return login(data)
    elif action == 'create_vm':
        return create_vm(data)
    else:
        return {"status": "error", "message": "Unknown command"}

def login(data):
    """
    Authenticates a user based on username and password.

    Args:
        data (dict): The dictionary containing 'username' and 'password'.

    Returns:
        dict: The result of the authentication process.
    """
    username = data.get('username')
    password = data.get('password')
    if username == 'admin' and password == 'admin123':
        return {"status": "success", "message": "Login successful"}
    else:
        return {"status": "error", "message": "Authentication failed"}

def create_vm(data):
    """
    Simulates the creation of a virtual machine. This function can be expanded
    with actual VM creation logic.

    Args:
        data (dict): The dictionary that might contain parameters for VM creation.

    Returns:
        dict: Confirmation of VM creation.
    """
    # Placeholder for actual VM creation logic
    return {"status": "success", "message": "VM created successfully"}

