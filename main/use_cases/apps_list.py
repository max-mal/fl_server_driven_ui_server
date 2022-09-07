import os
from typing import Dict, List


class AppListUseCase:
    found_icons = []
    found_svg_icons = []

    apps = []

    def _parse_desktop_file(self, file: str) -> dict[str, dict]:
        file_ds = open(file, 'r')
        content = file_ds.read()

        sections = {
            '_': {},
        }
        current_section = '_'

        for line in content.split("\n"):
            sline = line.strip()
            if sline.startswith('['):
                sections[sline] = {}
                current_section = sline
                continue

            if len(sline) == 0:
                continue

            if sline.startswith('#'):
                continue

            parts = sline.split('=')
            if len(parts) < 2:
                parts.append("")
            sections[current_section][parts[0]] = parts[1]

        return sections

    def _get_entry_categories(self, entry: dict) -> List[str]:
        cats = entry.get('Categories', '')
        cats_list = cats.split(';')

        return list(filter(lambda item: len(item) > 0, cats_list))

    def _find_entry_icon(self, icon: str):
        for file in self.found_icons:
            file_parts = os.path.splitext(os.path.basename(file))
            if file_parts[0] == icon:
                return file

        for file in self.found_svg_icons:
            file_parts = os.path.splitext(os.path.basename(file))
            if file_parts[0] == icon:
                return file

        return None

    def scan_images(self):
        paths = [
            "/usr/share/pixmaps",
            "/usr/share/icons",
        ]

        for path in paths:
            self._scan_images(path)

        self.found_icons.sort(reverse=True)

    def _scan_images(self, dir, exclude_extensions = ['.xpm', '.svg']):
        files_list = os.listdir(dir)
        for file in files_list:
            path = f"{dir}/{file}"

            if os.path.isdir(path):
                self._scan_images(path)
                continue
            if not os.path.isfile(path):
                continue

            file_parts = os.path.splitext(file)
            if file_parts[1] not in exclude_extensions:
                self.found_icons.append(path)

            if file_parts[1] == '.svg':
                self.found_svg_icons.append(path)


    def apps_list(self) -> List[Dict]:
        dir = "/usr/share/applications"
        files = os.listdir(dir)
        apps = []

        for file in files:
            path = f"{dir}/{file}"
            if not os.path.isfile(path):
                continue

            parsed = self._parse_desktop_file(path)
            entry = parsed.get('[Desktop Entry]', None)

            if entry is None:
                continue

            if entry.get('NoDisplay', None) == 'true':
                continue

            if entry.get('Hidden', None) == 'true':
                continue

            if entry.get('OnlyShowIn', None) != None:
                continue

            icon = entry.get('Icon', None)
            apps.append({
                'path': path,
                'name': entry.get('Name', ''),
                'icon': icon,
                'icon_path': self._find_entry_icon(icon),
                'exec': entry.get('Exec', ''),
                'comment': entry.get('Comment', None),
                'categories': self._get_entry_categories(entry),
            })

        sorted_apps = sorted(apps, key=lambda item: item['name'])

        return sorted_apps