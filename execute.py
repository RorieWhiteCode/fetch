import os  # Import for managing file paths
import subprocess  # Import to run other Python files as separate processes

def run_dashboard():
    """
    Executes the gui_display.py file to start the dashboard.
    """
    try:
        # Get the path to the gui_display.py script
        script_path = os.path.join(os.path.dirname(__file__), "gui_display.py")

        # Run the dashboard script
        subprocess.run(["python", script_path], check=True)
    except Exception as e:
        # Print the error message if script execution fails
        print(f"Error executing gui_display.py: {e}")

if __name__ == "__main__":
    # Run the dashboard
    run_dashboard()
