import re

def check_password_strength(password: str) -> bool:
    """
    Check whether the given password meets the following criteria:
      - At least 8 characters long
      - Contains at least one lowercase letter
      - Contains at least one uppercase letter
      - Contains at least one digit
      - Contains at least one special character (non-alphanumeric)
    Returns True if all criteria are met, else False.
    """
    pattern = re.compile(
        r'^(?=.*[a-z])'        # at least one lowercase letter
        r'(?=.*[A-Z])'         # at least one uppercase letter
        r'(?=.*\d)'            # at least one digit
        r'(?=.*[^A-Za-z0-9])'  # at least one special character
        r'.{8,}$'              # at least 8 characters in total
    )
    return bool(pattern.fullmatch(password))


def main():
    try:
        password = input("Enter password for strength check: ")
    except (KeyboardInterrupt, EOFError):
        print("\nNo input provided. Exiting.")
        return

    if check_password_strength(password):
        print("Password is valid and satisfies strength criteria.")
    else:
        print("Password does not satisfy strength criteria. It must:")
        print("- Be at least 8 characters long")
        print("- Contain at least one lowercase letter")
        print("- Contain at least one uppercase letter")
        print("- Contain at least one digit")
        print("- Contain at least one special character (non-alphanumeric)")

if __name__ == "__main__":
    main()
