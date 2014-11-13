import sublime, sublime_plugin, colorsys, plistlib, re, os, time, os.path

class crc8:
    def __init__(self):
      self.crcTable = ( 0x00,0x07,0x0E,0x09,0x1C,0x1B,0x12,0x15,
                        0x38,0x3F,0x36,0x31,0x24,0x23,0x2A,0x2D,
                        0x70,0x77,0x7E,0x79,0x6C,0x6B,0x62,0x65,
                        0x48,0x4F,0x46,0x41,0x54,0x53,0x5A,0x5D,
                        0xE0,0xE7,0xEE,0xE9,0xFC,0xFB,0xF2,0xF5,
                        0xD8,0xDF,0xD6,0xD1,0xC4,0xC3,0xCA,0xCD,
                        0x90,0x97,0x9E,0x99,0x8C,0x8B,0x82,0x85,
                        0xA8,0xAF,0xA6,0xA1,0xB4,0xB3,0xBA,0xBD,
                        0xC7,0xC0,0xC9,0xCE,0xDB,0xDC,0xD5,0xD2,
                        0xFF,0xF8,0xF1,0xF6,0xE3,0xE4,0xED,0xEA,
                        0xB7,0xB0,0xB9,0xBE,0xAB,0xAC,0xA5,0xA2,
                        0x8F,0x88,0x81,0x86,0x93,0x94,0x9D,0x9A,
                        0x27,0x20,0x29,0x2E,0x3B,0x3C,0x35,0x32,
                        0x1F,0x18,0x11,0x16,0x03,0x04,0x0D,0x0A,
                        0x57,0x50,0x59,0x5E,0x4B,0x4C,0x45,0x42,
                        0x6F,0x68,0x61,0x66,0x73,0x74,0x7D,0x7A,
                        0x89,0x8E,0x87,0x80,0x95,0x92,0x9B,0x9C,
                        0xB1,0xB6,0xBF,0xB8,0xAD,0xAA,0xA3,0xA4,
                        0xF9,0xFE,0xF7,0xF0,0xE5,0xE2,0xEB,0xEC,
                        0xC1,0xC6,0xCF,0xC8,0xDD,0xDA,0xD3,0xD4,
                        0x69,0x6E,0x67,0x60,0x75,0x72,0x7B,0x7C,
                        0x51,0x56,0x5F,0x58,0x4D,0x4A,0x43,0x44,
                        0x19,0x1E,0x17,0x10,0x05,0x02,0x0B,0x0C,
                        0x21,0x26,0x2F,0x28,0x3D,0x3A,0x33,0x34,
                        0x4E,0x49,0x40,0x47,0x52,0x55,0x5C,0x5B,
                        0x76,0x71,0x78,0x7F,0x6A,0x6D,0x64,0x63,
                        0x3E,0x39,0x30,0x37,0x22,0x25,0x2C,0x2B,
                        0x06,0x01,0x08,0x0F,0x1A,0x1D,0x14,0x13,
                        0xAE,0xA9,0xA0,0xA7,0xB2,0xB5,0xBC,0xBB,
                        0x96,0x91,0x98,0x9F,0x8A,0x8D,0x84,0x83,
                        0xDE,0xD9,0xD0,0xD7,0xC2,0xC5,0xCC,0xCB,
                        0xE6,0xE1,0xE8,0xEF,0xFA,0xFD,0xF4,0xF3)

    def crc(self, msg):
        runningCRC = 0
        for c in msg:
            c = ord(c) % 256
            runningCRC = self.crcTable[runningCRC ^ c]
        return runningCRC

hasher = crc8()
scopes = []

use_textcommand = True

class colorcoder(sublime_plugin.EventListener):

    def on_new(self,view):
        view.settings().set('colorcode',True)

    def on_activated(self, view):
        self.on_load(view)

    def on_load(self,view):
        view.settings().set('colorcode',True)
        set = sublime.load_settings("colorcoder.sublime-settings")
        if view.file_name():
            filename = os.path.split(view.file_name())[1]
            dotp = filename.rfind('.')
            ext = '' if dotp == -1 else filename[dotp+1:]
            if (set.has('enabled_for') and ext not in set.get('enabled_for')) or ext in set.get('disabled_for',[]):
                view.settings().set('colorcode',False)
                return

        if view.size() > set.get('max_size') and not view.settings().get('forcecolorcode',False):
            sublime.status_message("File is too big, disabling colorcoding as it might hurt perfromance")
            colorcoder.remove_colorcode(view)
            view.settings().set('colorcode',False)
            return

        vcc = view.settings().get('color_scheme')
        if vcc and "Widget" in vcc: 
            view.settings().set('colorcode',False)
            return

        vcc = view.settings().get('syntax')
        if vcc and ".build-language" in vcc:
            view.settings().set('colorcode',False)
            return

        self.on_modified_async(view)

    def on_post_save(self,view):
        self.on_load(view)

    def on_modified_async(self, view):
        global use_textcommand
        if view.settings().get('colorcode',False) or view.settings().get('forcecolorcode',False):
            if use_textcommand:
                view.run_command("colorcode")
            else:
                colorcoder.colorcode(view)

    @staticmethod
    def update_scopes():
        global scopes
        scopes = sublime.load_settings("colorcoder.sublime-settings").get('scopes')

    @staticmethod
    def update_use_textcommand():
        global use_textcommand
        use_textcommand = sublime.load_settings("colorcoder.sublime-settings").get('use_fast_highlighting_but_undo_typing_letterwise')

    def on_post_text_command(self, view, cmd, args):
        if cmd=="set_file_type":
            self.on_modified_async(sublime.active_window().active_view())

    @staticmethod
    def colorcode(view):
        global hasher, scopes

        regs = {}
        for i in map(hex,range(256)):
            regs[i] = []

        for sel in scopes:
            for r in view.find_by_selector(sel):
                regs[hex(hasher.crc(view.substr(r)))].append(r)

        for key in regs:
            view.add_regions('cc'+key,regs[key],'cc'+key,'', sublime.DRAW_NO_OUTLINE )

        del regs

    @staticmethod
    def remove_colorcode(view):
        for i in map(hex,range(256)):
            view.erase_regions('cc'+i)

class colorcode(sublime_plugin.TextCommand):
    def run(self, edit):
        colorcoder.colorcode(self.view)


class colorcodertoggler(sublime_plugin.ApplicationCommand):
    def run(self):
        view = sublime.active_window().active_view()
        cc = view.settings().get('colorcode',False)
        view.settings().set('colorcode',not cc)
        view.settings().set('forcecolorcode',False)

        if cc:
            colorcoder.remove_colorcode(view)
        else:
            if view.size() > sublime.load_settings("colorcoder.sublime-settings").get('max_size'):
                view.settings().set('forcecolorcode',True)
            view.run_command("colorcode")

    def is_checked(self):
        viewset = sublime.active_window().active_view().settings()
        return viewset.get('colorcode',False) or viewset.get('forcecolorcode',False)

    def description(self):
        if sublime.active_window().active_view().size() > sublime.load_settings("colorcoder.sublime-settings").get('max_size'):
            return "Colorcoding may hurt performance, File is large"
        else:
            return "Colorcode this view"

modification_running = False

class colorshemeemodifier(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.active_window().show_input_panel("Lightness and Saturation","%s %s"%(sublime.load_settings("colorcoder.sublime-settings").get('lightness'),sublime.load_settings("colorcoder.sublime-settings").get('saturation')),self.panel_callback,None,None)

    def panel_callback(self, text):
        (l,s)= map(float,text.split(' '))
        sublime.load_settings("colorcoder.sublime-settings").set('lightness',l)
        sublime.load_settings("colorcoder.sublime-settings").set('saturation',s)
        sublime.save_settings("colorcoder.sublime-settings")
        colorshemeemodifier.modify_color_scheme(l,s,True)

    @staticmethod
    def maybefixscheme():
        set = sublime.load_settings("colorcoder.sublime-settings")
        if set.get('auto_apply_on_scheme_change'):
            if sublime.load_settings("Preferences.sublime-settings").get('color_scheme').find('/Colorcoder/') == -1:
                colorshemeemodifier.modify_color_scheme(set.get('lightness'),set.get('saturation'))

    @staticmethod
    def modify_color_scheme(l,s,read_original = False):
        read_original = read_original and sublime.load_settings("Preferences.sublime-settings").has("original_color_scheme")
        if read_original and sublime.load_settings("Preferences.sublime-settings").get('color_scheme').find('/Colorcoder/') == -1:
            read_original = False
        if read_original and sublime.load_settings("Preferences.sublime-settings").get('original_color_scheme').find('/Colorcoder/') != -1:
            print("original theme already colorcoded, abort")
            return
        global modification_running
        if modification_running:
            return
        modification_running = True
        name = sublime.load_settings("Preferences.sublime-settings").get("original_color_scheme") if read_original else sublime.active_window().active_view().settings().get('color_scheme')
        try:
            cs = plistlib.readPlistFromBytes(sublime.load_binary_resource(name))

            tokenclr = "#000000"
            for rule in cs["settings"]:
                if "scope" not in rule and "name" not in rule:
                    bgc = rule["settings"]["background"]
                    r = int(bgc[1:3],16)
                    g = int(bgc[3:5],16)
                    b = int(bgc[5:7],16)
                    if b>0:
                        b = b-1
                    elif g>0:
                        g = g-1
                    elif r>0:
                        r = r-1
                    else:
                        rule["settings"]["background"] = "#000001"
                    tokenclr =  "#%02x%02x%02x" % (r,g,b)
                    break

            cs["name"] = cs["name"] + " (Colorcoded)"

            for x in range(0,256):
                cs["settings"].append(dict(
                    scope="cc0x%x" % x,
                    settings=dict(
                        foreground="#"+''.join(map(lambda c: "%02x" % int(256*c),colorsys.hls_to_rgb(x/256., l, s))),
                        background=tokenclr
                    )
                ))

            newname = "/Colorcoder/%s (Colorcoded).tmTheme" % re.search("/([^/]+).tmTheme$", name).group(1)

            plistlib.writePlist(cs,"%s%s" % (sublime.packages_path(),newname))

            sublime.load_settings("Preferences.sublime-settings").set("original_color_scheme", name)
            sublime.load_settings("Preferences.sublime-settings").set("color_scheme","Packages%s" % newname)
            sublime.save_settings("Preferences.sublime-settings")
        except Exception as e:
            sublime.error_message("Colorcoder was not able to parse the colorscheme\nCheck the console for the actual error message.")
            sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})
            print(e)
        finally:
            modification_running = False

class colorcoderInspectScope(sublime_plugin.ApplicationCommand):
    def run(self):
        view = sublime.active_window().active_view();
        sel = view.sel()[0]
        print(view.scope_name(sel.a))
        sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})

def plugin_loaded():
    sublime.load_settings("Preferences.sublime-settings").add_on_change('color_scheme',colorshemeemodifier.maybefixscheme)
    sublime.load_settings("colorcoder.sublime-settings").add_on_change('scopes',colorcoder.update_scopes)
    sublime.load_settings("colorcoder.sublime-settings").add_on_change('use_textcommand',colorcoder.update_use_textcommand)
    colorcoder.update_scopes()
    colorcoder.update_use_textcommand()
    pp = sublime.packages_path()
    if not os.path.exists(pp+"/Colorcoder"):
        os.makedirs(pp+"/Colorcoder")

    firstrunfile = pp+"/Colorcoder/firstrun"
    if not os.path.exists(firstrunfile):
        colorshemeemodifier.maybefixscheme()
        open(firstrunfile, 'a').close()

    for wnd in sublime.windows():
        for view in wnd.views():
            view.settings().set('colorcode',True)
            view.run_command("colorcode")
