import importlib
import platform
import re
import subprocess
import sys
import threading
from ast import literal_eval
from functools import cache
from parifinder import parse_pairs
from splitlistatindex import list_split
from flatten_everything import flatten_everything
import ctypes
import random

try:
    pd = importlib.__import__("pandas")
except Exception:
    pass
from ansi.colour.rgb import rgb256
from ansi.colour import bg, fx

strblackbg = str(bg.black)
resetstr = str(fx.reset)
backslash = "\\"
allthreads = []
allsubprocs = []

colors_with_black_bg = [
    (255, 255, 255),  # White
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (192, 255, 192),  # Light Green (3)
    (192, 192, 255),  # Light Blue (3)
    (255, 192, 255),  # Light Magenta (3)
    (192, 255, 255),  # Light Cyan (3)
    (255, 255, 192),  # Light Yellow (3)
    (255, 192, 128),  # Light Orange
    (255, 128, 255),  # Light Pink
    (128, 255, 192),  # Light Turquoise
    (192, 128, 255),  # Lavender
    (255, 255, 128),  # Light Lime
    (128, 192, 255),  # Baby Blue
    (192, 255, 128),  # Light Lime (2)
    (128, 255, 255),  # Light Aqua (2)
    (255, 128, 192),  # Light Rose
    (0, 128, 0),  # Green (dark)
    (0, 0, 128),  # Navy
    (128, 128, 0),  # Olive
    (128, 0, 128),  # Purple
    (0, 128, 128),  # Teal
    (192, 192, 192),  # Light Gray
    (128, 128, 128),  # Medium Gray
    (64, 64, 64),  # Dark Gray
    (255, 128, 0),  # Orange
    (0, 255, 128),  # Turquoise
    (128, 0, 255),  # Violet
    (255, 128, 128),  # Salmon
    (128, 255, 0),  # Lime
    (0, 128, 255),  # Sky Blue
    (255, 0, 128),  # Fuchsia
    (128, 255, 128),  # Light Green
    (128, 128, 255),  # Light Blue
    (255, 128, 255),  # Light Magenta
    (128, 255, 255),  # Light Cyan
    (255, 255, 128),  # Pale Yellow
    (192, 128, 0),  # Brown
    (128, 192, 0),  # Chartreuse
    (192, 0, 128),  # Indigo
    (0, 192, 128),  # Sea Green
    (128, 0, 192),  # Plum
    (192, 128, 128),  # Rosy Brown
    (128, 192, 128),  # Pale Green
    (128, 128, 192),  # Light Periwinkle
    (192, 128, 192),  # Orchid
    (192, 192, 128),  # Khaki
    (255, 128, 192),  # Pink
    (192, 255, 128),  # Lime Green
    (128, 192, 255),  # Light Sky Blue
    (255, 128, 255),  # Light Fuchsia
    (192, 255, 255),  # Light Aqua
    (255, 255, 192),  # Pale Lemon
    (128, 64, 0),  # Dark Orange
    (0, 128, 64),  # Dark Turquoise
    (64, 0, 128),  # Dark Violet
    (128, 64, 64),  # Dark Salmon
    (64, 128, 0),  # Dark Lime
    (0, 64, 128),  # Dark Sky Blue
    (128, 0, 64),  # Dark Fuchsia
    (64, 128, 64),  # Dark Sea Green
    (64, 64, 128),  # Dark Periwinkle
    (128, 64, 128),  # Dark Orchid
    (128, 128, 64),  # Dark Khaki
    (128, 0, 192),  # Dark Pink
    (192, 0, 64),  # Dark Indigo
    (0, 192, 64),  # Dark Sea Green (2)
    (64, 0, 192),  # Dark Plum
    (192, 64, 64),  # Dark Rosy Brown
    (64, 192, 64),  # Dark Pale Green
    (64, 64, 192),  # Dark Light Periwinkle
    (192, 64, 192),  # Dark Orchid (2)
    (192, 192, 64),  # Dark Khaki (2)
    (255, 64, 0),  # Darker Orange
    (0, 255, 64),  # Darker Turquoise
    (64, 0, 255),  # Darker Violet
    (255, 64, 64),  # Darker Salmon
    (64, 255, 0),  # Darker Lime
    (0, 64, 255),  # Darker Sky Blue
    (255, 0, 64),  # Darker Fuchsia
    (64, 255, 64),  # Darker Sea Green
    (64, 64, 255),  # Darker Periwinkle
    (255, 64, 255),  # Darker Orchid
    (64, 255, 255),  # Darker Light Blue
    (255, 255, 64),  # Darker Yellow
    (192, 192, 192),  # Light Gray (2)
    (255, 192, 0),  # Gold
    (0, 255, 192),  # Aquamarine
    (192, 0, 255),  # Hot Pink
    (192, 255, 0),  # Chartreuse (2)
    (0, 192, 255),  # Light Sky Blue (2)
    (255, 0, 192),  # Medium Orchid
    (255, 192, 192),  # Light Salmon
    (192, 255, 192),  # Light Green (2)
    (192, 192, 255),  # Light Blue (2)
    (255, 192, 255),  # Light Magenta (2)
    (192, 255, 255),  # Light Cyan (2)
    (255, 255, 192),  # Light Yellow (2)
    (255, 192, 64),  # Peach
    (192, 255, 64),  # Yellow-Green
    (192, 64, 255),  # Blue-Violet
    (64, 192, 255),  # Powder Blue
    (255, 64, 192),  # Raspberry
]

color_dict = {
    (255, 255, 0): "colorsep",
    (200, 120, 120): "color2",
    (0, 255, 0): "color3",
}
color_dict_values = {v: k for k, v in color_dict.items()}
maxstrlen = {}
reletter = re.compile(r"\[([A-Z0-9_;\s]+)\]")
retextfind = re.compile(r";\s+Text:\s+\[.*?];\s+")
resubspaces = re.compile(r"(?:^\s*\[\s*)|(?:\s*\]\s*$)")
reevent = re.compile(r"^.*\s+EventType:\s+")
splitregex = re.compile(rf"[\[\]]+")
textregex = re.compile(r"\bText:\s+")
iswindows = "win" in platform.platform().lower()
if iswindows:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    creationflags = subprocess.CREATE_NO_WINDOW
    invisibledict = {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "start_new_session": True,
    }
    from ctypes import wintypes

    windll = ctypes.LibraryLoader(ctypes.WinDLL)
    user32 = windll.user32
    kernel32 = windll.kernel32
    GetExitCodeProcess = windll.kernel32.GetExitCodeProcess
    CloseHandle = windll.kernel32.CloseHandle
    GetExitCodeProcess.argtypes = [
        ctypes.wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_ulong),
    ]
    CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
    GetExitCodeProcess.restype = ctypes.c_int
    CloseHandle.restype = ctypes.c_int

    GetWindowRect = user32.GetWindowRect
    GetClientRect = user32.GetClientRect
    _GetShortPathNameW = kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
    _GetShortPathNameW.restype = wintypes.DWORD
else:
    invisibledict = {}


@cache
def get_short_path_name(long_name):
    try:
        if not iswindows:
            return long_name
        output_buf_size = 4096
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
        return output_buf.value
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        return long_name


def killall(*args):
    for arg in args:
        try:
            arg.kill()
        except Exception:
            try:
                killthread(arg)
            except Exception:
                pass


def killthread(threadobject):
    # based on https://pypi.org/project/kthread/
    if not threadobject.is_alive():
        return True
    tid = -1
    for tid1, tobj in threading._active.items():
        if tobj is threadobject:
            tid = tid1
            break
    if tid == -1:
        sys.stderr.write(f"{threadobject} not found")
        return False
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(SystemExit)
    )
    if res == 0:
        return False
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        return False
    return True


class EventRecord:
    r"""
    EventRecord class for recording events from an Android device using ADB.

    This class provides a way to capture events from an Android device using ADB (Android Debug Bridge).
    It can parse and display event data in both standard output and Pandas DataFrame formats.

    Args:
        adb_path (str): The path to the ADB executable.
        device_serial (str): The serial number of the target Android device.
        print_output (bool, optional): Whether to print event data to the console. Default is True.
        print_output_pandas (bool, optional): Whether to print event data as Pandas DataFrames. Default is False.
        convert_to_pandas (bool, optional): Whether to convert event data to Pandas DataFrames. Default is False.
        parent1replacement (str, optional): A character used to replace temporarily opening square brackets '[' in event data. Default is "\x80".
        parent2replacement (str, optional): A character used to replace temporarily closing square brackets ']' in event data. Default is "\x81".

    Methods:
        start_recording(**kwargs): Starts recording events from the device.

    Attributes:
        stop: Stops the event recording if True
        results (list): A list of lists containing parsed event data.
        resultsdf (list): A list of Pandas DataFrames containing parsed event data. (if installed)

    Example usage
        from adbeventparser import EventRecord
        sua = EventRecord(
            adb_path=r"C:\Android\android-sdk\platform-tools\adb.exe",
            device_serial="127.0.0.1:5555",
            print_output=True,
            print_output_pandas=False,
            convert_to_pandas=False,
            parent1replacement="\x80",
            parent2replacement="\x81",
        )
        sua.start_recording()
        # to stop
        # sua.stop=True
        # the data as a list of lists
        # sua.results
        # the data as pandas (if installed)
        # sua.resultsdf
    """

    def __init__(
        self,
        adb_path,
        device_serial,
        print_output=True,
        print_output_pandas=False,
        convert_to_pandas=False,
        parent1replacement="\x80",
        parent2replacement="\x81",
    ):
        self.adb_path = get_short_path_name(adb_path)
        self.device_serial = device_serial
        self.pr = None
        self.print_output = print_output
        self.convert_to_pandas = convert_to_pandas
        self.resultsdf = []
        self.results = []
        self.stop = False
        self.parent1replacement = parent1replacement
        self.parent2replacement = parent2replacement
        self.threadparse = None
        self.print_output_pandas = print_output_pandas

    def _read_stdout(
        self,
    ):
        r"""
        Internal method to read and decode standard output from the ADB process.

        This method reads standard output from the ADB process, decodes it, and yields lines.

        Returns:
            Iterator[str]: An iterator yielding lines from standard output.
        """
        try:
            for l in iter(self.pr.stdout.readline, b""):
                if self.stop:
                    raise TimeoutError
                yield l.decode("utf-8", "backslashreplace")
        except Exception:
            try:
                self.pr.stdout.close()
            except Exception as fe:
                sys.stderr.write(f"{fe}")
                sys.stderr.flush()

    def start_recording(self, **kwargs):
        r"""
        Start recording events from the Android device.

        Args:
            **kwargs: Additional keyword arguments for subprocess.Popen.

        This method starts recording events from the Android device by launching the ADB process.
        """
        self.stop = False
        self.threadparse = threading.Thread(
            target=self._tstart_recording, kwargs=kwargs
        )
        self.threadparse.start()

    def _tstart_recording(self, **kwargs):
        allresx = []
        alloops = 0
        colorsep = (
            strblackbg + rgb256(*color_dict_values.get("colorsep")) + "█" + resetstr
        )
        color3 = rgb256(*color_dict_values.get("color3"))

        for ax, sti in enumerate(self._start_recording(**kwargs)):
            if self.stop:
                return
            sti = sti.replace(
                "[]", f"{self.parent1replacement}{self.parent2replacement}"
            )
            sti = reletter.sub("\\g<1>", sti)

            for xax in retextfind.finditer(sti):
                sti = (
                    sti[: xax.start()]
                    + sti[xax.start() : xax.end()]
                    .replace("[", f"{self.parent1replacement}")
                    .replace("]", f"{self.parent2replacement}")
                    + sti[xax.end() - 1 :]
                )

            sli = parse_pairs(string=sti, s1="[", s2="]", str_regex=False)
            allspli = []
            for k, v in sli.items():
                u = resubspaces.sub("", sti).split(";")
                for uu in u:
                    allspli.extend([(v["start"], v["end"])])

            allspli2 = sorted(list(set(tuple(flatten_everything(allspli)))))

            result1 = list_split(l=sti, indices_or_sections=allspli2)
            allres = []
            for ini, hh in enumerate(result1):
                hh = hh.replace(
                    f"{self.parent1replacement}{self.parent2replacement}", " "
                )
                hh = hh.replace(self.parent1replacement, "[").replace(
                    self.parent2replacement, "]"
                )
                if ini == 0:
                    try:
                        da = reevent.findall(hh)[0]
                        hh = (
                            f'Tstamp: {da.replace(":", self.parent1replacement).replace(f" EventType{self.parent1replacement}", "; EventType: ")}'
                            + hh[len(da) :]
                        )
                    except Exception as e:
                        sys.stderr.write(f"{e}")
                if not textregex.findall(hh):
                    for hhh in hh.split("; "):
                        if hhh.count("[") % 2 != 0 or hhh.count("]") % 2 != 0:
                            hhh = splitregex.split(hhh)
                            if hhh == ["", ""]:
                                continue
                            allres.append(f"{hhh}")
                        else:
                            allres.append(f"{hhh}")
                else:
                    for ixa in hh.split("; "):
                        if ixa.count("[") % 2 != 0 or ixa.count("]") % 2 != 0:
                            ixa = ixa.replace("[", "").replace("]", "").strip()
                        allres.append(ixa)
            allres = [(y + " ").split(":") for y in allres]
            lastone = ""
            for tu in range(len(allres)):
                allres[tu][0] = allres[tu][0].strip()
                try:
                    allres[tu][1] = allres[tu][1].strip()
                except Exception:
                    if lastone == "ContentChangeTypes":
                        allres[tu - 1][1] = allres[tu][0]

                if allres[tu][0] == "Tstamp":
                    allres[tu][1] = allres[tu][1].replace(self.parent1replacement, ":")
                lastone = allres[tu][0]
            allresx.append([[o[0], changedtypes(o[1])] for o in allres if len(o) == 2])
            self.results.extend(allresx)
            if self.print_output:
                allcols = []
                allvals = []
                for dat, va in allresx[0]:
                    if dat not in color_dict_values:
                        while (g := random.choice(colors_with_black_bg)) in color_dict:
                            pass
                        color_dict_values[dat] = rgb256(*g)
                        color_dict[g] = dat
                    strva = str(va)
                    lstrva = len(strva) + 4
                    datlen = len(str(dat)) + 4

                    if dat not in maxstrlen:
                        maxstrlen[dat] = lstrva if lstrva > datlen else datlen
                    else:
                        if (lstrva) > maxstrlen[dat]:
                            maxstrlen[dat] = lstrva if lstrva > datlen else datlen

                    color = color_dict_values[dat]
                    aacolor = (
                        strblackbg
                        + color
                        + f"  {strva}  ".ljust(maxstrlen[dat]).rjust(maxstrlen[dat])
                        + resetstr
                    )
                    bbcolor = (
                        color3
                        + f"  {dat}  ".ljust(maxstrlen[dat]).rjust(maxstrlen[dat])
                        + resetstr
                    )
                    allcols.append(colorsep + bbcolor + colorsep)
                    allvals.append(colorsep + aacolor + colorsep)
                if alloops % 10 == 0:
                    print()
                    for coa in allcols:
                        print(coa, end="")
                    print()
                for coa in allvals:
                    print(coa, end="")
                print()
                alloops = alloops + 1
            if self.convert_to_pandas:
                try:
                    df = pd.concat(
                        [pd.DataFrame(x).set_index(0).T for x in allresx],
                        ignore_index=True,
                    )
                    self.resultsdf.append(df)
                    if self.print_output_pandas:
                        print(df.to_string())
                except Exception as fe:
                    sys.stderr.write(f"{fe}")
                    sys.stderr.flush()
            allresx.clear()

    def _start_recording(self, **kwargs):
        kwargs.update(
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            bufsize=0,
        )
        kwargs.update(invisibledict)

        self.pr = subprocess.Popen(
            f"{self.adb_path} -s {self.device_serial} shell uiautomator events",
            **kwargs,
        )
        try:
            for _ in self._read_stdout():
                yield _
                if self.stop:
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            try:
                killall(self.pr, self.threadparse)
            except:
                killall(self.pr, self.threadparse)
        except Exception:
            killall(self.pr, self.threadparse)


@cache
def changedtypes(x):
    r"""
    Cache-decorated function to convert string values to appropriate data types.

    Args:
        x (str): The string value to convert.

    Returns:
        Any: The converted data type, or the original string if conversion fails.
    """
    x = x.strip()
    if x == "false":
        return False
    if x == "true":
        return True
    if x == "null":
        return None
    try:
        li = literal_eval(x)
        if isinstance(li, list):
            li = "".join([g for t in li if (g := t.strip())])
        return li

    except Exception:
        return x
