# -*- coding: utf-8 -*-
import json
import os.path
import re
import sys
import tkinter as tk
from logging import exception, getLogger
from tkinter import filedialog, messagebox, simpledialog, ttk
from tkinter.scrolledtext import ScrolledText
from typing import Optional, Union
from _tkinter import TclError
from thonny.utils.SugonUtils import (
    get_enable_url,
    get_job_cluster,
    get_job_queues,
    get_tokens,
    mkdir,
    search_files,
    submit_job,
    upload_file,
    view_files,
)
from thonny import get_runner, get_workbench, ui_utils
from thonny.base_file_browser import ask_backend_path, choose_node_for_file_operations
from thonny.codeview import BinaryFileException, CodeView, CodeViewText
from thonny.common import (
    REMOTE_PATH_MARKER,
    InlineCommand,
    TextRange,
    ToplevelResponse,
    is_local_path,
    is_remote_path,
    is_same_path,
    normpath_with_actual_case,
    universal_dirname,
)
from thonny.custom_notebook import CustomNotebook, CustomNotebookTab
from thonny.homework_and_exam import homeworkAndExamDialog
from thonny.languages import tr
from thonny.misc_utils import running_on_mac_os, running_on_windows, running_on_linux
from thonny.tktextext import rebind_control_a
from thonny.ui_utils import (
    CommonDialog,
    askopenfilename,
    asksaveasfilename,
    get_beam_cursor,
    select_sequence,
)
# from thonny.video import VideoDialog
from thonny.image import ImageDialog
from thonny.work import WorkDialog

PYTHON_FILES_STR = tr("Python files")
_dialog_filetypes = [(PYTHON_FILES_STR, ".py .pyw .pyi"), (tr("all files"), ".*")]

PYTHON_EXTENSIONS = {"py", "pyw", "pyi"}
PYTHONLIKE_EXTENSIONS = set()

logger = getLogger(__name__)


class EditorCodeViewText(CodeViewText):
    """Allows separate class binding for CodeViewTexts which are inside editors"""

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(
            master=master,
            cnf=cnf,
            **kw,
        )
        self.bindtags(self.bindtags() + ("EditorCodeViewText",))


class Editor(ttk.Frame):
    # self 类本身  master为调用方法的类
    def __init__(self, master):
        # ttk.Frame小部件（widget）基于 Frame 类的一个变体，但使用了 Themed Tkinter（ttk）模块的样式。ttk.Frame 提供了更现代和主题化的外观，与传统的 tkinter
        # 控件相比，它具有更多的样式和定制选项
        ttk.Frame.__init__(self, master)
        assert isinstance(master, EditorNotebook)
        # 调用方法赋值
        self.notebook = master  # type: EditorNotebook

        # parent of codeview will be workbench so that it can be maximized
        # 自定义编辑器
        self._code_view = CodeView(
            get_workbench(),
            propose_remove_line_numbers=True,
            font="EditorFont",
            text_class=EditorCodeViewText,
            cursor=get_beam_cursor(),
        )
        get_workbench().event_generate(
            "EditorTextCreated", editor=self, text_widget=self.get_text_widget()
        )

        self._code_view.grid(row=0, column=0, sticky=tk.NSEW, in_=self)
        self._code_view.home_widget = self  # don't forget home
        self.maximizable_widget = self._code_view

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._filename = None
        self._last_known_mtime = None

        self._code_view.text.bind("<<Modified>>", self._on_text_modified, True)
        self._code_view.text.bind("<<TextChange>>", self._on_text_change, True)
        self._code_view.text.bind("<Control-Tab>", self._control_tab, True)

        get_workbench().bind("DebuggerResponse", self._listen_debugger_progress, True)
        get_workbench().bind("ToplevelResponse", self._listen_for_toplevel_response, True)

        self.update_appearance()

    def get_text_widget(self):
        return self._code_view.text

    def get_code_view(self):
        # TODO: try to get rid of this
        return self._code_view

    def get_content(self) -> str:
        return self._code_view.get_content()

    def set_filename(self, path):
        self._filename = path

    def get_filename(self, try_hard=False):
        if self._filename is None and try_hard:
            self.save_file()

        return self._filename

    def get_identifier(self):
        if self._filename:
            return self._filename
        else:
            return str(self.winfo_id())

    def get_title(self):
        if self.get_filename() is None:
            result = tr("<untitled>")
        elif is_remote_path(self.get_filename()):
            path = extract_target_path(self.get_filename())
            name = path.split("/")[-1]
            result = "[ " + name + " ]"
        else:
            result = os.path.basename(self.get_filename())

        if self.is_modified():
            result += " *"

        return result

    def check_for_external_changes(self):
        if self._filename is None:
            return

        if is_remote_path(self._filename):
            return

        if self._last_known_mtime is None:
            return

        elif not os.path.exists(self._filename):
            self.notebook.select(self)

            if messagebox.askyesno(
                tr("File is gone"),
                tr("Looks like '%s' was deleted or moved.") % self._filename
                + "\n\n"
                + tr("Do you want to also close the editor?"),
                master=self,
            ):
                self.notebook.close_editor(self)
            else:
                self.get_text_widget().edit_modified(True)
                self._last_known_mtime = None

        elif os.path.getmtime(self._filename) != self._last_known_mtime:
            skip_confirmation = not self.is_modified() and get_workbench().get_option(
                "edit.auto_refresh_saved_files"
            )
            if not skip_confirmation:
                self.notebook.select(self)

            if skip_confirmation or messagebox.askyesno(
                tr("External modification"),
                tr("Looks like '%s' was modified outside of the editor.") % self._filename
                + "\n\n"
                + tr(
                    "Do you want to discard current editor content and reload the file from disk?"
                ),
                master=self,
            ):
                prev_location = self.get_text_widget().index("insert")
                self._load_file(self._filename, keep_undo=True)
                try:
                    self.get_text_widget().mark_set("insert", prev_location)
                    self.see_line(int(prev_location.split(".")[0]))
                except Exception:
                    logger.exception("Could not restore previous location")

            self._last_known_mtime = os.path.getmtime(self._filename)

    def get_long_description(self):
        if self._filename is None:
            result = tr("<untitled>")
        else:
            result = self._filename

        try:
            index = self._code_view.text.index("insert")
            if index and "." in index:
                line, col = index.split(".")
                result += "  @  {} : {}".format(line, int(col) + 1)
        except Exception:
            exception("Finding cursor location")

        return result

    def _load_file(self, filename, keep_undo=False):
        try:
            if is_remote_path(filename):
                result = self._load_remote_file(filename)
            else:
                result = self._load_local_file(filename, keep_undo)
                if not result:
                    return False
        except BinaryFileException:
            messagebox.showerror(
                tr("Problem"), tr("%s doesn't look like a text file") % (filename,), master=self
            )
            return False
        except SyntaxError as e:
            assert "encoding" in str(e).lower()
            messagebox.showerror(
                tr("Problem loading file"),
                tr(
                    "This file seems to have problems with encoding.\n\n"
                    "Make sure it is in UTF-8 or contains proper encoding hint."
                ),
                master=self,
            )
            return False

        self.update_appearance()
        return True

    def _load_local_file(self, filename, keep_undo=False):
        with open(filename, "rb") as fp:
            source = fp.read()

        # Make sure Windows filenames have proper format
        filename = normpath_with_actual_case(filename)
        self._filename = filename
        self.update_file_type()
        self._last_known_mtime = os.path.getmtime(self._filename)

        get_workbench().event_generate("Open", editor=self, filename=filename)
        if not self._code_view.set_content_as_bytes(source, keep_undo):
            return False
        self.get_text_widget().edit_modified(False)
        self._code_view.focus_set()
        self.notebook.remember_recent_file(filename)
        return True

    def _load_remote_file(self, filename):
        self._filename = filename
        self.update_file_type()
        self._code_view.set_content("")
        self._code_view.text.set_read_only(True)

        target_filename = extract_target_path(self._filename)

        self.update_title()
        response = get_runner().send_command_and_wait(
            InlineCommand(
                "read_file", path=target_filename, description=tr("Loading %s") % target_filename
            ),
            dialog_title=tr("Loading"),
        )

        if response.get("error"):
            # TODO: make it softer
            raise RuntimeError(response["error"])

        content = response["content_bytes"]
        self._code_view.text.set_read_only(False)
        if not self._code_view.set_content_as_bytes(content):
            return False
        self.get_text_widget().edit_modified(False)
        self.update_title()
        return True

    def is_modified(self):
        return bool(self._code_view.text.edit_modified())

    def save_file_enabled(self):
        return self.is_modified() or not self.get_filename()

    def save_file(self, ask_filename=False, save_copy=False, node=None) -> Optional[str]:
        if self._filename is not None and not ask_filename:
            save_filename = self._filename
            get_workbench().event_generate("Save", editor=self, filename=save_filename)
        else:
            save_filename = self.ask_new_path(node)

            if not save_filename:
                return None

            if self.notebook.get_editor(save_filename) is not None:
                messagebox.showerror(
                    tr("File is open"),
                    tr(
                        "This file is already open in Thonny.\n\n"
                        "If you want to save with this name,\n"
                        "close the existing editor first!"
                    ),
                    master=get_workbench(),
                )
                return None

            get_workbench().event_generate(
                "SaveAs", editor=self, filename=save_filename, save_copy=save_copy
            )

        content_bytes = self._code_view.get_content_as_bytes()

        if is_remote_path(save_filename):
            result = self.write_remote_file(save_filename, content_bytes, save_copy)
        else:
            result = self.write_local_file(save_filename, content_bytes, save_copy)

        if not result:
            return None

        if not save_copy:
            self._filename = save_filename
            self.update_file_type()

        self.update_title()
        return save_filename

    def write_local_file(self, save_filename, content_bytes, save_copy):
        process_shebang = content_bytes.startswith(b"#!/") and get_workbench().get_option(
            "file.make_saved_shebang_scripts_executable"
        )
        if process_shebang:
            content_bytes = content_bytes.replace(b"\r\n", b"\n")

        try:
            f = open(save_filename, mode="wb")
            f.write(content_bytes)
            f.flush()
            # Force writes on disk, see https://learn.adafruit.com/adafruit-circuit-playground-express/creating-and-editing-code#1-use-an-editor-that-writes-out-the-file-completely-when-you-save-it
            os.fsync(f)
            f.close()
            if process_shebang:
                os.chmod(save_filename, 0o755)
            if not save_copy or save_filename == self._filename:
                self._last_known_mtime = os.path.getmtime(save_filename)
            get_workbench().event_generate(
                "LocalFileOperation", path=save_filename, operation="save"
            )
        except PermissionError:
            messagebox.showerror(
                tr("Permission Error"),
                tr("Looks like this file or folder is not writable."),
                master=self,
            )
            return False

        if not save_copy or save_filename == self._filename:
            self.notebook.remember_recent_file(save_filename)

        if not save_copy or save_filename == self._filename:
            self._code_view.text.edit_modified(False)

        return True

    def update_file_type(self):
        if self._filename is None:
            self._code_view.set_file_type(None)
        else:
            ext = self._filename.split(".")[-1].lower()
            if ext in PYTHON_EXTENSIONS:
                file_type = "python"
            elif ext in PYTHONLIKE_EXTENSIONS:
                file_type = "pythonlike"
            else:
                file_type = None

            self._code_view.set_file_type(file_type)

        self.update_appearance()

    def write_remote_file(self, save_filename, content_bytes, save_copy):
        if get_runner().ready_for_remote_file_operations(show_message=True):
            target_filename = extract_target_path(save_filename)

            result = get_runner().send_command_and_wait(
                InlineCommand(
                    "write_file",
                    path=target_filename,
                    content_bytes=content_bytes,
                    editor_id=id(self),
                    blocking=True,
                    description=tr("Saving to %s") % target_filename,
                    make_shebang_scripts_executable=get_workbench().get_option(
                        "file.make_saved_shebang_scripts_executable"
                    ),
                ),
                dialog_title=tr("Saving"),
            )

            if "error" in result:
                messagebox.showerror(tr("Could not save"), str(result["error"]))
                return False

            if not save_copy:
                self._code_view.text.edit_modified(False)

            self.update_title()

            # NB! edit_modified is not falsed yet!
            get_workbench().event_generate(
                "RemoteFileOperation", path=target_filename, operation="save"
            )
            get_workbench().event_generate("RemoteFilesChanged")
            return True
        else:
            messagebox.showerror(tr("Could not save"), tr("Back-end is not ready"))
            return False

    def ask_new_path(self, node=None):
        if node is None:
            node = choose_node_for_file_operations(self.winfo_toplevel(), tr("Where to save to?"))
        if not node:
            return None

        if node == "local":
            return self.ask_new_local_path()
        else:
            assert node == "remote"
            return self.ask_new_remote_path()

    def ask_new_remote_path(self):
        target_path = ask_backend_path(self.winfo_toplevel(), "save")
        if target_path:
            target_path = self._check_add_py_extension(target_path)
            return make_remote_path(target_path)
        else:
            return None

    def ask_new_local_path(self):
        if self._filename is None:
            initialdir = get_workbench().get_local_cwd()
            initialfile = None
        else:
            initialdir = os.path.dirname(self._filename)
            initialfile = os.path.basename(self._filename)

        # https://tcl.tk/man/tcl8.6/TkCmd/getOpenFile.htm
        type_var = tk.StringVar(value="")
        new_filename = asksaveasfilename(
            filetypes=_dialog_filetypes,
            defaultextension=None,
            initialdir=initialdir,
            initialfile=initialfile,
            parent=get_workbench(),
            typevariable=type_var,
        )
        logger.info("Save dialog returned %r with typevariable %r", new_filename, type_var.get())

        # Different tkinter versions may return different values
        if new_filename in ["", (), None]:
            return None

        if running_on_windows():
            # may have /-s instead of \-s and wrong case
            new_filename = os.path.join(
                normpath_with_actual_case(os.path.dirname(new_filename)),
                os.path.basename(new_filename),
            )

        if type_var.get() == PYTHON_FILES_STR or type_var.get() == "":
            new_filename = self._check_add_py_extension(
                new_filename, without_asking=type_var.get() == PYTHON_FILES_STR
            )

        if new_filename.endswith(".py"):
            base = os.path.basename(new_filename)
            mod_name = base[:-3].lower()
            if running_on_windows():
                mod_name = mod_name.lower()

            if mod_name in [
                "math",
                "turtle",
                "random",
                "statistics",
                "pygame",
                "matplotlib",
                "numpy",
            ]:
                # More proper name analysis will be performed by ProgramNamingAnalyzer
                if not tk.messagebox.askyesno(
                    tr("Potential problem"),
                    tr(
                        "If you name your script '%s', "
                        "you won't be able to import the library module named '%s'"
                    )
                    % (base, mod_name)
                    + ".\n\n"
                    + tr("Do you still want to use this name for your script?"),
                    master=self,
                ):
                    return self.ask_new_local_path()

        return new_filename

    def show(self):
        self.notebook.select(self)

    def update_appearance(self):
        self._code_view.set_gutter_visibility(
            get_workbench().get_option("view.show_line_numbers") or get_workbench().in_simple_mode()
        )
        self._code_view.set_line_length_margin(
            get_workbench().get_option("view.recommended_line_length")
        )
        self._code_view.text.update_tabs()
        self._code_view.text.event_generate("<<UpdateAppearance>>")
        self._code_view.grid_main_widgets()

    def _listen_debugger_progress(self, event):
        # Go read-only
        # TODO: check whether this module is active?
        self._code_view.text.set_read_only(True)

    def _listen_for_toplevel_response(self, event: ToplevelResponse) -> None:
        self._code_view.text.set_read_only(False)

    def _control_tab(self, event):
        if event.state & 1:  # shift was pressed
            direction = -1
        else:
            direction = 1
        self.notebook.select_next_prev_editor(direction)
        return "break"

    def _shift_control_tab(self, event):
        self.notebook.select_next_prev_editor(-1)
        return "break"

    def select_range(self, text_range):
        self._code_view.select_range(text_range)

    def select_line(self, lineno, col_offset=None):
        self._code_view.select_range(TextRange(lineno, 0, lineno + 1, 0))
        self.see_line(lineno)

        if col_offset is None:
            col_offset = 0

        self.get_text_widget().mark_set("insert", "%d.%d" % (lineno, col_offset))

    def see_line(self, lineno):
        # first see an earlier line in order to push target line downwards
        self._code_view.text.see("%d.0" % max(lineno - 4, 1))
        self._code_view.text.see("%d.0" % lineno)

    def focus_set(self):
        self._code_view.focus_set()

    def is_focused(self):
        return self.focus_displayof() == self._code_view.text

    def _on_text_modified(self, event):
        self.update_title()

    def update_title(self):
        try:
            self.notebook.update_editor_title(self)
        except Exception as e:
            logger.exception("Could not update editor title", exc_info=e)

    def _on_text_change(self, event):
        self.update_title()

    def destroy(self):
        get_workbench().unbind("DebuggerResponse", self._listen_debugger_progress)
        get_workbench().unbind("ToplevelResponse", self._listen_for_toplevel_response)
        ttk.Frame.destroy(self)
        get_workbench().event_generate(
            "EditorTextDestroyed", editor=self, text_widget=self.get_text_widget()
        )

    def _check_add_py_extension(self, path: str, without_asking: bool = False) -> str:
        assert path
        parts = re.split(r"[/\\]", path)
        name = parts[-1]
        if "." not in name:
            if without_asking or messagebox.askyesno(
                title=tr("Confirmation"),
                message=tr("Python files usually have .py extension.")
                        + "\n\n"
                        + tr("Did you mean '%s'?" % (name + ".py")),
                parent=self.winfo_toplevel(),
            ):
                return path + ".py"
            else:
                return path

        return path


class ACFileDialog(CommonDialog):
    def __init__(self, master):
        super().__init__(master=master)
        self.title("曙光云文件管理")
        self.geometry("800x600")
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.TOP)

        self.back_button = tk.Button(self.button_frame, text="后退", command=self.go_back)
        self.back_button.pack(side=tk.LEFT, anchor=tk.W)

        self.new_button = tk.Button(self.button_frame, text="新建目录", command=self.create_file)
        self.new_button.pack(side=tk.LEFT, padx=5)

        self.upload_button = tk.Button(self.button_frame, text="上传", command=self.upload_file)
        self.upload_button.pack(side=tk.LEFT, padx=5)

        self.upload_button = tk.Button(self.button_frame, text="刷新", command=self.refresh_list)
        self.upload_button.pack(side=tk.LEFT, padx=5)

        self.file_tree = ttk.Treeview(self)
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.file_info_frame = tk.Frame(self)
        self.file_info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.file_info_label = tk.Label(self.file_info_frame, text="文件信息：")
        self.file_info_label.pack()

        self.open_button = tk.Button(self.file_info_frame, text="打开", command=self.open_file)
        self.open_button.configure(state=tk.DISABLED)
        self.open_button.pack()

        closed_folder = os.path.join(os.path.dirname(__file__), "res", "closed-folder.gif")
        self.folder_close_icon = tk.PhotoImage(file=closed_folder)
        self.data = None
        self.default_text = None
        self.file_name = None
        self.current_path = None
        self.parent_path = None
        self.load_files()

    def load_files(self, folder_path=None):
        print(folder_path)
        self.file_tree.delete(*self.file_tree.get_children())
        token = get_tokens("acsx6nwsm6", "yubo@liuzhongxiu")
        enable_url = get_enable_url(token, "efileUrls")
        search_file = search_files(token, enable_url, 10, 0, None, folder_path)
        self.data = json.loads(search_file)
        self.current_path = self.data["data"]["path"]
        file_list = self.data["data"]["fileList"]
        children_list = self.data["data"]["children"]
        for child in children_list:
            self.file_tree.insert(
                "", tk.END, text=f" {child['label']}", values=child, image=self.folder_close_icon
            )
        for file in file_list:
            self.file_tree.insert("", tk.END, text=file["name"], values=file)

        self.file_tree.bind("<<TreeviewSelect>>", self.show_file_info)

    def show_file_info(self, event):
        selected_item = self.file_tree.focus()
        file_info_text = ""
        file = self.file_tree.item(selected_item)
        if file["image"]:
            if file["image"][0].startswith("pyimage1"):
                path = (
                    file["values"][0].split("'path': ")[1].split(",")[0].strip("'")
                )  # 使用字符串分割提取路径,去除路径中的引号
                file_info_text += f"文件夹名: {file['text']}\n"
                file_info_text += f"文件路径: {path}\n"
                self.open_button.configure(state=tk.NORMAL)
        else:
            file_info_text += f"文件夹名: {file['text']}\n"
            print(file["values"])
            path = (
                file["values"][0].split("'path': ")[1].split(",")[0].strip("'")
            )  # 使用字符串分割提取路径,去除路径中的引号
            file_info_text += f"文件路径: {path}\n"
            owner = file["values"][0].split("'owner': ")[1].split(",")[0].strip("'")
            file_info_text += f"创建者: {owner}\n"
            size = file["values"][0].split("'size': ")[1].split(",")[0].strip("'")
            file_info_text += f"文件大小: {size} bytes\n"
            lastModifiedTime = (
                file["values"][0].split("'lastModifiedTime': ")[1].split(",")[0].strip("'")
            )
            file_info_text += f"最后修改时间: {lastModifiedTime}"

            self.open_button.configure(state=tk.NORMAL)
            # self.open_button.configure(state=tk.DISABLED)

        self.file_info_label.configure(text=file_info_text)

    def open_file(self):
        selected_item = self.file_tree.focus()
        file = self.file_tree.item(selected_item)
        path = file["values"][0].split("'path': ")[1].split(",")[0].strip("'")
        if file["image"]:
            print(f"打开文件夹路径: {path}")
            self.parent_path = self.current_path
            self.load_files(folder_path=path)
        else:
            print(f"打开文件路径: {path}")
            token = get_tokens("acsx6nwsm6", "yubo@liuzhongxiu")
            enable_url = get_enable_url(token, "hpcUrls")
            file_content = view_files(token, enable_url, path)
            file_content_o = json.loads(file_content)
            print(file_content_o)
            if file_content_o["code"] == "0":
                if file_content_o["data"]["success"] == "true":
                    self.file_name = file["text"]
                    self.default_text = file_content_o["data"]["data"]
                    print(f"文本内容: {self.default_text}")
                    editor_window = tk.Toplevel(self)
                    text_area = ScrolledText(editor_window, wrap=tk.WORD)
                    text_area.insert("1.0", self.default_text)
                    text_area.pack(fill=tk.BOTH, expand=True)

                    def save_on_ctrl_s():
                        text_content = text_area.get("1.0", tk.END)
                        print(text_content)
                        try:
                            with open(self.file_name, "w") as f:
                                f.write(text_content)
                            efile_url = get_enable_url(token, "efileUrls")
                            print(os.path.dirname(path))
                            upload_file(
                                token, efile_url, os.path.dirname(path), "cover", self.file_name
                            )
                            self.default_text = text_content
                            tk.messagebox.showinfo("保存成功", "文本保存成功。")
                            editor_window.destroy()
                        except Exception as e:
                            tk.messagebox.showerror("保存失败", f"保存文本时出错: {str(e)}")

                        # 使用完毕后删除临时文件
                        try:
                            os.remove(self.file_name)
                        except Exception as e:
                            print(f"Failed to delete the temporary file: {str(e)}")

                    editor_window.bind("<Control-s>", save_on_ctrl_s)

                    save_button = tk.Button(editor_window, text="保存", command=save_on_ctrl_s)
                    save_button.pack()

                    def on_close():
                        current_text = text_area.get("1.0", tk.END).strip()
                        if current_text != self.default_text:
                            result = messagebox.askyesnocancel("关闭文本", "是否要在关闭前保存更改？")
                            if result is True:
                                save_on_ctrl_s()
                                editor_window.destroy()
                            elif result is False:
                                editor_window.destroy()
                        else:
                            editor_window.destroy()

                    editor_window.protocol("WM_DELETE_WINDOW", on_close)
                else:
                    # 显示提示信息
                    self.open_button.configure(state=tk.DISABLED)
                    messagebox.showinfo("提示", f"目前仅支持文本文件打开查看")

            else:
                # 显示提示信息
                messagebox.showinfo("提示", f"远程连接失败")

    def go_back(self):
        # 执行返回操作
        # 调用接口或编写逻辑以实现后退功能
        print("Go Back")
        self.load_files(folder_path=self.parent_path)

    def create_file(self):
        # 执行新建文件操作
        # 调用接口或编写逻辑以实现新建文件功能
        print("Create File")
        file_name = simpledialog.askstring("新建目录", "请输入文件名")
        if file_name:
            # 调用接口或编写逻辑以实现创建文件功能
            print(f"Creating File: {file_name}")
            print(f"current_path: {self.current_path}")
            token = get_tokens("acsx6nwsm6", "yubo@liuzhongxiu")
            enable_url = get_enable_url(token, "efileUrls")
            mkdir(token, enable_url, self.current_path + "/" + file_name, "false")
            # 显示提示信息
            messagebox.showinfo("提示", f"创建文件 {file_name} 完成")

    def refresh_list(self):
        # 执行刷新文件列表操作
        # 调用接口或编写逻辑以实现新建文件功能
        print("Refresh List")
        self.load_files(folder_path=self.current_path)

    def upload_file(self):
        # 执行上传文件操作
        # 调用接口或编写逻辑以实现上传文件功能
        print("Upload File")
        file_path = filedialog.askopenfilename()
        if file_path:
            # 调用接口或编写逻辑以实现上传文件功能
            print(f"Uploading File: {file_path}")
            token = get_tokens("acsx6nwsm6", "yubo@liuzhongxiu")
            enable_url = get_enable_url(token, "efileUrls")
            upload_file(token, enable_url, self.current_path, "uncover", file_path)


class JobSubmitDialog(CommonDialog):
    def __init__(self, master):
        super().__init__(master=master)

        self.title("提交作业")
        self.geometry("400x600")

        self.create_widgets()

    def create_widgets(self):
        # 创建下拉选择框
        label_submission = tk.Label(self, text="提交方式:")
        label_submission.pack()
        self.combo_submission = ttk.Combobox(self, values=["命令行方式"])
        self.combo_submission.pack()
        default_value = "命令行方式"
        self.combo_submission.current(self.combo_submission["values"].index(default_value))

        # 创建标签和输入框
        label_name = tk.Label(self, text="作业名称:")
        label_name.pack()
        self.entry_name = tk.Entry(self)
        self.entry_name.pack()

        # 创建选择文件目录按钮
        label_directory = tk.Label(self, text="工作目录:")
        label_directory.pack()
        self.entry_directory = tk.Entry(self)
        self.entry_directory.pack()
        # button_select_directory = tk.Button(self, text="选择文件目录", command=self.select_directory)
        # button_select_directory.pack()

        # 创建命令行方式的文本输入框
        label_command = tk.Label(self, text="命令行方式:")
        label_command.pack()
        self.text_command = tk.Text(self, height=10)
        self.text_command.pack()
        default_text = "sleep 5"
        self.text_command.insert("1.0", default_text)

        # 创建提交按钮
        button_submit = tk.Button(self, text="提交", command=self.submit_homework)
        button_submit.pack()

    def submit_homework(self):
        # 获取下拉选择框的值
        submission_method = self.combo_submission.get()

        # 获取文本输入框的值
        job_name = self.entry_name.get()
        working_directory = self.entry_directory.get()
        command_line = self.text_command.get("1.0", tk.END)

        # 打印提交的作业信息
        print("提交方式:", submission_method)
        print("作业名称:", job_name)
        print("工作目录:", working_directory)

        if submission_method == "命令行方式":
            print("命令行:", command_line)
            if not command_line.strip():
                # command_line为空
                messagebox.showerror(
                    "提交作业",
                    "命令行脚本不能为空\n\n",
                    master=get_workbench(),
                )
            else:
                if command_line:
                    # 在这里可以将作业提交到服务器或进行其他处理
                    # todo 曙光账号来源
                    token = get_tokens("acsx6nwsm6", "yubo@liuzhongxiu")
                    enable_url = get_enable_url(token, "hpcUrls")
                    job_cluster = get_job_cluster(token, enable_url)
                    job_queues = get_job_queues(token, enable_url, "acsx6nwsm6", job_cluster)
                    job_info = submit_job(
                        token,
                        enable_url,
                        job_cluster,
                        job_queues,
                        command_line,
                        job_name,
                        working_directory,
                    )
                    print("提交请求:", job_info)
                    # 提交成功提示窗口
                    messagebox.showinfo("提交成功", "作业已成功提交！\n" + job_info)
                    # 关闭弹出框
                    self.destroy()

    def select_directory(self):
        # 弹出选择文件夹对话框
        directory = filedialog.askdirectory()
        # 将选择的文件夹路径显示在输入框中
        self.entry_directory.delete(0, tk.END)
        self.entry_directory.insert(tk.END, directory)


class EditorNotebook(CustomNotebook):
    """
    Manages opened files / modules
    """

    def __init__(self, master):
        super().__init__(master)

        get_workbench().set_default("file.reopen_all_files", False)
        get_workbench().set_default("file.open_files", [])
        get_workbench().set_default("file.current_file", None)
        get_workbench().set_default("file.recent_files", [])
        get_workbench().set_default("view.highlight_current_line", False)
        get_workbench().set_default("view.show_line_numbers", True)
        get_workbench().set_default("view.recommended_line_length", 0)
        get_workbench().set_default("edit.indent_with_tabs", False)
        get_workbench().set_default("edit.auto_refresh_saved_files", True)
        get_workbench().set_default("file.make_saved_shebang_scripts_executable", True)

        self._recent_menu = tk.Menu(
            get_workbench().get_menu("file"), postcommand=self._update_recent_menu
        )
        self._init_commands()
        self.enable_traversal()

        # open files from last session
        """ TODO: they should go only to recent files
        for filename in prefs["open_files"].split(";"):
            if os.path.exists(filename):
                self._open_file(filename)
        """

        # should be in the end, so that it can be detected when
        # constructor hasn't completed yet
        self.preferred_size_in_pw = None
        self._checking_external_changes = False

        get_workbench().bind("WindowFocusIn", self.check_for_external_changes, True)
        get_workbench().bind("ToplevelResponse", self.check_for_external_changes, True)
        self.bind("<<NotebookTabChanged>>", self.on_tab_changed, True)

    def on_tab_changed(self, *args):
        # Required to avoid incorrect sizing of parent panes
        self.update_idletasks()

    def _init_commands(self):
        # TODO: do these commands have to be in EditorNotebook ??
        # Create a module level function install_editor_notebook ??
        # Maybe add them separately, when notebook has been installed ??

        get_workbench().add_command(
            "new_file",
            "file",
            tr("New"),
            self._cmd_new_file,
            caption=tr("New"),
            default_sequence=select_sequence("<Control-n>", "<Command-n>"),
            extra_sequences=["<Control-Greek_nu>"],
            group=10,
            image="new-file",
            include_in_toolbar=True,
        )

        get_workbench().add_command(
            "watch_video",
            "course",
            tr("课程视频"),
            self._cmd_watch_video,
            caption=tr("Video"),
            group=10,
            image="video",
            include_in_toolbar=True,
        )

        get_workbench().add_command(
            "homework_and_exam",
            "course",
            "课程作业",
            self._cmd_homework_and_exam,
            caption=tr("Homework And Exam"),
            default_sequence=select_sequence("<Control-j>", "<Command-j>"),
            extra_sequences=["<Control-Greek_nu>"],
            group=10,
            image="homework 16x16",
            include_in_toolbar=True,
        )

        get_workbench().add_command(
            "job_submit",
            "AC",
            tr("曙光-文件提交"),
            self._cmd_job_submit,
            caption=tr("AC"),
            group=10,
            image="ac-submit",
            include_in_toolbar=True,
        )

        get_workbench().add_command(
            "ac_file",
            "AC",
            tr("曙光-文件管理"),
            self._cmd_ac_file,
            caption=tr("ac_file_manage"),
            group=10,
            image="ac-manager",
            include_in_toolbar=True,
        )

        get_workbench().add_command(
            "watch_work",
            "AC",
            "曙光-作业",
            self._cmd_watch_work,
            caption="ac_homework",
            group=10,
            image="ac-homework",
            include_in_toolbar=True,
        )

        get_workbench().add_command(
            "image_manage",
            "image",
            "image_manage",
            self._cmd_image_manage,
            caption="image_manage",
            group=10,
            image="ac-homework",
            include_in_toolbar=True,
        )

        get_workbench().add_command(
            "recents", "file", tr("Recent files"), group=10, submenu=self._recent_menu
        )

        # http://stackoverflow.com/questions/22907200/remap-default-keybinding-in-tkinter
        get_workbench().bind_class("Text", "<Control-o>", self._control_o)
        get_workbench().bind_class("Text", "<Control-Greek_omicron>", self._control_o)
        rebind_control_a(get_workbench())

        get_workbench().add_command(
            "close_file",
            "file",
            tr("Close"),
            self._cmd_close_file,
            default_sequence=select_sequence("<Control-w>", "<Command-w>"),
            extra_sequences=["<Control-Greek_finalsmallsigma>"],
            tester=lambda: self.get_current_editor() is not None,
            group=10,
        )

        get_workbench().add_command(
            "close_files",
            "file",
            tr("Close all"),
            self.close_tabs,
            tester=lambda: self.get_current_editor() is not None,
            default_sequence=select_sequence("<Control-W>", "<Command-Alt-w>"),
            group=10,
        )

        get_workbench().add_command(
            "save_file",
            "file",
            tr("Save"),
            self._cmd_save_file,
            caption=tr("Save"),
            default_sequence=select_sequence("<Control-s>", "<Command-s>"),
            extra_sequences=["<Control-Greek_sigma>"],
            tester=self._cmd_save_file_enabled,
            group=10,
            image="save-file",
            include_in_toolbar=True,
        )

        get_workbench().add_command(
            "save_all_files",
            "file",
            tr("Save All files"),
            self._cmd_save_all_files,
            caption=tr("Save All files"),
            default_sequence=select_sequence("<Control-Alt-s>", "<Command-Alt-s>"),
            tester=self._cmd_save_all_files_enabled,
            group=10,
        )

        get_workbench().add_command(
            "save_file_as",
            "file",
            tr("Save as..."),
            self._cmd_save_file_as,
            default_sequence=select_sequence("<Control-Shift-S>", "<Command-Shift-S>"),
            extra_sequences=["<Control-Greek_SIGMA>"],
            tester=lambda: self.get_current_editor() is not None,
            group=10,
        )

        get_workbench().add_command(
            "save_copy",
            "file",
            tr("Save copy..."),
            self._cmd_save_copy,
            tester=lambda: self.get_current_editor() is not None,
            group=10,
        )

        get_workbench().add_command(
            "move_rename_file",
            "file",
            tr("Move / rename..."),
            self._cmd_move_rename_file,
            tester=self._cmd_move_rename_file_enabled,
            group=10,
        )

        get_workbench().add_command(
            "goto_source_line",
            "edit",
            tr("Go to line..."),
            self._cmd_goto_source_line,
            default_sequence=select_sequence("<Control-g>", "<Command-g>"),
            # tester=,
            # no global switch, or cross plugin switch?
            # todo use same as find and replace -> plugins/find_replace.py
            group=60,
        )

        get_workbench().createcommand("::tk::mac::OpenDocument", self._mac_open_document)

    def _cmd_homework_and_exam(self):
        ui_utils.show_dialog(homeworkAndExamDialog(get_workbench()))

    def load_startup_files(self):
        """
        这行代码是一个列表推导式，用于获取命令行参数中存在的文件的绝对路径。

        让我们逐个解析这段代码：

        sys.argv[1:]：sys.argv 是一个包含命令行参数的列表，其中第一个元素是脚本的名称，后续元素是传递给脚本的参数。sys.argv[1:] 表示从第二个参数开始（即索引为 1 的元素）直到最后一个参数，切片出来的部分由 : 表示。

        os.path.exists(name)：os.path.exists() 是一个函数，用于检查给定路径是否存在。在这里，name 是指从命令行参数中取得的每个文件名。

        os.path.abspath(name)：os.path.abspath() 是一个函数，用于获取给定路径的绝对路径。在这里，name 是每个存在的文件名。

        for name in sys.argv[1:] if os.path.exists(name)：这是一个列表推导式的语法结构。它遍历 sys.argv[1:] 中的每个参数，但只有当 os.path.exists(name) 返回 True（即文件存在）时才会执行后续操作。

        因此，这段代码的作用是对于命令行参数中存在的每个文件名，获取其绝对路径，并将这些绝对路径以列表的形式输出。换句话说，它过滤出命令行参数中真实存在的文件，并返回这些文件的绝对路径列表。

        """
        """If no filename was sent from command line
        then load previous files (if setting allows)"""

        cmd_line_filenames = [
            os.path.abspath(name) for name in sys.argv[1:] if os.path.exists(name)
        ]

        if len(cmd_line_filenames) > 0:
            filenames = cmd_line_filenames
        elif get_workbench().get_option("file.reopen_all_files"):
            filenames = get_workbench().get_option("file.open_files")
        elif get_workbench().get_option("file.current_file"):
            filenames = [get_workbench().get_option("file.current_file")]
        else:
            filenames = []

        if len(filenames) > 0:
            for filename in filenames:
                if os.path.exists(filename):
                    self.show_file(filename)

            cur_file = get_workbench().get_option("file.current_file")
            # choose correct active file
            if len(cmd_line_filenames) > 0:
                self.show_file(cmd_line_filenames[0])
            elif cur_file and os.path.exists(cur_file):
                self.show_file(cur_file)
            else:
                self._cmd_new_file()
        else:
            self._cmd_new_file()

    def save_all_named_editors(self):
        all_saved = True
        for editor in self.winfo_children():
            if editor.get_filename() and editor.is_modified():
                success = editor.save_file()
                all_saved = all_saved and success

        return all_saved

    def remember_recent_file(self, filename):
        recents = get_workbench().get_option("file.recent_files")
        if filename in recents:
            recents.remove(filename)
        recents.insert(0, filename)
        relevant_recents = [name for name in recents if os.path.exists(name)][:15]
        get_workbench().set_option("file.recent_files", relevant_recents)
        self._update_recent_menu()

    def _update_recent_menu(self):
        recents = get_workbench().get_option("file.recent_files")
        relevant_recents = [
            path for path in recents if os.path.exists(path) and not self.file_is_opened(path)
        ]
        self._recent_menu.delete(0, "end")
        for path in relevant_recents:
            def load(path=path):
                self.show_file(path)

            self._recent_menu.insert_command("end", label=path, command=load)

    def remember_open_files(self):
        if (
            self.get_current_editor() is not None
            and self.get_current_editor().get_filename() is not None
        ):
            current_file = self.get_current_editor().get_filename()
        else:
            current_file = None

        get_workbench().set_option("file.current_file", current_file)

        open_files = [
            editor.get_filename() for editor in self.winfo_children() if editor.get_filename()
        ]
        get_workbench().set_option("file.open_files", open_files)

    def _cmd_image_manage(self):
        ui_utils.show_dialog(ImageDialog(get_workbench()))

    # 获取视频
    def _cmd_watch_video(self):
        ui_utils.show_dialog(VideoDialog(get_workbench()))

    def _cmd_watch_work(self):
        ui_utils.show_dialog(WorkDialog(get_workbench()))

    def _cmd_job_submit(self):
        ui_utils.show_dialog(JobSubmitDialog(get_workbench()))

    def _cmd_ac_file(self):
        ui_utils.show_dialog(ACFileDialog(get_workbench()))

    def _cmd_new_file(self):
        self.open_new_file()

    def open_new_file(self, path=None, remote=False):
        new_editor = Editor(self)
        get_workbench().event_generate("NewFile", editor=new_editor)
        if path:
            if remote:
                new_editor.set_filename(make_remote_path(path))
            else:
                new_editor.set_filename(path)
        self.add(new_editor, text=new_editor.get_title())
        self.select(new_editor)
        new_editor.focus_set()

    def _cmd_open_file(self):
        node = choose_node_for_file_operations(self.winfo_toplevel(), "Where to open from?")
        if not node:
            return

        if node == "local":
            initialdir = get_workbench().get_local_cwd()
            if (
                self.get_current_editor() is not None
                and self.get_current_editor().get_filename() is not None
            ):
                initialdir = os.path.dirname(self.get_current_editor().get_filename())
            path = askopenfilename(
                filetypes=_dialog_filetypes, initialdir=initialdir, parent=get_workbench()
            )
        else:
            assert node == "remote"
            target_path = ask_backend_path(self.winfo_toplevel(), "open")
            if not target_path:
                return

            path = make_remote_path(target_path)

        if path:
            # self.close_single_untitled_unmodified_editor()
            self.show_file(path, propose_dialog=False)

    def _control_o(self, event):
        # http://stackoverflow.com/questions/22907200/remap-default-keybinding-in-tkinter
        self._cmd_open_file()
        return "break"

    def _close_files(self, except_index=None):
        for tab_index in reversed(range(len(self.winfo_children()))):
            if except_index is not None and tab_index == except_index:
                continue
            else:
                editor = self.get_child_by_index(tab_index)
                if self.check_allow_closing(editor):
                    self.forget(editor)
                    editor.destroy()

    def _cmd_close_file(self):
        self.close_tab(self.index(self.select()))

    def close_tab(self, index_or_tab: Union[int, CustomNotebookTab]):
        if isinstance(index_or_tab, int):
            page = self.pages[index_or_tab]
        else:
            page = self.get_page_by_tab(index_or_tab)

        assert isinstance(page.content, Editor)
        self.close_editor(page.content)

    def close_editor(self, editor, force=False):
        if not force and not self.check_allow_closing(editor):
            return
        self.forget(editor)
        editor.destroy()

    def _cmd_save_file(self):
        if self.get_current_editor():
            self.get_current_editor().save_file()
            self.update_editor_title(self.get_current_editor())

    def _cmd_save_file_enabled(self):
        return self.get_current_editor() and self.get_current_editor().save_file_enabled()

    def _cmd_save_all_files(self):
        for editor in self.get_all_editors():
            if editor.save_file_enabled() == True:
                editor.save_file()
                self.update_editor_title(editor)

    def _cmd_save_all_files_enabled(self):
        for editor in self.get_all_editors():
            if editor.save_file_enabled() == True:
                return True
        return False

    def _cmd_save_file_as(self, node=None):
        if not self.get_current_editor():
            return

        self.get_current_editor().save_file(ask_filename=True, node=node)
        self.update_editor_title(self.get_current_editor())
        get_workbench().update_title()

    def _cmd_save_copy(self):
        if not self.get_current_editor():
            return

        self.get_current_editor().save_file(ask_filename=True, save_copy=True)
        self.update_editor_title(self.get_current_editor())

    def _cmd_save_file_as_enabled(self):
        return self.get_current_editor() is not None

    def _cmd_move_rename_file(self):
        editor = self.get_current_editor()
        old_filename = editor.get_filename()
        assert old_filename is not None

        if is_remote_path(old_filename):
            node = "remote"
        else:
            node = "local"

        self._cmd_save_file_as(node=node)

        if editor.get_filename() != old_filename:
            if is_remote_path(old_filename):
                remote_path = extract_target_path(old_filename)
                get_runner().send_command_and_wait(
                    InlineCommand(
                        "delete", paths=[remote_path], description=tr("Deleting" + remote_path)
                    ),
                    dialog_title=tr("Deleting"),
                )
                get_workbench().event_generate(
                    "RemoteFileOperation", path=remote_path, operation="delete"
                )
            else:
                os.remove(old_filename)
                get_workbench().event_generate(
                    "LocalFileOperation", path=old_filename, operation="delete"
                )

    def _cmd_move_rename_file_enabled(self):
        return self.get_current_editor() and self.get_current_editor().get_filename() is not None

    def close_single_untitled_unmodified_editor(self):
        editors = self.winfo_children()
        if len(editors) == 1 and not editors[0].is_modified() and not editors[0].get_filename():
            self._cmd_close_file()

    def _cmd_goto_source_line(self):
        editor = self.get_current_editor()
        if editor:
            line_no = simpledialog.askinteger(tr("Go to line"), tr("Line number"))
            if line_no:
                editor.select_line(line_no)

    def _mac_open_document(self, *args):
        for arg in args:
            if isinstance(arg, str) and os.path.exists(arg):
                self.show_file(arg)
        get_workbench().become_active_window()

    def get_current_editor(self) -> Optional[Editor]:
        return self.get_current_child()

    def get_current_editor_content(self):
        editor = self.get_current_editor()
        if editor is None:
            return None
        else:
            return editor.get_content()

    def get_all_editors(self):
        # When workspace is closing, self.winfo_children()
        # may return an unexplainable tkinter.Frame
        return [child for child in self.winfo_children() if isinstance(child, Editor)]

    def select_next_prev_editor(self, direction):
        cur_index = self.index(self.select())
        next_index = (cur_index + direction) % len(self.tabs())
        self.select(self.get_child_by_index(next_index))

    def file_is_opened(self, path):
        for editor in self.get_all_editors():
            if editor.get_filename() and is_same_path(path, editor.get_filename()):
                return True

        return False

    def show_file(self, filename, text_range=None, set_focus=True, propose_dialog=True):
        # self.close_single_untitled_unmodified_editor()
        try:
            editor = self.get_editor(filename, True)
        except PermissionError:
            logger.exception("Loading " + filename)
            msg = tr("Got permission error when trying to load\n%s") % (filename,)
            if running_on_mac_os() and propose_dialog:
                msg += "\n\n" + tr("Try opening it with File => Open.")

            messagebox.showerror(tr("Permission error"), msg, master=self)
            return None

        if editor is None:
            return

        self.select(editor)
        if set_focus:
            editor.focus_set()

        if text_range is not None:
            editor.select_range(text_range)

        return editor

    def show_remote_file(self, target_filename):
        if not get_runner().ready_for_remote_file_operations(show_message=True):
            return None
        else:
            return self.show_file(make_remote_path(target_filename))

    def show_file_at_line(self, filename, lineno, col_offset=None):
        editor = self.show_file(filename)
        editor.select_line(lineno, col_offset)

    def update_appearance(self):
        for editor in self.winfo_children():
            editor.update_appearance()

    def update_editor_title(self, editor, title=None):
        if title is None:
            title = editor.get_title()
        try:
            self.tab(editor, text=title)
        except TclError:
            pass

        try:
            self.indicate_modification()
        except Exception:
            logger.exception("Could not update modification indication")

    def indicate_modification(self):
        if not running_on_mac_os():
            return

        atts = self.winfo_toplevel().wm_attributes()
        if "-modified" in atts:
            i = atts.index("-modified")
            mod = atts[i: i + 2]
            rest = atts[:i] + atts[i + 2:]
        else:
            mod = ()
            rest = atts

        for editor in self.get_all_editors():
            if editor.is_modified():
                if mod != ("-modified", 1):
                    self.winfo_toplevel().wm_attributes(*(rest + ("-modified", 1)))
                break
        else:
            if mod == ("-modified", 1):
                self.winfo_toplevel().wm_attributes(*(rest + ("-modified", 0)))

    def _open_file(self, filename):
        editor = Editor(self)
        if editor._load_file(filename):
            self.add(editor, text=editor.get_title())
            return editor
        else:
            editor.destroy()
            return None

    def get_editor(self, filename_or_id, open_when_necessary=False):
        if os.path.isfile(filename_or_id):
            filename_or_id = normpath_with_actual_case(os.path.abspath(filename_or_id))

        for child in self.winfo_children():
            assert isinstance(child, Editor)
            child_identifier = child.get_identifier()
            if child_identifier == filename_or_id:
                return child

        if open_when_necessary:
            return self._open_file(filename_or_id)
        else:
            return None

    def check_allow_closing(self, editor=None):
        if not editor:
            modified_editors = [e for e in self.winfo_children() if e.is_modified()]
        else:
            if not editor.is_modified():
                return True
            else:
                modified_editors = [editor]
        if len(modified_editors) == 0:
            return True

        message = tr("Do you want to save files before closing?")
        if editor:
            message = tr("Do you want to save file before closing?")

        confirm = messagebox.askyesnocancel(
            title=tr("Save On Close"), message=message, default=messagebox.YES, master=self
        )

        if confirm:
            for editor_ in modified_editors:
                assert isinstance(editor_, Editor)
                if editor_.get_filename(True):
                    if not editor_.save_file():
                        return False
                else:
                    return False
            return True

        elif confirm is None:
            return False
        else:
            return True

    def check_for_external_changes(self, event=None):
        if self._checking_external_changes:
            # otherwise the method will be re-entered when focus
            # changes because of a confirmation message box
            return

        self._checking_external_changes = True
        try:
            for editor in self.get_all_editors():
                editor.check_for_external_changes()
        finally:
            self._checking_external_changes = False


def get_current_breakpoints():
    result = {}

    for editor in get_workbench().get_editor_notebook().get_all_editors():
        filename = editor.get_filename()
        if filename:
            linenos = editor.get_code_view().get_breakpoint_line_numbers()
            if linenos:
                result[filename] = linenos

    return result


def get_saved_current_script_filename(force=True):
    editor = get_workbench().get_editor_notebook().get_current_editor()
    if not editor:
        return None

    filename = editor.get_filename(force)
    if not filename:
        return None

    if editor.is_modified():
        filename = editor.save_file()

    return filename


def get_target_dirname_from_editor_filename(s):
    if is_local_path(s):
        return os.path.dirname(s)
    else:
        return universal_dirname(extract_target_path(s))


def extract_target_path(s):
    assert is_remote_path(s)
    return s[s.find(REMOTE_PATH_MARKER) + len(REMOTE_PATH_MARKER):]


def make_remote_path(target_path):
    return get_runner().get_node_label() + REMOTE_PATH_MARKER + target_path
