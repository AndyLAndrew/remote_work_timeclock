import flet as ft
import pandas as pd
import fitz  # PyMuPDF
import os
from PIL import Image

# Load your CSV data (example path)
df = pd.read_csv("path_to_your_csv_file.csv")

# Clear the assets directory function
def clear_assets_dir(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

# Save PDF pages as PNG images in the assets directory
def save_pdf_pages_as_images(file, output_dir):
    pdf_file = fitz.open(file)
    for i, page in enumerate(pdf_file):
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(f"{output_dir}/{i}.png")

class PDFViewerApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.current_index = 0
        self.pdf_page = 1
        self.load_current_row_data()

    def load_current_row_data(self):
        self.doc_location = df.loc[self.current_index, "doc_location"]
        self.var_number = df.loc[self.current_index, "attribute"]
        self.var_name = df.loc[self.current_index, "annotation_variable"]
        self.var_value = df.loc[self.current_index, "annotation_value"]

        print(f'{self.doc_location}, {self.var_number}, {self.var_name}, {self.var_value}')

        # Clear assets directory and save PDF pages as images
        self.assets_dir = "assets"
        clear_assets_dir(self.assets_dir)
        save_pdf_pages_as_images(self.doc_location, self.assets_dir)

        self.total_pdf_pages = len(os.listdir(self.assets_dir))
        img = Image.open(f"{self.assets_dir}/0.png")
        self.page_width, self.page_height = img.size

    def build(self):
        self.doc_location_text = ft.Text(value=f"Doc Location: {self.doc_location}", size=20)
        self.var_number_text = ft.Text(value=f"Var#: {self.var_number}", size=15)
        self.var_name_text = ft.Text(value=f"VarName: {self.var_name}", size=15)
        self.var_value_text = ft.TextField(value=self.var_value, multiline=True, expand=True)

        self.correct_button = ft.FilledButton(text="Correct", on_click=self.correct_clicked)
        self.incorrect_button = ft.FilledButton(text="Incorrect", on_click=self.incorrect_clicked)
        self.back_button = ft.FilledButton(text="Back", on_click=self.back_clicked)
        self.forward_button = ft.FilledButton(text="Forward", on_click=self.forward_clicked)

        self.pdf_display = ft.Image(src=f"/{self.assets_dir}/0.png", width=self.page_width, height=self.page_height)
        self.page_navigation = ft.Row(
            controls=[
                ft.FilledButton(text="<", on_click=self.prev_page),
                ft.Text(value=f"Page {self.pdf_page}", size=15),
                ft.FilledButton(text=">", on_click=self.next_page),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.save_button = ft.FilledButton(text="Save", on_click=self.save_clicked)

        left_column = ft.Column(
            controls=[
                self.var_number_text,
                self.var_name_text,
                ft.Text(value="VarValue", size=15),
                self.var_value_text,
                ft.Row(
                    controls=[self.correct_button, self.incorrect_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[self.back_button, self.forward_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            expand=True,
        )

        right_column = ft.Column(
            controls=[
                self.pdf_display,
                self.page_navigation,
                self.save_button,
            ],
            expand=True,
        )

        return ft.Column(
            controls=[
                self.doc_location_text,
                ft.Row(
                    controls=[left_column, right_column],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )

    async def correct_clicked(self, e):
        df.at[self.current_index, "correct"] = True
        await self.update_ui()

    async def incorrect_clicked(self, e):
        df.at[self.current_index, "correct"] = False
        await self.update_ui()

    async def back_clicked(self, e):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_current_row_data()
            await self.update_ui()

    async def forward_clicked(self, e):
        if self.current_index < len(df) - 1:
            self.current_index += 1
            self.load_current_row_data()
            await self.update_ui()

    async def prev_page(self, e):
        if self.pdf_page > 1:
            self.pdf_page -= 1
            await self.update_pdf_page()

    async def next_page(self, e):
        if self.pdf_page < self.total_pdf_pages:
            self.pdf_page += 1
            await self.update_pdf_page()

    async def save_clicked(self, e):
        df.to_csv("modified.csv", index=False)
        print("Data saved to modified.csv")

    async def update_ui(self):
        self.doc_location_text.value = f"Doc Location: {self.doc_location}"
        self.var_number_text.value = f"Var#: {self.var_number}"
        self.var_name_text.value = f"VarName: {self.var_name}"
        self.var_value_text.value = self.var_value

        self.pdf_page = 1
        self.pdf_display.src = f"/{self.assets_dir}/0.png"
        self.page_navigation.controls[1].value = f"Page {self.pdf_page}"

        await self.update_async()

    async def update_pdf_page(self):
        self.pdf_display.src = f"/{self.assets_dir}/{self.pdf_page - 1}.png"
        self.page_navigation.controls[1].value = f"Page {self.pdf_page}"
        await self.update_async()

async def main(page: ft.Page):
    page.title = "PDF Viewer App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    await page.update_async()
    app = PDFViewerApp()
    await page.add_async(app)

ft.app(target=main, assets_dir="assets")