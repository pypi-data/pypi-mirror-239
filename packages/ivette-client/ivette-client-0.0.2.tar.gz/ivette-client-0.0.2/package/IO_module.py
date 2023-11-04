import re
import os
import shutil

def setUp():
    # Create a new file
    folder_name = "tmp"
    if not os.path.exists(folder_name):
        # If it doesn't exist, create the folder
        os.mkdir(folder_name)
        print(f"Folder '{folder_name}' created.")
    else:
        print(f"Folder '{folder_name}' already exists.")


def cleanUp(prefix):
    for filename in os.listdir():
        if filename.startswith(prefix):
            os.remove(filename)

    # Check if the "tmp" subdirectory exists and then remove it
    tmp_dir = os.path.join(os.getcwd(), "tmp")
    if os.path.exists(tmp_dir) and os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)


def validate_filename(filename, allowed_extensions=[".inp"]):
    """
    Validates a filename to ensure it ends with one of the allowed extensions.

    Args:
        filename (str): The filename to be validated.
        allowed_extensions (list): A list of allowed file extensions. Default is ['.log', '.out', '.txt', '.inp'].

    Returns:
        str: The valid filename.

    Raises:
        None

    This function checks whether the provided 'filename' ends with one of the 'allowed_extensions'. If the
    'filename' is valid, it returns the filename. If not, it repeatedly prompts the user to enter a valid
    filename until a valid one is provided.

    Example usage:
    >>> filename = validate_filename(input("Enter a filename: "))
    >>> print(f"Valid filename: {filename}")

    Note:
    - The function uses regular expressions to perform a case-insensitive check on the file extension.
    - If the 'filename' provided by the user does not end with a valid extension, the user will be prompted
      to provide a valid filename until a valid one is given.
    - The list of 'allowed_extensions' determines the file extensions that are considered valid. By default,
      the function allows '.log', '.out', '.txt', and '.inp' extensions, but you can customize this list
      by providing your own list of allowed extensions.
    """
    while True:
        # Use regular expressions to check if the filename ends with a valid extension (case-insensitive)
        if re.search(r"\.(log|out|txt|inp)$", filename, re.IGNORECASE):
            return filename
        else:
            print(f"Invalid extension. Please use one of {allowed_extensions}")
        filename = input("Enter a valid filename: ")


def get_cpu_core_count():
    """
    Determine the number of CPU cores available on the system.

    Returns:
        int: The number of CPU cores available.

    Raises:
        None

    This function attempts to retrieve the number of CPU cores available on the system using the
    `os.cpu_count()` function. If successful, it returns the actual number of CPU cores. If there is an issue
    with determining the core count (e.g., due to an AttributeError or NotImplementedError), the function
    returns a reasonable default value of 4.

    Note:
    - The number of CPU cores is a significant factor in parallel computing and multi-threaded applications.
    - The default value of 4 is returned as a reasonable assumption when the core count cannot be determined.
    """
    try:
        return os.cpu_count()
    except (AttributeError, NotImplementedError):
        # If the number of CPU cores cannot be determined, return a reasonable default value
        return 4


def validate_cpu_core_input(input_str):
    """
    Validate user input for selecting the number of CPU cores.

    Args:
        input_str (str): The user's input as a string.

    Returns:
        int: The validated number of CPU cores if it falls within the allowed range, or None if the input is invalid.

    Raises:
        None

    This function attempts to validate the user's input for selecting the number of CPU cores. It first tries to
    convert the input string to an integer. If successful, it checks whether the input is within the allowed range
    (from 1 to the number of available CPU cores, inclusive). If the input is valid, it returns the selected number
    of CPU cores. If the input is outside the allowed range, an error message is displayed, and None is returned.
    If the input is not a valid integer, another error message is displayed, and None is returned.

    Note:
    - The function relies on the `get_cpu_core_count()` function to determine the number of available CPU cores on
      the system.
    - The user is guided to enter a valid integer within the appropriate range, and error messages are displayed to
      provide feedback in case of input errors.
    """
    try:
        # Attempt to convert the input string to an integer
        input_value = int(input_str)
        cpu_core_count = get_cpu_core_count()  # Get the number of available CPU cores

        # Check if the input is within the valid range (1 to the number of CPU cores)
        if 1 <= input_value <= cpu_core_count:
            return input_value  # Return the selected core count
        else:
            print(f"Please enter an integer between 1 and {cpu_core_count}.")
            return None
    except ValueError:
        print("Please enter a valid integer.")
        return None

def setCPU():
    cpu_core_count = get_cpu_core_count()
    print(f"Your computer has {cpu_core_count} CPU core(s).")

    while True:
        user_input = input("Enter the number of CPU cores to use: ")
        validated_input = validate_cpu_core_input(user_input)

        if validated_input is not None:
            print(f"You have selected {validated_input} CPU core(s).")
            return validated_input