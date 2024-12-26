import tkinter as tk  # Import tkinter for GUI elements
from fetch_prices import fetch_prices  # Import fetch_prices function to fetch asset data
import time
import os  # Import for folder and file management
from datetime import datetime  # Import for timestamping
from PIL import ImageGrab  # Import for taking screenshots
"""
Current Features:
- Displays live prices for cryptocurrencies (e.g., Bitcoin, Ethereum, Litecoin) and stocks (e.g., Tesla, Apple, S&P 500).
- Updates prices and 24-hour percentage changes every 30 seconds using fetch_prices.py.
- Includes filter buttons to dynamically toggle between cryptocurrencies and stocks.
- Utilizes a professional dark theme with alternating row colors for enhanced readability.
- Handles errors by displaying error messages when data cannot be fetched.
- Last update timestamp dynamically reflects the latest refresh, currently set at 30 seconds.

Future Improvements:
1. Add Sorting:
   - Include options to sort assets alphabetically, by price, or by percentage change.
2. Historical Data and Charts:
   - Display sparkline or historical charts for each asset.
3. Alert System:
   - Integrate a visual or sound-based alert when certain thresholds are crossed (e.g., 5% price change).
4. Save and Load Configuration:
   - Allow users to customize and save their asset list and preferred settings.
5. Enhanced Filtering:
   - Add multi-select filtering options to display specific combinations of assets.
6. Mobile-Friendly Design:
   - Make the GUI responsive and usable on smaller screens.
7. Data Export:
   - Provide functionality to export the displayed data to CSV or Excel.
8. Custom Themes:
   - Allow users to toggle between light and dark themes.
9. Additional Data:
   - Include market capitalization, volume, or other financial metrics for each asset.
10. Multi-Currency Support:
   - Enable users to view prices in different currencies (e.g., USD, EUR, GBP).

"""


class CryptoDashboard:
    def __init__(self, root):
        # Set up the main application window (root)
        self.root = root
        self.root.title("Rorie's Dashboard")  # Set the window title
        self.root.geometry("950x550")  # Set the size of the window
        self.root.configure(bg="#121212")  # Set a dark background color for the window

        # Create and display the main header
        self.header = tk.Label(
            root,
            text="Asset Manager",  # Header text
            font=("Arial", 20, "bold"),  # Font style, size, and weight for the header
            fg="#00bfff",  # Header text color
            bg="#121212",  # Header background color matches the main window
        )
        self.header.pack(pady=10)  # Add padding around the header for better spacing

        # Create a frame to hold the filter buttons
        self.button_frame = tk.Frame(root, bg="#121212")  # Frame background matches the main window
        self.button_frame.pack(pady=10)  # Add padding around the button frame

        # Add a button to filter for cryptocurrencies
        self.crypto_button = tk.Button(
            self.button_frame,
            text="Crypto",  # Button label
            font=("Arial", 12),  # Font style and size
            command=lambda: self.filter_assets("crypto"),  # Action: filter for cryptocurrencies
            bg="#1e1e2f",  # Button background color
            fg="white",  # Button text color
            width=20  # Button width
        )
        self.crypto_button.pack(side="left", padx=10)  # Position the button on the left with padding

        # Add a button to filter for stocks
        self.stock_button = tk.Button(
            self.button_frame,
            text="Stocks",  # Button label
            font=("Arial", 12),  # Font style and size
            command=lambda: self.filter_assets("stock"),  # Action: filter for stocks
            bg="#1e1e2f",  # Button background color
            fg="white",  # Button text color
            width=20  # Button width
        )
        self.stock_button.pack(side="left", padx=10)  # Position the button on the left with padding

        # Create a frame to hold the data table
        self.table_frame = tk.Frame(root, bg="#121212")  # Frame background matches the main window
        self.table_frame.pack(pady=10)  # Add padding around the table frame

        # Define the table headers and display them
        headers = ["Asset", "Price", "24%"]  # Column headers
        for col, text in enumerate(headers):  # Iterate through each header
            tk.Label(
                self.table_frame,
                text=text,  # Header text
                font=("Arial", 14, "bold"),  # Font style and size for headers
                fg="white",  # Text color for headers
                bg="#1e1e2f",  # Header background color for contrast
                width=20,  # Width of each header cell
                anchor="center",  # Center-align text in headers
            ).grid(row=0, column=col, padx=5, pady=5)  # Position headers in a grid layout

        # Initialize a dictionary to store rows for each asset
        self.rows = {}
        # Define the list of all assets, specifying their types for filtering
        self.assets = [
            # Cryptocurrencies
            {"name": "Bitcoin", "type": "crypto"},
            {"name": "Ethereum", "type": "crypto"},
            {"name": "Litecoin", "type": "crypto"},
            {"name": "XRP", "type": "crypto"},
            {"name": "Monero", "type": "crypto"},
            {"name": "Cardano", "type": "crypto"},
            {"name": "Dogecoin", "type": "crypto"},
            # Stocks
            {"name": "S&P 500", "type": "stock"},
            {"name": "Tesla", "type": "stock"},
            {"name": "Nio", "type": "stock"},
            {"name": "Apple", "type": "stock"},
        ]
        # Start by showing all assets
        self.active_assets = self.assets
        self.display_assets()  # Display all assets initially

        # Create a label to display the last update timestamp
        self.last_update_label = tk.Label(
            root,
            text="Last Update: Fetching...",  # Default text for the last update label
            font=("Arial", 12),  # Font style and size
            fg="#00ff00",  # Text color (green) to indicate success
            bg="#121212",  # Background color matches the main window
        )
        self.last_update_label.pack(pady=10)  # Add padding around the label

        # Create a label to display error messages
        self.error_label = tk.Label(
            root,
            text="",  # Default text is empty (no error)
            font=("Arial", 12),  # Font style and size
            fg="red",  # Text color (red) to indicate errors
            bg="#121212",  # Background color matches the main window
        )
        self.error_label.pack(pady=5)  # Add padding around the error label

        # Start the periodic update process
        self.update_prices()

    def display_assets(self):
        """
        Display rows for the currently active assets.
        """
        # Clear existing rows from the table frame
        for widget in self.table_frame.winfo_children():
            widget.destroy()  # Remove all widgets in the frame

        # Redraw the headers
        headers = ["Asset", "Price", "24%"]  # Column headers
        for col, text in enumerate(headers):
            tk.Label(
                self.table_frame,
                text=text,  # Header text
                font=("Arial", 14, "bold"),  # Font style and size for headers
                fg="white",  # Text color
                bg="#1e1e2f",  # Header background color
                width=20,
                anchor="center",
            ).grid(row=0, column=col, padx=5, pady=5)  # Position headers

        # Populate the table with rows for each active asset
        for i, asset in enumerate(self.active_assets, start=1):
            bg_color = "#2b2b2b" if i % 2 == 0 else "#1e1e2f"  # Alternate row colors
            asset_name = asset["name"]  # Get the asset name
            self.rows[asset_name] = {}
            # Create and display the asset name cell
            tk.Label(
                self.table_frame,
                text=asset_name,
                font=("Arial", 12),
                fg="white",
                bg=bg_color,
                width=20,
                anchor="center",
            ).grid(row=i, column=0, padx=5, pady=5)
            # Create and display the price cell
            self.rows[asset_name]["price"] = tk.Label(
                self.table_frame,
                text="Fetching...",
                font=("Arial", 12),
                fg="white",
                bg=bg_color,
                width=20,
                anchor="center",
            )
            self.rows[asset_name]["price"].grid(row=i, column=1, padx=5, pady=5)
            # Create and display the 24% change cell
            self.rows[asset_name]["change_24hr"] = tk.Label(
                self.table_frame,
                text="--",
                font=("Arial", 12),
                fg="white",
                bg=bg_color,
                width=20,
                anchor="center",
            )
            self.rows[asset_name]["change_24hr"].grid(row=i, column=2, padx=5, pady=5)

    def filter_assets(self, asset_type):
        """
        Filter assets by type and refresh the display.
        :param asset_type: The type of asset to display ("crypto" or "stock").
        """
        # Filter assets by their type
        self.active_assets = [asset for asset in self.assets if asset["type"] == asset_type]
        self.display_assets()  # Refresh the table to show only the filtered assets

    def update_prices(self):
        """
        Fetch and update prices for all displayed assets.
        """
        data = fetch_prices()  # Fetch data using the fetch_prices function
        if data:  # Check if data is successfully fetched
            for asset_name, values in data.items():  # Iterate through fetched data
                if asset_name in self.rows:  # Update only rows that are displayed
                    # Update the price cell with the fetched price
                    self.rows[asset_name]["price"].config(text=f"£{values['price']}")
                    # Update the 24% change cell with the fetched percentage
                    if "change_24hr" in values:  # Check if the 24-hour change is available
                        self.rows[asset_name]["change_24hr"].config(text=values["change_24hr"])
            # Update the last update timestamp
            self.last_update_label.config(text=f"Last Update: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.error_label.config(text="")  # Clear any existing error messages
        else:
            # Display an error message if data fetching fails
            self.error_label.config(text="Error fetching data. Retrying...")

        # Schedule the next update after 30 seconds
        self.root.after(30000, self.update_prices)


        
    def take_screenshot(self):
        """
        Takes a screenshot of the dashboard and saves it in a structured folder hierarchy:
        Day > Hour > Minute.
        """
        # Get the current time
        now = datetime.now()
        day = now.strftime("%Y-%m-%d")  # Format the current day (e.g., "2024-11-26")
        hour = now.strftime("%H")  # Format the current hour (e.g., "14")
        minute = now.strftime("%M")  # Format the current minute (e.g., "15")

        # Define the base folder path on the desktop
        base_folder = os.path.join(os.path.expanduser("~"), "Desktop", "DashboardScreenshots")
        day_folder = os.path.join(base_folder, day)  # Create a folder for the current day
        hour_folder = os.path.join(day_folder, hour)  # Create a folder for the current hour

        # Ensure the folder structure exists
        os.makedirs(hour_folder, exist_ok=True)

        # Define the screenshot file path
        screenshot_path = os.path.join(hour_folder, f"{minute}.png")

        # Take a screenshot of the entire dashboard window
        x0 = self.root.winfo_rootx()  # X-coordinate of the window's top-left corner
        y0 = self.root.winfo_rooty()  # Y-coordinate of the window's top-left corner
        x1 = x0 + self.root.winfo_width()  # Width of the window
        y1 = y0 + self.root.winfo_height()  # Height of the window

        # Capture and save the screenshot
        screenshot = ImageGrab.grab(bbox=(x0, y0, x1, y1))  # Grab the region of the app
        screenshot.save(screenshot_path)  # Save the screenshot as a PNG file
        print(f"Screenshot saved to {screenshot_path}")  # Log the save location

        # Schedule the next screenshot in 15 minutes (900,000 ms)
        self.root.after(900000, self.take_screenshot)


if __name__ == "__main__":
    # Create the root application window
    root = tk.Tk()
    # Initialize the CryptoDashboard with the root window
    app = CryptoDashboard(root)
    # Run the Tkinter event loop
    root.mainloop()
