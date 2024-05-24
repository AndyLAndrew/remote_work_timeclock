
import asyncio, time, flet as ft


class Clock():
    def __init__(self):
        super().__init__()
        self.seconds = 1
        self.is_stopwatch_on = False  # Flag to control timer play/pause

    async def did_mount_async(self):
        self.running = True
        asyncio.create_task(self.update_stopwatch())
        asyncio.create_task(self.update_clock())

    async def will_unmount_async(self):
        self.running = False

    async def update_stopwatch(self):
        while self.seconds and self.running:
            if self.is_stopwatch_on:
                mins, secs = divmod(self.seconds, 60)
                self.countup.value = "{:02d}:{:02d}".format(mins, secs)
                await self.update_async()
                await asyncio.sleep(1)
                self.seconds += 1
            else:
                await asyncio.sleep(1)

    async def update_clock(self):
        while self.running:
            current_time = time.strftime("%H:%M", time.localtime())
            self.clock.value = current_time
            await self.update_async()
            await asyncio.sleep(1)

    async def toggle_stopwatch(self, e):
        # Toggle the play/pause state
        self.is_stopwatch_on = not self.is_stopwatch_on

        # Update the button's selected state
        e.control.selected = self.is_stopwatch_on
        await e.control.update_async()

    async def reset_stopwatch(self, e):
        # Reset/Update the stopwatch
        self.seconds = 1
        self.countup.value = "00:00"
        await self.update_async()


class TodoApp(ft.UserControl, Clock):

    def build(self):
        self.countup = ft.Text(value="00:00")
        self.clock = ft.Text()
        self.timer_row = ft.Row(
            controls=[
                ft.Text(value="Current Time:", size=10),
                self.clock,  # Initialize the clock control
                ft.Text(value="Elapsed:", size=10),
                self.countup,   # Initialize the timer control
                ft.IconButton(
                    icon=ft.icons.PLAY_CIRCLE_FILLED_OUTLINED,
                    selected_icon=ft.icons.PAUSE_CIRCLE_FILLED_OUTLINED,
                    on_click=self.toggle_stopwatch,
                    tooltip="Play/Pause Stopwatch",
                    selected=self.is_stopwatch_on,
                ),
                ft.IconButton(
                    icon=ft.icons.UNDO_ROUNDED,
                    selected_icon=ft.icons.UNDO_OUTLINED,
                    on_click=self.reset_stopwatch,
                    tooltip="Reset Stopwatch",
                )
            ]
        )

        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks = ft.Column()

        # application's root control (i.e. "view") containing all other controls
        return ft.Column(
            width=600,
            controls=[
                self.timer_row,
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                self.tasks,
            ],
        )

    async def add_clicked(self, e):
        task = Task(self.new_task.value, self.task_delete)
        self.tasks.controls.append(task)
        self.new_task.value = ""
        await self.update_async()

    async def task_delete(self, task):
        self.tasks.controls.remove(task)
        await self.update_async()


class Task(ft.UserControl):
    def __init__(self, task_name, task_delete):
        super().__init__()
        self.task_name = task_name
        self.task_delete = task_delete

    def build(self):
        self.display_task = ft.Checkbox(value=False, label=self.task_name)
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return ft.Column(controls=[self.display_view, self.edit_view])

    async def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        await self.update_async()

    async def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        await self.update_async()

    async def delete_clicked(self, e):
        await self.task_delete(self)


async def main(page: ft.Page):
    page.title = "Time Clock ToDo"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    await page.update_async()
    await page.add_async(Clock())
    # create application instance
    todo = TodoApp()
    # add application's root control to the page
    await page.add_async(todo)


ft.app(target=main)