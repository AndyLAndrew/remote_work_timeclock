import flet as ft
import time

def main(page: ft.Page):
    file_list = []
    export_path = ""

    pb = ft.ProgressBar(width=400, value=0)  # Initialize progress bar with value set to 0

    def on_select_files_result(e: ft.FilePickerResultEvent):
        nonlocal file_list
        if e.files:
            file_list = [f.path for f in e.files]
            selected_files.value = "Selected Files: " + ", ".join(file_list)
        else:
            selected_files.value = "File selection cancelled!"
        selected_files.update()

    def on_save_to_result(e: ft.FilePickerResultEvent):
        nonlocal export_path
        if e.path:
            export_path = e.path
            export_path_text.value = "Export Path: " + export_path
        else:
            export_path_text.value = "Save location selection cancelled!"
        export_path_text.update()

    def convert(e):
        if not file_list:  # Check if the file list is empty
            return  # Exit the function if the file list is empty

        if export_path:
            button_convert.disabled = True
            page.update()

            # Perform custom function (placeholder)
            custom_func(file_list, export_path)

            button_convert.disabled = False
            page.update()

    def custom_func(file_list, export_path):
        # Placeholder for the custom function logic
        for i in range(101):
            pb.value = i * 0.01  # Update progress bar value
            time.sleep(0.1)  # Simulate processing time
        pb.value = 0  # Reset progress bar value to 0 after completion
        page.update()

    # File picker for selecting files
    pick_files_dialog = ft.FilePicker(on_result=on_select_files_result)

    # File picker for saving files
    save_file_dialog = ft.FilePicker(on_result=on_save_to_result)

    # Append file pickers to the page overlay
    page.overlay.extend([pick_files_dialog, save_file_dialog])

    # Define buttons and texts
    selected_files = ft.Text(value="Selected Files: None")
    export_path_text = ft.Text(value="Export Path: None")

    button_select_files = ft.ElevatedButton(
        text="Select Files",
        on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True)
    )
    button_save_to = ft.ElevatedButton(
        text="Save To",
        on_click=lambda _: save_file_dialog.save_file()
    )

    # Convert button defined after the convert function
    button_convert = ft.ElevatedButton(
        text="Convert",
        on_click=convert
    )

    # Add buttons and status texts to the page
    page.add(
        ft.Column([
            ft.Row([button_select_files, selected_files]),
            ft.Row([button_save_to, export_path_text]),
            ft.Row([button_convert]),
            ft.Row([pb])  # Add progress bar to the page
        ])
    )

    # Resize window to 600x400 pixels and make it resizable
    page.window_width = 600
    page.window_height = 400
    page.window_resizable = True
    page.update()

ft.app(target=main)