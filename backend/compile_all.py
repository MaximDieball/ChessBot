import os
import sys
import subprocess

BOT_DIRECTORIES = [
    "bots/botLib",
    "bots/botv5",
    "bots/botv6"
]


def compile_all():
    backend_root = os.path.abspath(os.path.dirname(__file__))

    for bot_dir in BOT_DIRECTORIES:
        target_path = os.path.join(backend_root, bot_dir)
        print(f"Building: {bot_dir}")

        if not os.path.exists(target_path):
            print(f"Error: Directory {bot_dir} not found.")
            sys.exit(1)

        # Create the builds directory and __init__.py if they don't exist
        builds_dir = os.path.join(target_path, "builds")
        os.makedirs(builds_dir, exist_ok=True)

        init_file = os.path.join(builds_dir, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                pass

        os.chdir(target_path)

        try:
            subprocess.check_call([sys.executable, "compile.py", "build_ext", "--inplace"])
            print(f"Success: {bot_dir}")
        except subprocess.CalledProcessError as e:
            print(f"Failed: {bot_dir}")
            sys.exit(e.returncode)

        os.chdir(backend_root)

    print("Build complete.")


if __name__ == "__main__":
    compile_all()