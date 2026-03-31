import argparse

from password_check import PasswordInWordsDirFilter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check passwords against a wordlist directory.")
    parser.add_argument(
        "directory",
        type=str,
        help="Required directory containing password database/wordlist files."
    )
    args = parser.parse_args()

    checker = PasswordInWordsDirFilter(args.directory)
    print("Pass:", end="")
    password = getpass.getuser("Pass:")
    errors = checker.validate(password)
    if len(errors) > 0:
        print("Password not safe")
        for error in errors:
            print(error)
    else:
        print("Password safe")
