"""Stand-in for tkMessageBox: notices are queued on the bus instead of popping up."""
import bus


def showinfo(title, message):
    bus.messages.append((str(title), str(message)))
    return "ok"


showwarning = showerror = showinfo


def askyesno(title, message):
    # The only caller (Play.ExtraPoint) compares the result to the string "no",
    # which never matches, so the desktop app always proceeded.  Preserve that.
    bus.messages.append((str(title), str(message)))
    return True
