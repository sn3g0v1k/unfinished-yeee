import os
import flet as ft
from typing import Dict



def file_system_widgets(page: ft.Page):
    start_path = os.path.expanduser("~")  # можно заменить на любую другую папку
    drawer_width = 260
    collapsed_drawer_width = 0  # ширина, когда drawer скрыт

    # Состояния
    expanded: Dict[str, bool] = {}        # открыт/закрыт для каждой папки
    children_loaded: Dict[str, bool] = {} # подгружались ли дети (lazy load)

    # Контейнеры
    # Левая тонкая колонка с кнопкой свёртывания/развёртывания drawer
    toggle_column = ft.Container(
        width=40,
        padding=4,
        alignment=ft.alignment.center,
    )

    # Собственно drawer (фиксированная ширина, полная высота)
    nav_scroll = ft.Column(
        scroll="auto",
        expand=True,
        height=page.window.height,
    )

    drawer = ft.Container(
        width=drawer_width,
        bgcolor=ft.Colors.BLUE_GREY_900,
        padding=8,
        border_radius=ft.border_radius.only(top_right=8, bottom_right=8),
        content=nav_scroll,
        # делаем его высоту равной высоте окна (и он не сжимается по содержимому)
        height=page.window.height,
    )

    def safe_join(root: str, *parts) -> str:
            """Безопасно соединяем путь, проверяем, что результат внутри root."""
            candidate = os.path.normpath(os.path.join(root, *parts))
            try:
                common = os.path.commonpath([os.path.abspath(root), os.path.abspath(candidate)])
            except Exception:
                return None
            if common != os.path.abspath(root):
                return None
            return candidate

    def list_dir_safe(path: str):
        """Возвращает отсортированный список (папки сначала, затем файлы)."""
        try:
            items = os.listdir(path)
        except PermissionError:
            return []
        dirs = []
        files = []
        for it in sorted(items, key=str.lower):
            full = os.path.join(path, it)
            if os.path.isdir(full):
                dirs.append(it)
            else:
                files.append(it)
        return dirs + files

    # Хелпер для создания виджета строки файла
    def create_file_row(file_path: str, level: int):
        name = os.path.basename(file_path)
        indent = ft.Container(width=12 * level)  # отступ
        def on_click_file(e):
            # Показываем путь и, если это текстовый файл, превью (попробуем открыть безопасно)
            page.get_control("selected_path").value = file_path
            preview = ""
            try:
                # показываем только первые ~40 KiB чтобы не тянуть большие бинарные файлы
                with open(file_path, "rb") as f:
                    data = f.read(40960)
                # попробуем декодировать как utf-8/latin1 — если бинарный, покажем сообщение
                try:
                    text = data.decode("utf-8")
                except Exception:
                    try:
                        text = data.decode("latin-1")
                    except Exception:
                        text = None
                if text is None:
                    preview = "[Бинарный или недекодируемый файл — превью недоступно]"
                else:
                    # Тримим многострочно до 1000 символов
                    preview = text[:2000]
                    if len(text) > 2000:
                        preview += "\n\n... (обрезано)"
            except Exception as ex:
                preview = f"[Не удалось открыть файл: {ex}]"
            page.get_control("file_preview").value = preview
            page.update()

        return ft.Row(
            controls=[
                indent,
                ft.Icon(ft.Icons.DESCRIPTION, size=16),
                ft.TextButton(name, on_click=on_click_file, style=ft.ButtonStyle(color=ft.Colors.WHITE)),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=6,
        )

    # Хелпер для создания виджета папки (с возможностью раскрутки)
    def create_folder_node(folder_path: str, level: int):
        """Возвращает Column: header row + children column (скрываемые)."""
        name = os.path.basename(folder_path.rstrip(os.sep)) or folder_path
        # уникальные объекты для этого узла
        children_column = ft.Column(scroll=None, spacing=0)
        header_chevron = ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20)
        header_text = ft.TextButton(
            name,
            style=ft.ButtonStyle(color=ft.Colors.AMBER),
        )

        indent = ft.Container(width=12 * level)

        # Сборка header row
        header_row = ft.Row(
            controls=[
                indent,
                ft.IconButton(icon=ft.Icons.CHEVRON_RIGHT, icon_size=20),
                ft.Icon(ft.Icons.FOLDER, size=16),
                header_text,
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=6,
        )

        node_column = ft.Column([header_row, children_column], spacing=0)

        # Логика разворачивания
        def toggle(e):
            is_open = expanded.get(folder_path, False)
            if not is_open:
                # открываем
                expanded[folder_path] = True
                header_chevron.icon = ft.Icons.EXPAND_MORE
                # lazy load детей только при первом открытии
                if not children_loaded.get(folder_path, False):
                    children_loaded[folder_path] = True
                    # подгружаем содержимое директории, но только те, что внутри start_path
                    items = list_dir_safe(folder_path)
                    # очищаем на всякий случай
                    children_column.controls.clear()
                    for it in items:
                        candidate = os.path.join(folder_path, it)
                        # safety: candidate должен быть в пределах start_path
                        if os.path.commonpath([os.path.abspath(start_path), os.path.abspath(candidate)]) != os.path.abspath(start_path):
                            # пропускаем (на всякий случай)
                            continue
                        if os.path.isdir(candidate):
                            children_column.controls.append(create_folder_node(candidate, level + 1))
                        else:
                            children_column.controls.append(create_file_row(candidate, level + 1))
                children_column.visible = True
            else:
                # закрываем
                expanded[folder_path] = False
                header_chevron.icon = ft.Icons.CHEVRON_RIGHT
                children_column.visible = False
            page.update()

        # назначаем клики
        header_row.controls[1].on_click = toggle  # иконка
        header_text.on_click = toggle           # текст

        # по умолчанию скрываем детей
        children_column.visible = expanded.get(folder_path, False)
        return node_column

    # Инициализация дерева — только содержимое start_path (не вызываем ".." выше)
    def build_root_tree():
        nav_scroll.controls.clear()
        # Покажем корневую папку как корень (не даём подниматься выше)
        root_node = create_folder_node(start_path, level=0)
        nav_scroll.controls.append(root_node)
        page.update()

    # Переключатель видимости drawer (кнопка слева)
    drawer_visible = {"v": True}

    def toggle_drawer(e):
        drawer_visible["v"] = not drawer_visible["v"]
        drawer.visible = drawer_visible["v"]
        # при скрытом drawer желаем, чтобы не занимал место — тогда можно убрать width,
        # но Flet автоматически убирает видимый контейнер из layout если visible=False.
        # Подстраиваем иконку:
        toggle_column.content = ft.IconButton(
            icon=ft.Icons.MENU if not drawer_visible["v"] else ft.Icons.CHEVRON_LEFT,
            on_click=toggle_drawer
        )
        page.update()

    # Изначальная кнопка
    toggle_column.content = ft.IconButton(icon=ft.Icons.CHEVRON_LEFT, on_click=toggle_drawer)

    # Создадим начальное дерево
    build_root_tree()


    # page.add(layout)
    return toggle_column, drawer