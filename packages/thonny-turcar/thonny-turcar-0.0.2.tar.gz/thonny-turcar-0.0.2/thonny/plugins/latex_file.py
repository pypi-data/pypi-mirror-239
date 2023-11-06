# -*- coding: utf-8 -*-
import json
import os
import pathlib
import tkinter as tk
from logging import getLogger
from pathlib import PurePath, PurePosixPath, PureWindowsPath
from tkinter import messagebox, ttk
from tkinter.messagebox import askokcancel, showerror
import random
from typing import Dict, Iterable, List, Type

from thonny.utils.SugonUtils import get_enable_url, get_tokens, search_files

from thonny import get_runner, get_shell, get_workbench, ui_utils
from thonny.base_file_browser import (
    HIDDEN_FILES_OPTION,
    BaseLocalFileBrowser,
    BaseRemoteFileBrowser,
    get_file_handler_conf_key,
)
from thonny.common import (
    IGNORED_FILES_AND_DIRS,
    InlineCommand,
    normpath_with_actual_case,
    universal_dirname,
)
from thonny.languages import tr
from thonny.misc_utils import running_on_windows, sizeof_fmt
from thonny.running import InlineCommandDialog, construct_cd_command
from thonny.ui_utils import (open_with_default_app, lookup_style_option)

logger = getLogger(__name__)

minsize = 80

class FilesView1(tk.PanedWindow):
    def __init__(self, master=None):
        tk.PanedWindow.__init__(self, master, orient=tk.HORIZONTAL, borderwidth=0)
        self.remote_added = False

        self.configure(sashwidth=lookup_style_option("Sash", "sashthickness", 4))
        self.configure(background=lookup_style_option("TPanedWindow", "background"))

        get_workbench().bind("BackendTerminated", self.on_backend_terminate, True)
        get_workbench().bind("BackendRestart", self.on_backend_restart, True)
        get_workbench().bind("WorkbenchClose", self.on_workbench_close, True)

        self.local_files = ActiveLocalFileBrowser(self)
        self.local_files.check_update_focus()
        self.show_label = tk.Label(self, text='当前激活项目:')


        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True)
        self.menu = tk.Menu(self.tree, tearoff=False)

        # Define columns for the tree
        self.tree["columns"] = ("name", "extension")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<3>", self.on_secondary_click, True)

        self.add_node()
        self.refresh_button = tk.Button(self, text='刷新', command=self.refresh_hander)
        self.add(self.refresh_button)
        self.add(self.tree)
        self.add(self.show_label)
        # self.remote_files = ActiveRemoteFileBrowser(self)
        # self.reset_remote()

        if os.path.exists('C:\\test\\activeProject.txt'):
            with open('C:\\test\\activeProject.txt', 'r') as f:
                content = f.read()
                if content:
                    self.show_label.config(text='当前激活项目:' + content)

    def refresh_hander(self):
        self.add_node()
    def on_secondary_click(self, event):
        self.menu.delete(0, "end")
        path_name = self.tree.focus().split('-s-')[0]
        res_path = 'C:\latex_project\\' + path_name
        is_exist = self.check_directory_exists(res_path)
        if is_exist:
            if not path_name == '':
                self.menu.add_command(
                    label='新建latex文件', command=lambda: self.request_focus_into(path_name)
                )
        else:
            if not path_name == '' and path_name.endswith('.tex'):
                self.menu.add_command(
                    label='打开文件', command=lambda: self.open_tex(path_name)
                )
            else:
                if os.path.exists('C:\\test\\activeProject.txt'):
                    with open('C:\\test\\activeProject.txt', 'r') as f:
                        content = f.read()
                        if content:
                            self.show_label.config(text='当前激活项目:' + content)
                self.menu.add_command(label='使用电脑默认程序打开', command=lambda:open_with_default_app('C:\latex_project\\'+content +'\\' + path_name))

        self.menu.tk_popup(event.x_root, event.y_root)
    def open_tex(self, path):
        print(self.file_obj)
        file_father = self.find_parent_name(self.file_obj, path)
        get_workbench().get_editor_notebook().show_file('C:\\latex_project\\'+ file_father +'\\'+ path)
    def request_new_focus(self, path):
        # Overridden in active browser
        self.focus_into(path)

    def find_parent_name(self, arr, target_name):
        for item in arr:
            if item['children']:
                for i in item['children']:
                    if i['name'] == target_name:
                        return item['name']
        return None
    def request_focus_into(self, path):
        self.paht_name = path
        self.add_root = tk.Tk()
        ex_w = self.add_root.winfo_screenwidth()
        ex_h = self.add_root.winfo_screenheight()
        self.add_root.geometry("800x800+" + str(int(ex_w / 2) - 400) + "+" + str(int(ex_h / 2) - 400))

        frame = tk.Frame(self.add_root)
        frame.place(rely=0.5, relx=0.5, anchor='center')

        # 创建一个 StringVar 变量并绑定到 Entry 控件上
        self.folder_name_var = tk.StringVar()
        self.folder_name_var.set("请输入latex文件名称，无需.tex:")

        label = tk.Label(frame, text="请输入latex文件名称，无需.tex:")
        label.grid(row=0, column=0, sticky='nsew')

        self.add_entry = tk.Entry(frame, textvariable=self.folder_name_var)
        self.add_entry.grid(row=1, pady=10, padx=10, column=0, sticky='nsew')

        button = tk.Button(frame, text="新建", command=self.add_latex)
        button.grid(row=2, column=0, sticky='nsew')
        self.add_root.mainloop()
    def add_latex(self):
        if not self.add_entry.get():
            return messagebox.showerror('错误', '输入为空，请检查')
        create_paht = 'C:\latex_project\\' + self.paht_name + '\\' + self.add_entry.get() + '.tex'
        file = open(create_paht, 'w')
        # file.write("Hello, World!")
        self.add_node()
        file.close()
        self.add_root.destroy()
    def clear_all(self):
        # 清空树中的所有节点
        self.tree.delete(*self.tree.get_children())

    def on_select(self, e):
        path_name = self.tree.focus().split('-s-')[0]
        res_path = 'C:\latex_project\\' + path_name
        is_exist = self.check_directory_exists(res_path)
        if is_exist:
            if not path_name == '':
                self.show_label.config(text='当前激活项目:' + path_name)
                if not os.path.exists('C:\\test\\activeProject.txt'):
                    open('C:\\test\\activeProject.txt', 'a')
                with open('C:\\test\\activeProject.txt', 'w') as f:
                    f.write(path_name)

    def add_node(self):
        self.clear_all()
        self.file_obj = []
        root_path = r"C:\latex_project"

        if not os.path.exists(root_path):
            os.makedirs(root_path)
        # 获取目录下的所有文件和文件夹
        for item in os.listdir(root_path):
            folder_path = os.path.join(root_path, item)
            if os.path.isdir(folder_path):
                self.file_obj.append({'name': item, 'children': []})
                root_node = self.tree.insert("", "end", text=item, iid=item + '-s-' +str(random.random()))
                for i in os.listdir(folder_path):
                    children_arr = self.file_obj[len(self.file_obj) - 1]['children']
                    children_arr.append({'name': i})
                    self.tree.insert(root_node, 'end', text=i, iid=i + '-s-' +str(random.random()))

    def check_directory_exists(self, directory_path):
        if os.path.isdir(directory_path):
            return True
        else:
            return False


    def insert_files_into_tree(self):
        # 根目录路径
        root_path = r"C:\latex_project"
        # 获取目录下的所有文件和文件夹
        for item in os.listdir(root_path):
            # 获取完整路径
            full_path = os.path.join(root_path, item)
            # 如果是文件夹，则添加到树中
            if os.path.isdir(full_path):
                self.tree.insert("", "end", text=item, open=True)
                # 如果是子文件夹，递归添加到树中
                # for sub_item in os.listdir(full_path):
                    # sub_full_path = os.path.join(full_path, sub_item)
                    # if os.path.isdir(sub_full_path):
                    #     self.tree.insert(item, "end", text=sub_item, open=True)
                    #     # 如果是文件，则添加到对应的文件夹下
            elif os.path.isfile(full_path):
                parent = self.tree.find_children(item)[0]  # 获取父节点id
                self.tree.insert(parent, "end", text=item)

    def toggle_tree(self, event):
        item_id = self.tree.identify_row(event.y)
        print(item_id, 1111)
        if item_id:
            res = self.tree.item(item_id, open=not self.tree.item(item_id, "open"))
            print(res)

    def on_show(self):
        self.reset_remote()
        self.local_files.refresh_tree()

    def reset_remote(self, msg=None):
        runner = get_runner()
        if not runner:
            return

        proxy = runner.get_backend_proxy()
        if not proxy:
            self.hide_remote()
            return

        if proxy.supports_remote_files():
            # remote pane is needed
            if not self.remote_added:
                self.add(self.remote_files, minsize=minsize)
                self.remote_added = True
                self.restore_split()
            self.remote_files.clear()
            self.remote_files.check_update_focus()
        else:
            # remote pane not needed
            self.hide_remote()

    def hide_remote(self):
        if self.remote_added:
            self.save_split()
            self.remove(self.remote_files)
            self.remote_added = False

    def save_split(self):
        _, y = self.sash_coord(0)
        get_workbench().set_option("view.files_split", y)

    def restore_split(self):
        split = get_workbench().get_option("view.files_split", None)
        if split is None:
            if self.winfo_height() > 5:
                split = int(self.winfo_height() * 0.66)
            else:
                split = 600

        self.sash_place(0, 0, split)

    def on_backend_restart(self, event):
        if event.get("full"):
            self.reset_remote(event)

    def on_backend_terminate(self, event):
        self.reset_remote(event)

    def on_workbench_close(self, event=None):
        if self.remote_added:
            self.save_split()

    def get_active_local_dir(self):
        return self.local_files.get_active_directory()

    def get_active_remote_dir(self):
        if self.remote_added:
            return self.remote_files.get_active_directory()
        else:
            return None

    def destroy(self):
        get_workbench().unbind("BackendTerminated", self.on_backend_terminate)
        get_workbench().unbind("BackendRestart", self.on_backend_restart)
        get_workbench().unbind("WorkbenchClose", self.on_workbench_close)
        super().destroy()


class ActiveLocalFileBrowser(BaseLocalFileBrowser):
    def __init__(self, master):
        super().__init__(master)
        get_workbench().bind("ToplevelResponse", self.on_toplevel_response, True)

    def is_active_browser(self):
        return True

    def create_new_file(self):
        path = super().create_new_file()
        if path and path.endswith(".py"):
            get_workbench().get_editor_notebook().show_file(path)

    def get_proposed_new_file_name(self, folder, extension):
        base = "new_file"

        if os.path.exists(os.path.join(folder, base + extension)):
            i = 2

            while True:
                name = base + "_" + str(i) + extension
                path = os.path.join(folder, name)
                if os.path.exists(path):
                    i += 1
                else:
                    return name
        else:
            return base + extension


        proxy = get_runner().get_backend_proxy()
        if (
            proxy
            and proxy.uses_local_filesystem()
            and proxy.get_cwd() != path
            and get_runner().is_waiting_toplevel_command()
        ):
            get_shell().submit_magic_command(construct_cd_command(normpath_with_actual_case(path)))
        else:
            # it's OK, if it's already focused into this directory
            # focus again to refresh
            self.focus_into(path)
            get_workbench().set_local_cwd(path)

    def on_toplevel_response(self, event):
        self.check_update_focus()

    def check_update_focus(self):
        cwd = get_workbench().get_local_cwd()
        if cwd != self.current_focus and os.path.isdir(cwd):
            self.focus_into(cwd)

    def check_add_upload_command(self):
        target_dir = self.master.get_active_remote_dir()
        if target_dir is None:
            return

        proxy = get_runner().get_backend_proxy()

        if not proxy.supports_remote_directories():
            target_dir_desc = proxy.get_node_label()
        else:
            target_dir_desc = target_dir

        def _upload():
            selection = self.get_selection_info(True)
            if not selection:
                return

            if "dir" in selection["kinds"] and not proxy.supports_remote_directories():
                messagebox.showerror(
                    "Can't upload directory",
                    "%s does not support directories.\n" % proxy.get_node_label()
                    + "You can only upload files.",
                    master=self,
                )
            else:
                if upload(selection["paths"], target_dir, master=self):
                    self.master.remote_files.refresh_tree()

        self.menu.add_command(label=tr("Upload to %s") % target_dir_desc, command=_upload)

    def add_first_menu_items(self, context):
        if self.check_for_venv():
            self.menu.add_command(
                label=tr("Activate virtual environment"), command=lambda: self.do_activate_venv()
            )
            self.menu.add_separator()

        super().add_first_menu_items(context)

    def add_middle_menu_items(self, context):
        self.check_add_upload_command()
        super().add_middle_menu_items(context)

    def _get_venv_path(self):
        path = self.get_selected_path()
        if not path:
            return None

        CFGFILE = "pyvenv.cfg"
        fnam = self.get_selected_name()
        try:
            if os.path.exists(path):
                if os.path.isdir(path):
                    cfgfile = os.path.join(path, CFGFILE)
                    if os.path.exists(cfgfile) and os.path.isfile(cfgfile):
                        return path
                else:
                    if fnam == CFGFILE:
                        return os.path.dirname(path)
        except Exception:
            import traceback

            traceback.print_stack()
            logger.exception("_get_venv_path")

    def check_for_venv(self):
        return self._get_venv_path() is not None

    def do_activate_venv(self):
        venv_path = self._get_venv_path()

        if running_on_windows():
            backend_python = os.path.join(venv_path, "Scripts", "python.exe")
        else:
            backend_python = os.path.join(venv_path, "bin", "python3")

        if os.path.isfile(backend_python):
            get_workbench().set_option("run.backend_name", "LocalCPython")
            get_workbench().set_option("LocalCPython.executable", backend_python)

            # just like pressing the button
            get_runner().cmd_stop_restart()
        else:
            messagebox.showerror("Error", f"Could not find {backend_python!r}", master=self)


class ActiveRemoteFileBrowser(BaseRemoteFileBrowser):
    def __init__(self, master):
        super().__init__(master)
        get_workbench().bind("ToplevelResponse", self.on_toplevel_response, True)
        get_workbench().bind("RemoteFilesChanged", self.on_remote_files_changed, True)

    def is_active_browser(self):
        return True

    def supports_new_file(self):
        return True

    def on_toplevel_response(self, msg):
        if not self.winfo_ismapped():
            return
        if get_runner().get_backend_proxy().supports_remote_files():
            # pass cwd, as proxy may not yet know it
            self.check_update_focus(msg.get("cwd"))

    def on_remote_files_changed(self, event=None):
        if not self.winfo_ismapped():
            return

        if get_runner().get_backend_proxy().supports_remote_files():
            self.refresh_tree()

    def check_update_focus(self, new_cwd=None):
        if new_cwd is None:
            proxy = get_runner().get_backend_proxy()
            new_cwd = proxy.get_cwd()

        if self.current_focus != new_cwd:
            self.focus_into(new_cwd)

    def request_new_focus(self, path):
        get_shell().submit_magic_command(["%cd", path if path != "" else "/"])

    def add_download_command(self):
        target_dir = self.master.get_active_local_dir()

        def download():
            selection = self.get_selection_info(True)
            if not selection:
                return

            dlg = DownloadDialog(
                self,
                selection["paths"],
                selection["description"],
                target_dir,
            )
            ui_utils.show_dialog(dlg)
            if dlg.response is not None:
                self.master.local_files.refresh_tree()

        self.menu.add_command(label=tr("Download to %s") % target_dir, command=download)

    def add_middle_menu_items(self, context):
        self.add_download_command()
        super().add_middle_menu_items(context)


class TransferDialog(InlineCommandDialog):
    def _on_response(self, response):
        if response.get("command_id") != self._cmd["id"]:
            return

        if self._stage == "preparation":
            if self._confirm_and_start_main_work(response):
                self._stage = "main_work"
            else:
                self.response = None
                self.report_done(True)

        elif self._stage == "main_work":
            self.response = response
            self.report_done(self._check_success(response))

        self.update_ui()

    def _confirm_and_start_main_work(self, response):
        raise NotImplementedError()

    def _check_success(self, response):
        if response.get("error"):
            self.set_action_text("Error")
            self.append_text("\nError: %s\n" % response["error"])
            return False
        elif response["errors"]:
            self.set_action_text("Error")
            self.append_text("\nError: %s\n" % format_items(response["errors"]))
            return False
        else:
            self.set_action_text("Done!")
            return True


class UploadDialog(TransferDialog):
    def __init__(self, master, paths, target_dir):
        self._stage = "preparation"
        self.items = []
        source_names = []
        for path in paths:
            source_context_dir = os.path.dirname(path)
            for item in prepare_upload_items(path, source_context_dir, target_dir):
                # same path could have been provided directly and also via its parent
                if item not in self.items:
                    self.items.append(item)
                    source_names.append(os.path.basename(item["source_path"]))

        target_paths = [x["target_path"] for x in self.items]
        cmd = InlineCommand(
            "prepare_upload",
            target_paths=target_paths,
            description=get_transfer_description("Uploading", source_names, target_dir),
        )

        super(UploadDialog, self).__init__(master, cmd, "Uploading")

    def _confirm_and_start_main_work(self, preparation_response):
        picked_items = list(
            sorted(
                pick_transfer_items(self.items, preparation_response["existing_items"], self),
                key=lambda x: x["target_path"],
            )
        )
        if picked_items:
            backend_name = get_runner().get_backend_proxy().get_backend_name()
            self._cmd = InlineCommand(
                "upload",
                items=picked_items,
                make_shebang_scripts_executable=get_workbench().get_option(
                    f"{backend_name}.make_uploaded_shebang_scripts_executable"
                ),
            )
            get_runner().send_command(self._cmd)
            return True
        else:
            return False


class DownloadDialog(TransferDialog):
    def __init__(self, master, paths, description, target_dir):
        self._stage = "preparation"
        self._target_dir = target_dir

        cmd = InlineCommand(
            "prepare_download",
            source_paths=paths,
            description=tr("Downloading %s to %s") % (description, target_dir),
        )

        super(DownloadDialog, self).__init__(master, cmd, "Downloading")

    def _prepare_download_items(
        self, all_source_items: Dict[str, Dict], target_dir: str
    ) -> List[Dict]:
        result = []
        for source_path, source_item in all_source_items.items():
            source_context_dir = universal_dirname(source_item["anchor"])
            result.append(
                {
                    "kind": source_item["kind"],
                    "size": source_item["size"],
                    "source_path": source_path,
                    "target_path": transpose_path(
                        source_path, source_context_dir, target_dir, PurePosixPath, pathlib.Path
                    ),
                }
            )
        return result

    def _get_existing_target_items(self, prepared_items: List[Dict]) -> Dict[str, Dict]:
        result = {}

        for item in prepared_items:
            target_path = item["target_path"]
            if os.path.exists(target_path):
                if os.path.isdir(target_path):
                    kind = "dir"
                    size = None
                else:
                    kind = "file"
                    size = os.path.getsize(target_path)

                result[target_path] = {
                    "kind": kind,
                    "size": size,
                }
        return result

    def _confirm_and_start_main_work(self, preparation_response):
        prepared_items = self._prepare_download_items(
            preparation_response["all_items"], self._target_dir
        )
        existing_target_items = self._get_existing_target_items(prepared_items)
        picked_items = pick_transfer_items(prepared_items, existing_target_items, self)
        if picked_items:
            self._cmd = InlineCommand("download", items=picked_items)
            get_runner().send_command(self._cmd)
            return True
        else:
            return False


def transpose_path(
    source_path: str,
    source_dir: str,
    target_dir: str,
    source_path_class: Type[PurePath],
    target_path_class: Type[PurePath],
) -> str:
    assert not source_dir.endswith(":")
    source_path_parts = source_path_class(source_path).parts
    source_dir_parts = source_path_class(source_dir).parts
    assert source_path_parts[: len(source_dir_parts)] == source_dir_parts
    source_suffix_parts = source_path_parts[len(source_dir_parts) :]

    target = target_path_class(target_dir).joinpath(*source_suffix_parts)
    return str(target)


def pick_transfer_items(
    prepared_items: List[Dict], existing_target_items: Dict[str, Dict], master
) -> List[Dict]:
    if not existing_target_items:
        return prepared_items

    errors = []
    overwrites = []

    for item in prepared_items:
        if item["target_path"] in existing_target_items:
            target_info = existing_target_items[item["target_path"]]
            if item["kind"] != target_info["kind"]:
                errors.append(
                    "Can't overwrite '%s' with '%s', because former is a %s but latter is a %s"
                    % (item["target_path"], item["source_path"], target_info["kind"], item["kind"])
                )
            elif item["kind"] == "file":
                size_diff = item["size"] - target_info["size"]
                if size_diff > 0:
                    replacement = "a larger file (%s + %s)" % (
                        sizeof_fmt(target_info["size"]),
                        sizeof_fmt(size_diff),
                    )
                elif size_diff < 0:
                    replacement = "a smaller file (%s - %s)" % (
                        sizeof_fmt(target_info["size"]),
                        sizeof_fmt(-size_diff),
                    )
                else:
                    replacement = "a file of same size (%s)" % sizeof_fmt(target_info["size"])

                overwrites.append("'%s' with %s" % (item["target_path"], replacement))

    if errors:
        showerror("Error", format_items(errors), master=master)
        return []
    elif overwrites:
        if askokcancel(
            "Overwrite?",
            "This operation will overwrite\n\n" + format_items(overwrites),
            master=master,
        ):
            return prepared_items
        else:
            return []
    else:
        return prepared_items


def format_items(items):
    max_count = 10
    if len(items) == 1:
        return items[0]
    msg = "• " + "\n• ".join(items[:max_count])
    if len(items) > max_count:
        msg += "\n ... %d more ..." % (len(items) - max_count)

    return msg


def upload(paths, target_dir, master) -> bool:
    dlg = UploadDialog(master, paths, target_dir)
    ui_utils.show_dialog(dlg)
    return dlg.response is not None


def prepare_upload_items(
    source_path: str, source_context_dir: str, target_dir: str
) -> Iterable[Dict]:
    # assuming target system has Posix paths
    if os.path.isdir(source_path):
        kind = "dir"
        size = None
    else:
        kind = "file"
        size = os.path.getsize(source_path)

    result = [
        {
            "kind": kind,
            "size": size,
            "source_path": source_path,
            "target_path": transpose_path(
                source_path, source_context_dir, target_dir, pathlib.Path, PurePosixPath
            ),
        }
    ]

    if os.path.isdir(source_path):
        for child in os.listdir(source_path):
            if child not in IGNORED_FILES_AND_DIRS:
                result.extend(
                    prepare_upload_items(
                        os.path.join(source_path, child), source_context_dir, target_dir
                    )
                )
    return result


def get_transfer_description(verb, paths, target_dir):
    if len(paths) == 1:
        subject = "'%s'" % paths[0]
    else:
        subject = "%d items" % len(paths)

    return "%s %s to %s" % (verb, subject, target_dir)


def load_plugin() -> None:
    get_workbench().set_default(
        "file.last_browser_folder", normpath_with_actual_case(os.path.expanduser("~"))
    )

    get_workbench().set_default(HIDDEN_FILES_OPTION, False)

    get_workbench().add_view(FilesView1, 'latex项目', "nw")

    for ext in [
        ".py",
        ".pyw",
        ".pyi",
        ".txt",
        ".log",
        ".json",
        ".yml",
        ".yaml",
        ".md",
        ".rst",
        ".toml",
        ".gitignore",
        ".env",
    ]:
        get_workbench().set_default(get_file_handler_conf_key(ext), "thonny")
