Colorcoder
==========
this plugin for Sublime Text will highlight every variable in its own, consistent color — feature known as semantic highlighting, variable-name highlighting, contextual highlighting — you name it.
![code from rosettacode.org used under GNU FDL 1.2](https://dl.dropboxusercontent.com/u/14672987/site/colorcoder/colorcoder.png)

Notice how all instances of `m_nValue` share the same color

Motivation
----------
 - [“Coding in color”](https://medium.com/p/3a6db2743a1e/) by [Evan Brooks](https://medium.com/@evnbr)
 - actually thought about something to improve the current highlighting system and accent the data flow
 - help dysgraphic/dyslexic coder

it is important to note i use a `crc8` hash of the variable name to give similar named variables distinct colors to improve typo recognition

Installation
------------
download the [zip-ball](https://github.com/vprimachenko/Sublime-Colorcoder/archive/master.zip) and unpack to `sublime\data\packages` or via [packageControl](https://sublime.wbond.net/)

On the first run plugin will cast magic to make everything work, it will even automatically reapply when change your color scheme (to turn this off set `auto_apply_on_scheme_change` to `false`). You can use `Tools`▶`Packages`▶`Colorcoder`▶` Tweak Colorcode on current color scheme` (or <kbd>CTRL</kbd><kbd>SHIFT</kbd><kbd>P</kbd> it) to modify the colors a bit 
(note: the plugin will not actually modify the scheme but create a modified copy in its own directory and apply it)

As few language definitions provided by Sublime are insufficient for optimal Colorcoder results i bundle tailored defintions. You can set them up as default via `language menu`▶`Open all with current extension as`▶`*** (Colorcode)` or copy/hardlink `Packages/Colorcoder/***.tmLanguage` to `Packages/***/***.tmLanguage`. You can also add more scopes for the plugin to colorize via the `scopes` setting. Colorcoder comes with a handy command `colorcoder_inspect_scope` which will print the scope of the token under text cursor to the console. You can bind it to a key (e.g. <kbd>CTRL</kbd><kbd>F12</kbd>) by adding following to `Preferences`▶`Key Bindings – User`

	{ "keys": ["ctrl+f12"], "command": "colorcoder_inspect_scope"},

Sometimes things we are interested in don't have distinct scope e.g. the variables in `Javascript` are only `source.js`. You would need to modify the `.tmLanguage`.

- First you need to obtain it - it is inside the same names `.sublime-package` file, which is a zip-archive
- now locate first instance of

		<key>patterns</key>
		<array>

it should be somewhere within first 50 lines
- use code folding to find where according `</array>` is
- place following right before it

		<dict>
			<key>comment</key>
			<string>colorize everything</string>
			<key>match</key>
			<string>\b\w+\b</string>
			<key>name</key>
			<string>colorize</string>
		</dict>

or modify the bundled `.tmLanguage` files, you probably would only need to replace the keywords

Contact
-------
you can reach me via email: [vprimachenko@ya.ru](mailto:vprimachenko@ya.ru), twitter: [@vprimachenko](https://twitter.com/vprimachenko) or visit the official irc channel [freenode.net#colorcoder](irc://irc.freenode.net/colorcoder) ([webchat](http://webchat.freenode.net/?channels=colorcoder))


