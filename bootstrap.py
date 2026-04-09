import os
import sys
import subprocess
import platform

ENV_NAME = "venv"

def run(cmd):
    print(f"\n▶ {' '.join(cmd)}\n")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("❌ Command failed")
        sys.exit(result.returncode)

def main():
    print("========== DEBUG INFO ==========")
    print("OS:", platform.system(), platform.release())
    print("Python Executable:", sys.executable)
    print("Python Version:", sys.version)
    print("Working Directory:", os.getcwd())
    print("================================")

    # Prevent running inside venv
    if "venv" in sys.executable or ".venv" in sys.executable:
        print("❌ Do NOT run this script inside a virtual environment")
        print("👉 Run: python3 bootstrap.py (Mac/Linux)")
        print("👉 Run: python bootstrap.py (Windows)")
        sys.exit(1)

    # Step 1: Create venv
    if not os.path.exists(ENV_NAME):
        print("\n🔧 Creating virtual environment...")
        run([sys.executable, "-m", "venv", ENV_NAME])
    else:
        print("\n⚠️ Virtual environment already exists, skipping creation")

    # Step 2: Resolve paths
    system = platform.system()

    if system == "Windows":
        venv_python = os.path.join(ENV_NAME, "Scripts", "python.exe")
        activate_cmd = f"{ENV_NAME}\\Scripts\\activate"
    else:
        venv_python = os.path.join(ENV_NAME, "bin", "python")
        activate_cmd = f"source {ENV_NAME}/bin/activate"

    # Verify venv
    if not os.path.exists(venv_python):
        print("❌ ERROR: Virtual environment was not created properly")
        print("👉 Try manually:")
        print(f"{sys.executable} -m venv {ENV_NAME}")
        sys.exit(1)

    print(f"\n✅ Virtual environment ready: {venv_python}")

    # Step 3: Upgrade pip
    print("\n⬆️ Upgrading pip...")
    run([venv_python, "-m", "pip", "install", "--upgrade", "pip"])

    # Step 4: Install requirements
    if os.path.exists("requirements.txt"):
        print("\n📦 Installing requirements...")
        run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("\n⚠️ No requirements.txt found, skipping install")

    print("\n✅ SETUP COMPLETE!")

    # Step 5: Auto-open terminal with venv activated
    print("\n🚀 Attempting to open a new terminal with venv activated...")

    try:
        if system == "Windows":
            subprocess.run(
                f'start powershell -NoExit -Command "cd \'{os.getcwd()}\'; {activate_cmd}"',
                shell=True
            )

        elif system == "Darwin":  # macOS
            subprocess.run([
                "osascript",
                "-e",
                f'tell application "Terminal" to do script "cd {os.getcwd()} && {activate_cmd}"'
            ])

        else:  # Linux
            subprocess.run([
                "gnome-terminal",
                "--",
                "bash",
                "-c",
                f"cd {os.getcwd()} && {activate_cmd}; exec bash"
            ])

    except Exception as e:
        print("⚠️ Could not open new terminal automatically")
        print("Error:", e)

    # Step 6: Manual fallback
    print("\n👉 If the new terminal did NOT open, do this manually:\n")
    print("----- COPY THIS -----")
    print(activate_cmd)
    print("---------------------")

    print("\n💡 After activation, you should see something like:")
    print("(venv) your-terminal$")

if __name__ == "__main__":
    main()