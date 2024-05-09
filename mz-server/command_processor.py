# command_processor.py

def process_command(data):
    """
    Process commands based on data received from the client.

    Args:
    data (dict): Parsed JSON data from the client.

    Returns:
    dict: Response to be sent back to the client.
    """
    # Determine the action requested by the client and call the appropriate function
    action = data.get('action')
    if action == 'login':
        return login(data)
    elif action == 'create_vm':
        return create_vm(data)
    else:
        return {"status": "error", "message": "Unknown command"}

def login(data):
    """
    Handle login authentication.

    Args:
    data (dict): Contains username and password for authentication.

    Returns:
    dict: Result of the authentication process.
    """
    username = data.get('username')
    password = data.get('password')
    # Simple check for username and password (replace with secure check in production)
    if username == 'admin' and password == 'admin123':
        return {"status": "success", "message": "Login successful"}
    else:
        return {"status": "error", "message": "Authentication failed"}

def create_vm(data):
    """
    Placeholder function for VM creation logic.

    Args:
    data (dict): Contains data necessary to create a VM.

    Returns:
    dict: Confirmation of VM creation.
    """
    # Example: Assume VM creation is successful
    return {"status": "success", "message": "VM created successfully"}

