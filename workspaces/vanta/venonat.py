#!/usr/bin/env python3
import curses
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import textwrap


DEFAULT_PROJECT_ID = "01992fca-c2a8-74d0-92dc-c356e45266ce"
DEFAULT_CLASS_ID = "019b3484-f550-77bc-8c28-86627185b6a3"
DEFAULT_CURSOR_EDITOR_ID = "01938c6f-d9b9-7824-adfe-da30eb56ec41"
DEFAULT_VSCODE_EDITOR_ID = "018d655f-2f16-761e-b530-390d640fd9db"

PROJECT_ID = os.environ.get("ONA_TUI_PROJECT_ID", DEFAULT_PROJECT_ID)
CLASS_ID = os.environ.get("ONA_TUI_CLASS_ID", DEFAULT_CLASS_ID)
INACTIVITY_TIMEOUT = os.environ.get("ONA_TUI_INACTIVITY_TIMEOUT", "3h")
CURSOR_EDITOR = os.environ.get("ONA_TUI_CURSOR_EDITOR", DEFAULT_CURSOR_EDITOR_ID)
VSCODE_EDITOR = os.environ.get("ONA_TUI_VSCODE_EDITOR", DEFAULT_VSCODE_EDITOR_ID)
ENV_LIMIT = os.environ.get("ONA_TUI_LIMIT", "100")
SCP_USER = os.environ.get("ONA_TUI_SSH_USER", "gitpod_devcontainer")
SCP_HOST_SUFFIX = os.environ.get("ONA_TUI_SSH_HOST_SUFFIX", ".gitpod.remote")
SCP_DEFAULT_REMOTE = os.environ.get("ONA_TUI_SCP_REMOTE", "/workspaces/obsidian")

FOOTER = (
    "ona deck  ::  [n] new  [s] start  [x] stop  [enter] ssh  [o] open  [c] scp  "
    "[r] refresh  [/] find  [?] help  [q] bye"
)


class OnaTui:
    def __init__(self, screen):
        self.screen = screen
        self.environments = []
        self.filtered = []
        self.selected = 0
        self.offset = 0
        self.filter_text = ""
        self.message = "Loading environments..."
        self.error = ""
        self.running = True

    def run(self):
        self.set_cursor(0)
        self.screen.keypad(True)
        self.setup_colors()
        self.refresh_environments()

        while self.running:
            self.draw()
            key = self.screen.getch()
            self.handle_key(key)

    def setup_colors(self):
        if not curses.has_colors():
            return

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_RED, -1)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_CYAN)

    def color(self, pair, fallback=0):
        if not curses.has_colors():
            return fallback
        return curses.color_pair(pair)

    def handle_key(self, key):
        if key in (ord("q"), 27):
            self.running = False
        elif key in (curses.KEY_UP, ord("k")):
            self.move_selection(-1)
        elif key in (curses.KEY_DOWN, ord("j")):
            self.move_selection(1)
        elif key == curses.KEY_PPAGE:
            self.move_selection(-self.list_height())
        elif key == curses.KEY_NPAGE:
            self.move_selection(self.list_height())
        elif key == ord("r"):
            self.refresh_environments()
        elif key == ord("/"):
            self.prompt_filter()
        elif key == ord("?"):
            self.show_help()
        elif key == ord("n"):
            self.create_environment()
        elif key == ord("s"):
            self.run_for_selected(["ona", "environment", "start", "{id}", "--set-as-context"], refresh=True)
        elif key == ord("x"):
            env = self.current_environment()
            if env and self.confirm(f"Stop {env['name']}?"):
                self.run_for_selected(["ona", "environment", "stop", "{id}"], refresh=True)
        elif key in (curses.KEY_ENTER, 10, 13):
            self.run_for_selected(["ona", "environment", "ssh", "{id}", "--start"], refresh=True)
        elif key == ord("o"):
            self.prompt_open_editor()
        elif key == ord("c"):
            self.prompt_scp()

    def prompt_open_editor(self):
        if not self.current_environment():
            return

        self.message = "open in...  [c] cursor  [v] vscode  [esc] cancel"
        self.draw()

        second = self.screen.getch()
        if second == ord("c"):
            self.open_in_editor(CURSOR_EDITOR)
        elif second == ord("v"):
            self.open_in_editor(VSCODE_EDITOR)
        else:
            self.message = ""

    def open_in_editor(self, editor):
        self.run_for_selected(
            ["ona", "environment", "open", "{id}", "--editor", editor, "--start"],
            refresh=False,
        )

    def prompt_scp(self):
        env = self.current_environment()
        if not env:
            self.message = "No environment selected."
            return

        if not shutil.which("scp"):
            self.error = "scp not found on PATH."
            return

        self.message = "scp...  [u] upload local->remote  [d] download remote->local  [esc] cancel"
        self.draw()

        second = self.screen.getch()
        if second in (ord("u"), ord("U")):
            self.scp_transfer(env, upload=True)
        elif second in (ord("d"), ord("D")):
            self.scp_transfer(env, upload=False)
        else:
            self.message = ""

    def scp_prompt(self, prompt_func, label, default="", noun=None):
        """Prompt for a path. Returns the resolved value, or None to abort the
        transfer (Esc was pressed, or a required path — one with a `noun` and no
        default — was left blank)."""
        value = prompt_func(label, default)
        if value is None:
            return None
        value = value.strip() or default
        if not value and noun:
            self.message = f"scp cancelled: no {noun} path."
        return value or None

    def scp_transfer(self, env, upload):
        host = f"{SCP_USER}@{env['id']}{SCP_HOST_SUFFIX}"

        if upload:
            local = self.scp_prompt(self.prompt_path, "Local path (source)", noun="local")
            if local is None:
                return
            remote = self.scp_prompt(self.prompt, "Remote path (dest)", SCP_DEFAULT_REMOTE)
            if remote is None:
                return
            source, dest = os.path.expanduser(local), f"{host}:{remote}"
        else:
            remote = self.scp_prompt(self.prompt, "Remote path (source)", noun="remote")
            if remote is None:
                return
            local = self.scp_prompt(self.prompt_path, "Local path (dest)", ".")
            if local is None:
                return
            source, dest = f"{host}:{remote}", os.path.expanduser(local)

        self.run_command(["scp", "-r", source, dest])

    def move_selection(self, delta):
        if not self.filtered:
            return

        self.selected = max(0, min(self.selected + delta, len(self.filtered) - 1))
        height = self.list_height()

        if self.selected < self.offset:
            self.offset = self.selected
        elif self.selected >= self.offset + height:
            self.offset = self.selected - height + 1

    def list_height(self):
        height, _ = self.screen.getmaxyx()
        return max(1, height - 8)

    def current_environment(self):
        if not self.filtered:
            return None
        return self.filtered[self.selected]

    def refresh_environments(self):
        self.message = "Loading environments..."
        self.error = ""
        self.draw()

        result = subprocess.run(
            ["ona", "environment", "list", "--format", "json", "--limit", ENV_LIMIT, "--timeout", "2m"],
            text=True,
            capture_output=True,
        )

        if result.returncode != 0:
            self.error = result.stderr.strip() or result.stdout.strip() or "Failed to load environments."
            self.message = "Refresh failed."
            return

        try:
            raw_environments = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            self.error = f"Could not parse Ona JSON: {exc}"
            self.message = "Refresh failed."
            return

        self.environments = [self.normalize_environment(item) for item in raw_environments]
        self.apply_filter()
        self.message = f"Loaded {len(self.environments)} environments."

    def normalize_environment(self, item):
        metadata = item.get("metadata") or {}
        status = item.get("status") or {}
        content = status.get("content") or {}
        git = content.get("git") or {}
        phase = (status.get("phase") or "-").replace("ENVIRONMENT_PHASE_", "").lower()

        return {
            "id": item.get("id") or "-",
            "name": metadata.get("name") or "(unnamed)",
            "phase": phase,
            "branch": git.get("branch") or "-",
            "repo": git.get("cloneUrl") or "-",
            "created": metadata.get("createdAt") or "-",
            "last_started": metadata.get("lastStartedAt") or "-",
        }

    def apply_filter(self):
        query = self.filter_text.lower().strip()
        if not query:
            self.filtered = list(self.environments)
        else:
            self.filtered = [
                env for env in self.environments
                if query in " ".join([env["id"], env["name"], env["phase"], env["branch"], env["repo"]]).lower()
            ]

        self.selected = min(self.selected, max(0, len(self.filtered) - 1))
        self.offset = min(self.offset, self.selected)

    def draw(self):
        self.screen.erase()
        height, width = self.screen.getmaxyx()

        if height < 12 or width < 70:
            self.addstr(0, 0, "ona-tui needs a larger terminal.", curses.A_BOLD)
            self.screen.refresh()
            return

        self.draw_header(width)
        self.draw_table(height, width)
        self.draw_details(height, width)
        self.draw_message(height, width)
        self.draw_footer(height, width)
        self.screen.refresh()

    def draw_header(self, width):
        title = "Ona environments"
        subtitle = f"{len(self.filtered)}/{len(self.environments)} shown"
        if self.filter_text:
            subtitle += f"  find: {self.filter_text}"

        self.addstr(0, 2, title, curses.A_BOLD | self.color(1))
        self.addstr(0, max(2, width - len(subtitle) - 2), subtitle, curses.A_DIM)
        self.hline(1, 0, width)

    def draw_table(self, height, width):
        list_width = max(46, int(width * 0.62))
        header = self.fit_columns(
            ["name", "phase", "branch"],
            [22, 10, max(10, list_width - 38)],
        )

        self.addstr(3, 2, header, curses.A_BOLD)
        visible = self.filtered[self.offset:self.offset + self.list_height()]

        if not visible:
            self.addstr(5, 4, "No environments match.", curses.A_DIM)
            return

        for index, env in enumerate(visible):
            row_index = self.offset + index
            y = 4 + index
            widths = [22, 10, max(10, list_width - 38)]
            row = self.fit_columns([env["name"], env["phase"], env["branch"]], widths)
            attr = curses.A_REVERSE if row_index == self.selected else 0
            attr |= self.phase_attr(env["phase"])
            self.addstr(y, 2, row.ljust(list_width - 4), attr)

    def draw_details(self, height, width):
        env = self.current_environment()
        if not env:
            return

        x = max(50, int(width * 0.62) + 1)
        pane_width = max(20, width - x - 2)
        self.vline(2, x - 2, height - 5)
        self.addstr(3, x, "Selected", curses.A_BOLD | self.color(1))

        lines = [
            ("Name", env["name"]),
            ("Phase", env["phase"]),
            ("Branch", env["branch"]),
            ("Repo", env["repo"]),
            ("ID", env["id"]),
            ("Created", self.short_time(env["created"])),
            ("Last start", self.short_time(env["last_started"])),
        ]

        y = 5
        for label, value in lines:
            self.addstr(y, x, f"{label}: ", curses.A_BOLD)
            wrapped = textwrap.wrap(value, pane_width - len(label) - 3) or [""]
            self.addstr(y, x + len(label) + 2, wrapped[0][:pane_width - len(label) - 3])
            y += 1
            for continuation in wrapped[1:3]:
                self.addstr(y, x + 2, continuation[:pane_width - 2], curses.A_DIM)
                y += 1
            y += 1
            if y >= height - 5:
                break

    def draw_message(self, height, width):
        y = height - 3
        text = self.error or self.message
        attr = self.color(4) if self.error else curses.A_DIM
        self.addstr(y, 2, text[:width - 4], attr)

    def draw_footer(self, height, width):
        footer = self.center_text(FOOTER, width - 2)
        footer_attr = curses.A_REVERSE | curses.A_BOLD
        self.addstr(height - 1, 0, " " * (width - 1), footer_attr)
        self.addstr(height - 1, 1, footer[:width - 2], footer_attr)

    def phase_attr(self, phase):
        if phase == "running":
            return self.color(2)
        if phase in ("stopping", "starting", "creating", "updating"):
            return self.color(3)
        if phase in ("deleted", "deleting"):
            return self.color(4)
        return 0

    def prompt_filter(self):
        value = self.prompt("Find", self.filter_text)
        if value is None:
            return
        self.filter_text = value
        self.selected = 0
        self.offset = 0
        self.apply_filter()
        self.message = "Filter cleared." if not value else f"Filtering by: {value}"

    def create_environment(self):
        default = dt.datetime.now().strftime("%b-%d").lower()
        name = self.prompt("Environment name", default)
        if name is None:
            return
        name = name.strip() or default

        result = self.run_captured_command([
            "ona", "environment", "create", PROJECT_ID,
            "--name", name,
            "--class-id", CLASS_ID,
            "--inactivity-timeout", INACTIVITY_TIMEOUT,
            "--dont-wait",
            "--set-as-context",
        ])
        if result.returncode == 0:
            self.refresh_environments()
            self.message = f"Created {name}."
        else:
            self.error = result.stderr.strip() or result.stdout.strip() or f"Create failed with status {result.returncode}."

    def run_for_selected(self, command, refresh):
        env = self.current_environment()
        if not env:
            self.message = "No environment selected."
            return

        expanded = [env["id"] if part == "{id}" else part for part in command]
        self.run_command(expanded)
        if refresh:
            self.refresh_environments()

    def run_captured_command(self, command):
        self.error = ""
        self.message = "Running: " + " ".join(shlex_quote(part) for part in command)
        self.draw()
        return subprocess.run(command, text=True, capture_output=True)

    def run_command(self, command):
        curses.def_prog_mode()
        curses.endwin()
        print()
        print("Running:", " ".join(shlex_quote(part) for part in command))
        print()
        status = subprocess.call(command)
        if status != 0:
            print()
            print(f"Command failed with status {status}.")
        print()
        input("Press Enter to return to ona-tui...")
        curses.reset_prog_mode()
        self.set_cursor(0)
        self.screen.keypad(True)
        self.message = "Command finished." if status == 0 else f"Command failed with status {status}."

    def prompt(self, label, default=""):
        height, width = self.screen.getmaxyx()
        prompt = f"{label} [{default}]: " if default else f"{label}: "
        y = height - 3

        curses.echo()
        self.set_cursor(1)
        self.addstr(y, 0, " " * width)
        self.addstr(y, 2, prompt, curses.A_BOLD)
        self.screen.refresh()

        try:
            raw = self.screen.getstr(y, min(width - 1, len(prompt) + 2), max(0, width - len(prompt) - 4))
        except KeyboardInterrupt:
            raw = None
        finally:
            curses.noecho()
            self.set_cursor(0)

        if raw is None:
            return None

        value = raw.decode(errors="replace")
        return value if value else default

    def prompt_path(self, label, default=""):
        height, width = self.screen.getmaxyx()
        y = height - 3
        prompt = f"{label} [{default}]: " if default else f"{label}: "
        buf = ""

        self.set_cursor(1)
        try:
            while True:
                self.addstr(y, 0, " " * (width - 1))
                self.addstr(y, 2, prompt, curses.A_BOLD)
                self.addstr(y, 2 + len(prompt), buf)
                self.screen.move(y, min(width - 1, 2 + len(prompt) + len(buf)))
                self.screen.refresh()

                key = self.screen.getch()
                if key == 27:
                    return None
                if key in (curses.KEY_ENTER, 10, 13):
                    value = buf.strip()
                    return value if value else default
                if key in (curses.KEY_BACKSPACE, 127, 8):
                    buf = buf[:-1]
                elif key == 9:
                    buf = self.complete_local_path(buf, y - 1, width)
                elif 32 <= key < 127:
                    buf += chr(key)
        finally:
            self.set_cursor(0)

    def complete_local_path(self, buf, hint_y, width):
        self.addstr(hint_y, 0, " " * (width - 1))
        directory, sep, prefix = buf.rpartition("/")
        listing_dir = os.path.expanduser(directory) if sep else "."

        try:
            entries = sorted(os.listdir(listing_dir or "."))
        except OSError:
            self.addstr(hint_y, 2, "(can't read directory)", curses.A_DIM)
            return buf

        matches = [e for e in entries if e.startswith(prefix)]
        if not matches:
            self.addstr(hint_y, 2, "(no match)", curses.A_DIM)
            return buf

        if len(matches) == 1:
            new_buf = buf + matches[0][len(prefix):]
            if os.path.isdir(os.path.join(listing_dir or ".", matches[0])) and not new_buf.endswith("/"):
                new_buf += "/"
            return new_buf

        self.addstr(hint_y, 2, "  ".join(matches)[:width - 4], curses.A_DIM)
        return buf + os.path.commonprefix(matches)[len(prefix):]

    def confirm(self, question):
        height, width = self.screen.getmaxyx()
        self.addstr(height - 3, 0, " " * width)
        self.addstr(height - 3, 2, f"{question}  y/N", curses.A_BOLD | self.color(3))
        self.screen.refresh()
        key = self.screen.getch()
        return key in (ord("y"), ord("Y"))

    def show_help(self):
        lines = [
            "Keys",
            "",
            "n      create a new environment",
            "s      start selected environment and set it as context",
            "x      stop selected environment",
            "Enter  SSH into selected environment",
            "o c    open selected environment in Cursor",
            "o v    open selected environment in VS Code",
            "c u    upload a local file/dir to the selected environment",
            "c d    download a file/dir from the selected environment",
            "       (Tab completes local paths; remote paths are free-text)",
            "r      refresh the environment list",
            "/      filter by name, id, phase, repo, or branch",
            "q      quit",
            "",
            "scp uses native SSH; run 'ona environment ssh-config' once first.",
            "",
            "Press any key to return.",
        ]
        self.modal(lines)

    def modal(self, lines):
        height, width = self.screen.getmaxyx()
        box_width = min(width - 8, max(len(line) for line in lines) + 6)
        box_height = min(height - 4, len(lines) + 4)
        y = max(1, (height - box_height) // 2)
        x = max(2, (width - box_width) // 2)

        window = curses.newwin(box_height, box_width, y, x)
        window.border()
        for index, line in enumerate(lines[:box_height - 4]):
            attr = curses.A_BOLD if index == 0 else 0
            window.addstr(index + 2, 3, line[:box_width - 6], attr)
        window.refresh()
        window.getch()

    def addstr(self, y, x, text, attr=0):
        height, width = self.screen.getmaxyx()
        if y < 0 or y >= height or x >= width:
            return
        self.screen.addstr(y, max(0, x), text[:max(0, width - max(0, x) - 1)], attr)

    def hline(self, y, x, width):
        self.screen.hline(y, x, curses.ACS_HLINE, max(0, width))

    def vline(self, y, x, height):
        self.screen.vline(y, x, curses.ACS_VLINE, max(0, height))

    def set_cursor(self, visibility):
        try:
            curses.curs_set(visibility)
        except curses.error:
            pass

    def fit_columns(self, values, widths):
        cells = []
        for value, width in zip(values, widths):
            cells.append(ellipsize(str(value), width).ljust(width))
        return "  ".join(cells)

    def center_text(self, text, width):
        if len(text) >= width:
            return text[:width]
        padding = max(0, (width - len(text)) // 2)
        return " " * padding + text

    def short_time(self, value):
        if value == "-":
            return value
        return value.replace("T", " ").replace("Z", " UTC")


def ellipsize(value, width):
    if width <= 0:
        return ""
    if len(value) <= width:
        return value
    if width <= 1:
        return value[:width]
    if width <= 3:
        return value[:width]
    return value[:width - 3] + "..."


def shlex_quote(value):
    import shlex
    return shlex.quote(value)


def require_command(name):
    if shutil.which(name):
        return
    print(f"ona-tui: missing required command: {name}", file=sys.stderr)
    sys.exit(1)


def usage():
    print("""Usage: ona-tui
Interactive terminal UI for common Ona environment actions.
Environment overrides:
  ONA_TUI_PROJECT_ID             Project ID to use for new environments.
  ONA_TUI_CLASS_ID               Machine class ID to use for new environments.
  ONA_TUI_INACTIVITY_TIMEOUT     Inactivity timeout for new environments. Default: 3h.
  ONA_TUI_CURSOR_EDITOR          Editor ID or name for Cursor. Default: Cursor editor ID.
  ONA_TUI_LIMIT                  Number of environments to list. Default: 100.
  ONA_TUI_SSH_USER               SSH user for scp. Default: gitpod_devcontainer.
  ONA_TUI_SSH_HOST_SUFFIX        Native SSH host suffix for scp. Default: .gitpod.remote.
  ONA_TUI_SCP_REMOTE             Default remote path for uploads. Default: /workspaces/obsidian.
""")


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h", "--help"):
            usage()
            return 0
        usage()
        return 2

    require_command("ona")
    curses.wrapper(lambda screen: OnaTui(screen).run())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
