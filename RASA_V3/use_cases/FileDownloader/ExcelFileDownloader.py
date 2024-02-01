import pandas as pd
import os
import shutil

class ExcelFileDownloader:
    @staticmethod
    def download_excelfile_in_local(data, filename):
        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(data)
        
        # Save the DataFrame to an Excel file
        df.to_excel(filename, index=False)

        # Move the file to the Downloads directory
        file_path = os.path.join(os.getcwd(), filename)
        downloads_path = os.path.expanduser("~\\Downloads")
        new_file_path = os.path.join(downloads_path, filename)
        shutil.move(file_path, new_file_path)

        # Get the file URL for sending to the user
        file_url = f"file://{new_file_path}"
        print(f"successfully downloaded {filename}")
        return file_url

    @staticmethod
    def download_excelfile_in_server(data, filename):
        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(data)

        # Define the directory where you want to save the file on the server
        server_excel_directory = "/app/excel_files"  # Adjust this path to your server's configuration

        # Ensure the directory exists
        os.makedirs(server_excel_directory, exist_ok=True)

        # Save the DataFrame to an Excel file in the server directory
        server_filepath = os.path.join(server_excel_directory, filename)
        df.to_excel(server_filepath, index=False)
        
        # Specify the new file path in the server downloads directory
        server_new_file_path = f"http://20.235.145.135:7739/excel_files/{filename}.xlsx"
        # Move the file to the server downloads directory
        # shutil.move(server_filepath, server_new_file_path)

        # Get the file URL for sending to the user
        file_url = server_new_file_path
        return  file_url