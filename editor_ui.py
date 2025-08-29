# main.py
import flet as ft
from recognition import recognize_text
from audio_recorder import AudioRecorder
from ai_part_new import regeneration

def main(page: ft.Page):
    # page.window.width = 1100
    # page.window.height = 1300
    # page.theme_mode = ft.ThemeMode.LIGHT
    # page.padding = 0
    # page.spacing = 0
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    recorder = AudioRecorder()
    status_text = ft.Text(
        "Нажмите кнопку для начала записи",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLACK
    )
    status_text_row = ft.Row(
        controls=[
            status_text
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    recorder.set_status_callback(lambda msg: update_status(status_text, msg, page))
    pause_button = ft.IconButton(
        icon=ft.Icons.PLAY_ARROW,
        icon_color=ft.Colors.WHITE,
        icon_size=65,
        on_click=lambda e: on_pause_click(e, recorder),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE,
            shape=ft.RoundedRectangleBorder(radius=30)
        ),
    )

    pause_button_container = ft.Container(
        content=pause_button,
        width=100,
        height=100,
        alignment=ft.Alignment(0, 0),
        offset=ft.Offset(0.0, 0.0),
        animate_offset=ft.Animation(
            duration=400,
            curve=ft.AnimationCurve.ELASTIC_OUT
        ),
        visible=True
    )

    record_button = ft.IconButton(
        icon=ft.Icons.CIRCLE,
        on_click=lambda e: on_record_click(e, recorder, pause_button_container, pause_button, status_text, page),
        icon_color=ft.Colors.RED,
        icon_size=100,
        style=ft.ButtonStyle(
            color=ft.Colors.RED,
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=50)
        ),
    ) 
    button_stack = ft.Stack(
        [
            pause_button_container,
            record_button
        ],
        width=250,
        height=120
    )
    buttons_row = ft.Row(
        controls=[button_stack],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    top_button_row = ft.Row(
                controls=[
                    ft.IconButton(icon=ft.Icons.EDIT_SQUARE, height=150, width=150, on_click=lambda e: on_edit_click(page))
                ],
                alignment=ft.MainAxisAlignment.END
            )
    

    # page.add(
    #         top_button_row,
    # )
    markdown_widget = ft.Markdown(
        value="""# This is an H1

## This is an H2

###### This is an H6

Select the valid headers:

- [x] `# hello`
- [ ] `#hello`

## Links

[inline-style](https://www.google.com)""",
        selectable=True,
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        on_tap_link=lambda e: page.launch_url(e.data),
        
    )


    markdown_row = ft.Row(
        controls=[
            ft.Container(
                        ft.Column(
                            [markdown_widget],
                            scroll="hidden",
                        ),
                        expand=True,
                        alignment=ft.alignment.top_left,
                        margin=50,
                        border=ft.border.all(color=ft.Colors.GREY),
                        border_radius=30,
                        padding=20,
                        # bgcolor=ft.Colors.GREY_400, #GREY_400
                    ),
        ],
        alignment=ft.MainAxisAlignment.START, 
        vertical_alignment=ft.CrossAxisAlignment.START, 
        expand=True 
    )

    
    main_column = ft.Column(
        controls=[
            markdown_row, 
            status_text_row,
            buttons_row
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.END,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=20
    )

    return top_button_row, main_column
    # page.add(main_column)

def update_preview(e, page: ft.Page, md):
    md.value = page.controls[1].controls[0].controls[0].controls[0].value
    page.update()


def on_edit_click(page: ft.Page):
    if page.controls[0].controls[0].icon == ft.Icons.EDIT_SQUARE:
        original_text =  page.controls[1].controls[0].controls[0].content.controls[0].value
        md = ft.Markdown(
                    value=original_text,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    on_tap_link=lambda e: page.launch_url(e.data),
                )
        page.controls[1].controls[0].controls[0] = ft.Row(
            controls=[
                ft.TextField(
                value=original_text,
                multiline=True,
                on_change=lambda e: update_preview(e, page, md),
                expand=True,
                border_color=ft.Colors.TRANSPARENT,
                ),
                ft.VerticalDivider(color=ft.Colors.GREY),
                    ft.Container(
                        ft.Column(
                            [md],
                            scroll="hidden",
                        ),
                        expand=True,
                        alignment=ft.alignment.top_left,
                        margin=50,
                        border=ft.border.all(color=ft.Colors.GREY),
                        border_radius=30,
                        padding=20,
                        # bgcolor=ft.Colors.GREY_400,
                    )
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
        page.controls[0].controls[0].icon = ft.Icons.TEXT_SNIPPET
        page.update()
    else:
        edited_text = page.controls[1].controls[0].controls[0].controls[0].value
        md = ft.Markdown(
                value=edited_text,
                selectable=True,
                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                on_tap_link=lambda e: page.launch_url(e.data),
            )
        page.controls[1].controls[0].controls[0] = ft.Container(
                        ft.Column(
                            [md],
                            scroll="hidden",
                        ),
                        expand=True,
                        alignment=ft.alignment.top_left,
                        margin=50,
                        border=ft.border.all(color=ft.Colors.GREY),
                        border_radius=30,
                        padding=20,
                        # bgcolor=ft.Colors.GREY_400,
                    )
        page.controls[0].controls[0].icon = ft.Icons.EDIT_SQUARE
        page.update()

def update_status(status_text: ft.Text, message: str, page: ft.Page):
    status_text.value = message
    if "Ошибка" in message:
        status_text.color = ft.Colors.RED
    elif "Сохранено" in message:
        status_text.color = ft.Colors.GREEN
    elif "Пауза" in message:
        status_text.color = ft.Colors.ORANGE
    else:
        status_text.color = ft.Colors.BLACK
    page.update()


def on_record_click(e, recorder: AudioRecorder, pause_container, pause_button, status_text, page):
    if not recorder.is_recording:
        recorder.start_recording()
        if recorder.is_recording:
            pause_container.offset = ft.Offset(1.2, 0.0)
            pause_container.update()

            pause_button.icon = ft.Icons.PAUSE_ROUNDED
            pause_button.icon_color = ft.Colors.WHITE
            pause_button.style.bgcolor = ft.Colors.RED_700
            pause_button.update()

    else:
        filename = recorder.stop_recording()
        message = f"Сохранено: {filename}."
        update_status(status_text, message, page)

        pause_container.offset = ft.Offset(0.0, 0.0)
        pause_container.update()

        pause_button.icon = ft.Icons.PLAY_ARROW
        pause_button.icon_color = ft.Colors.WHITE
        pause_button.style.bgcolor = ft.Colors.BLUE
        pause_button.update()
        finished_markdown = regeneration(
            recognize_text(
                filename
            )
        )
        page.controls[1].controls[0].controls[0].content.controls[0].value = finished_markdown
        page.update()
        mcontrol = page.controls[1].controls[0].controls[0]
        if type(mcontrol) is ft.Row:
            mcontrol.controls[0].value = finished_markdown
            update_preview(None, page, mcontrol.controls[2].content.controls[0])
        else:
            mcontrol.value = finished_markdown
        page.update()


def on_pause_click(e, recorder: AudioRecorder):
    if recorder.is_recording:
        recorder.toggle_pause()
        if recorder.is_paused:
            e.control.icon = ft.Icons.PLAY_ARROW
            e.control.style.bgcolor = ft.Colors.BLUE
        else:
            e.control.icon = ft.Icons.PAUSE_ROUNDED
            e.control.style.bgcolor = ft.Colors.RED_700
        e.control.update()
    

# ft.app(target=main)