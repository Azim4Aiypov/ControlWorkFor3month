import flet as ft
from db import main_db


def main(page: ft.Page):
    page.title = 'Список покупок'
    page.theme_mode = ft.ThemeMode.DARK
    page.window_maximized = True

    shopping_list = ft.Column(spacing=10)
    bought_count = 0
    filter_type = "all"

    def load_tasks():
        nonlocal bought_count
        shopping_list.controls.clear()
        bought_count = 0
        for task_id, task_text, completed, quantity in main_db.get_tasks(filter_type):
            shopping_list.controls.append(create_task_row(task_id, task_text, completed, quantity))
            if completed:
                bought_count += 1
        page.update()

    def create_task_row(task_id, task_text, completed, quantity):
        task_field = ft.TextField(value=task_text, expand=True, dense=True, read_only=True)
        quantity_field = ft.TextField(value=str(quantity), expand=True, dense=True, read_only=True)
        task_checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        def enable_edit(e):
            task_field.read_only = False
            quantity_field.read_only = False
            page.update()

        def save_edit(e):
            main_db.update_task_db(task_id, task_field.value, quantity_field.value)
            task_field.read_only = True
            quantity_field.read_only = True
            page.update()

        return ft.Row([
            task_checkbox,
            task_field,
            quantity_field,
            ft.IconButton(ft.Icons.EDIT, icon_color=ft.colors.YELLOW_400, on_click=enable_edit),
            ft.IconButton(ft.Icons.SAVE, icon_color=ft.colors.GREEN_400, on_click=save_edit),
            ft.IconButton(ft.Icons.DELETE, icon_color=ft.colors.RED_400, on_click=lambda e: delete_task(task_id))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def add_task(e):
        if task_input.value.strip() and quantity_input.value.strip():
            task_id = main_db.add_task_db(task_input.value, quantity_input.value)
            shopping_list.controls.append(create_task_row(task_id, task_input.value, False, quantity_input.value))
            task_input.value = ""
            quantity_input.value = ""
            page.update()

    def toggle_task(task_id, is_completed):
        main_db.update_task_db(task_id, completed=int(is_completed))
        load_tasks()

    def delete_task(task_id):
        main_db.delete_task_db(task_id)
        load_tasks()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()

    def update_bought_count():
        bought_count_text.value = f"Куплено: {bought_count}"
        page.update()

    task_input = ft.TextField(hint_text='Добавьте товар', expand=True, dense=True, on_submit=add_task)
    quantity_input = ft.TextField(hint_text='Количество', expand=True, dense=True, on_submit=add_task)
    add_button = ft.ElevatedButton("Добавить", on_click=add_task, icon=ft.Icons.ADD)

    filter_button = ft.Row([
        ft.ElevatedButton("Все", on_click=lambda e: set_filter("all")),
        ft.ElevatedButton("Купленные", on_click=lambda e: set_filter("completed")),
        ft.ElevatedButton("Некупленные", on_click=lambda e: set_filter("incomplete"))
    ], alignment=ft.MainAxisAlignment.CENTER)

    bought_count_text = ft.Text(f"Куплено: {bought_count}", size=20)

    content = ft.Container(
        content=ft.Column([
            ft.Row([task_input, quantity_input, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            filter_button,
            bought_count_text,
            shopping_list
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        alignment=ft.alignment.center
    )

    background_image = ft.Image(
        src='/path/to/your/background/image.jpg',
        fit=ft.ImageFit.FILL,
        width=page.width,
        height=page.height
    )

    background = ft.Stack([background_image, content])

    def on_resize(e):
        background_image.width = page.width
        background_image.height = page.height
        page.update()

    page.add(background)
    page.on_resized = on_resize

    load_tasks()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)