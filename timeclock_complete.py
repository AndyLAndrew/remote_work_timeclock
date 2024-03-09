import flet as ft
import time, threading  # do NOT use threading for future iterations

class TodoApp(ft.UserControl):
    def __init__(self):  # initialize our clock and timer displays
        super().__init__()
        self.clock = ft.Text(value="00:00:00", size=10)
        self.timer = ft.Text(value="00:00:00", size=10)
        self.is_timer_on = False  # Flag to control timer play/pause

    def build(self):
        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks = ft.Column()

        # Row for the clock/timer
        self.timer_row = ft.Row(
            controls=[
                ft.Text(value="Clock:", size=10),
                self.clock,  # Initialize the clock control
                ft.Text(value="Timer:", size=10),
                self.timer,   # Initialize the timer control
                ft.IconButton(
                    icon=ft.icons.PLAY_CIRCLE_FILLED_OUTLINED,
                    selected_icon=ft.icons.PAUSE_CIRCLE_FILLED_OUTLINED,
                    on_click=self.toggle_timer,
                    tooltip="Toggle Timer",
                    selected=self.is_timer_on,
                ),
            ]
        )

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
    def clock_thread(self):
        while True:
            current_time = time.strftime("%H:%M:%S", time.localtime())
            self.clock.value = current_time
            time.sleep(1)

    def timer_thread(self):
        start_time = time.time()
        while True:
            if self.is_timer_on:
                elapsed_time = time.time() - start_time
                formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

                # Update the timer text field
                self.timer.value = formatted_time

                # Sleep for a short interval before updating again
                time.sleep(1)
                # Make sure to handle thread termination conditions if needed
    def add_clicked(self, e):
        task = Task(self.new_task.value, self.task_delete)
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def toggle_timer(self, e):
        # Toggle the play/pause state
        self.is_timer_on = not self.is_timer_on

        print("Timer is now: ", "On" if self.is_timer_on else "Off")

        # Start or stop the timer thread based on the play/pause state
        if self.is_timer_on and not hasattr(self, 'timer_thread_handle'):
            self.timer_thread_handle = threading.Thread(target=self.timer_thread)
            self.timer_thread_handle.start()

        # Update the button's selected state
        e.control.selected = self.is_timer_on
        e.control.update()

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

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        self.task_delete(self)

def main(page: ft.Page):
    page.title = "ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # create application instance
    todo = TodoApp()

    # add application's root control to the page
    page.add(todo)


ft.app(target=main)