#Colorcoder
This plugin for Sublime Text will highlight every variable in its own, consistent color — feature known as semantic highlighting, variable-name highlighting, contextual highlighting — you name it.
![code from rosettacode.org used under GNU FDL 1.2](https://dl.dropboxusercontent.com/u/14672987/site/colorcoder/colorcoder.png)

Notice how all instances of `m_nValue` share the same color

##Motivation
 - [“Coding in color”](https://medium.com/p/3a6db2743a1e/) by [Evan Brooks](https://medium.com/@evnbr)
 - actually thought about something to improve the current highlighting system and accent the data flow
 - help dysgraphic/dyslexic coder

it is important to note i use a `crc8` hash of the variable name to give similar named variables distinct colors to improve typo recognition

##Installation
Download the [zip-ball](https://github.com/vprimachenko/Sublime-Colorcoder/archive/master.zip) and unpack to `sublime\data\packages` or via [packageControl](https://sublime.wbond.net/). Please make sure to name the resulting folder `Colorcoder` not ~~`Sublime-Colorcoder`~~.

To properly work Colorcoder needs an appropriately modified color scheme. On the first run plugin will try its best to automatically modify your current scheme. :grey_exclamation: the plugin will not actually modify the scheme but create a modified copy in its own directory and apply it. 
You can use `Tools`▶`Packages`▶`Colorcoder`▶` Tweak Colorcode on current color scheme` (or <kbd>CTRL</kbd><kbd>SHIFT</kbd><kbd>P</kbd> it) to modify the colors a bit (you can change the lightness and saturation).
Colorcoder also needs a "good" language definition, which it does not activate automatically but leaves you the choice to do so, read below for more.

##Supported Languages
As the few language definitions provided by Sublime are insufficient for optimal Colorcoder results I bundle tailored definitions. So far it's

 - `C++`
 - `Python`
 - `Lua`
 - `Go`
 - `Ruby`
 - `CoffeeScript` ([via](https://github.com/aponxi/sublime-better-coffeescript/blob/master/CoffeeScript.tmLanguage) by @aponxi)

for `JavaScript` please use the [`JavaScript Next` package](https://github.com/Benvie/JavaScriptNext.tmLanguage).

You can set them up as default via `language menu`▶`Open all with current extension as`▶`Colorcoder`▶`… (Colorcoded)` or copy them to appropriate folder (erg. `Packages/Colorcoder/Python (Colorcoded).tmLanguage` to `Packages/Python/Python.tmLanguage`.

 You can also add more scopes for the plugin to colorize via the `scopes` setting. Colorcoder comes with a handy command `colorcoder_inspect_scope` which will print the scope of the token under text cursor to the console. You can bind it to a key (e.g. <kbd>CTRL</kbd><kbd>F12</kbd>) by adding following to `Preferences`▶`Key Bindings – User`

	{ "keys": ["ctrl+f12"], "command": "colorcoder_inspect_scope"},

Sometimes things we are interested in don't have distinct scope e.g. the variables in `Javascript` are only `source.js`. You would need to modify the `.tmLanguage`.

- First you need to obtain it - it is inside the same names `.sublime-package` file, which is a zip-archive
- now locate the first instance of

		<key>patterns</key>
		<array>

it should be somewhere within the first 50–100 lines
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

##Options
You can turn the highlighting off per view via `View`▶`Colorcode this view`.
Colorcoder also might slow down the editor when highlighting huge files, so it will turn itself off once the file has exceeded the `max_size` (the check happens when you save the file or reactivate the view). You can force it to highlight the file nevertheless via said menu item (which will read `Colorcoding may hurt performance, File is large` now)
Default (faster) highlighting method makes the undo work letterwise, you can change this by setting `use_fast_highlighting_but_undo_typing_letterwise` to false. Colorcoder will then use alternative engine, which does not interfer with undo, but work somewhat slower on large files. You might want to tune `max_size` lower then.
Colorcoder allows you to specify white- and blacklist for file-types to highlight: the settings are `enabled_for` and `disabled_for`. If `enabled_for` is present in the config only those file-types will be highlighted, `disabled_for` won't be highlighted even if present in whitelist.
Finally :exclamation: if you use some plugins which change the color scheme based on time, or filename, or modify the schemes you better turn the `auto_apply_on_scheme_change` off, or the plugin conflict may result in an endless loop which will lock the editor. You can always change the settings even when sublime is not running.

##Contact
You can reach me via email: [vprimachenko@ya.ru](mailto:vprimachenko@ya.ru), twitter: [@vprimachenko](https://twitter.com/vprimachenko) or visit the official irc channel [freenode.net#colorcoder](irc://irc.freenode.net/colorcoder) ([webchat](http://webchat.freenode.net/?channels=colorcoder)). If Colorcoder was usefull to you i greatly appreciate a donation via Bitcoin [1DzZ1thGTHubRzoxEeDCJnJZwgFpna6jQk](bitcoin:1DzZ1thGTHubRzoxEeDCJnJZwgFpna6jQk).
