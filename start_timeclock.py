
# time clock based thread
import flet as ft, pytz
from datetime import datetime, date
from time import sleep
from dateutil.tz import gettz
initial = True

def main(page:ft.Page):
    page.title = "Timer App"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "top"
    page.theme_mode = "dark"
    page.padding = 30
    page.window_frameless = False
    page.window_height = 500
    page.window_width = 550

    frdtext = ft.Text(value="Time @ FRD:", size=10, visible=False)
    tztext = ft.Text(size=10, style="displayLarge", visible=False)
    timezone = ft.Dropdown(hint_text="Timezone", width=200, options=[ft.dropdown.Option(x.replace('America/', "").replace('_', ' ')) for x in pytz.country_timezones["us"]], autofocus=True, dense=True)

    def begin_clock(e):
        global initial
        tz = pytz.timezone(("America/" + timezone.value).replace(" ", "_"))
        frdtz = pytz.timezone("America/New_York")
        tztext.value = timezone.value
        play.data = True
        play.visible = False
        pause.visible =True
        timezone.text_size = 10
        timezone.width = (len(tztext.value*8))
        timezone.height = 44

        if initial:
            frdcaptured_time = datetime.time(datetime.now(tz))  # for timer, cannot be changed
            initial = False

        while play.data:
            time.value = datetime.now(tz).strftime('%I:%M %p')  # time pull
            frd_now = datetime.now(frdtz)  # FRD time pull
            frdtext.visible = True
            frdtime.value = frd_now.strftime('%I:%M %p')

            duration = datetime.combine(date.min, datetime.time(frd_now)) - datetime.combine(date.min, frdcaptured_time)
            timeclock.value = str(duration)[0:7:1]

            page.update()
            sleep(1)

            if pytz.timezone(("America/" + timezone.value).replace(" ", "_")) != tz:
                tz = pytz.timezone(("America/" + timezone.value).replace(" ", "_"))
                tztext.value = timezone.value
                timezone.text_size = 10
                timezone.width = (len(tztext.value)*8)
                timezone.height = 44

            else:
                continue

            if pause.data:
                play.data = False
                pause.visible = False
                pause.visible = True

        sleep(1)
        page.update()

    play = ft.IconButton(
        icon=ft.icons.PLAY_CIRCLE_FILLED_OUTLINED, on_click=begin_clock, data=0
    )
    pause = ft.IconButton(
        icon=ft.icons.PAUSE_CIRCLE_FILLED_OUTLINED, on_click=lambda _: pause.data(True), data=0, visible=False
    )

    time = ft.Text(style="displayLarge", color="white", size=10)
    frdtime = ft.Text(style="displaySmall", color="white", size=10)
    timeclock = ft.Text(value="00:00:00", style="displayLarge", color="white", size=50)
    horizontal_space_large = ft.Container()
    horizontal_space_small = ft.Container()
    horizontal_space_large.padding = ft.padding.symmetric(horizontal=40)
    horizontal_space_small.padding = ft.padding.symmetric(horizontal=10)

    page.add(
        ft.Row([frdtext, frdtime, horizontal_space_large, timezone, time], alignment="Center"),
        ft.Container(padding=20),
        ft.Row([horizontal_space_small, timeclock, play, pause], alignment="Center"),
        ft.Container(padding=50),
        ft.Text("Version 0.015b", color="yellow", size=12)
    )

ft.app(target=main, assets_dir="assets")