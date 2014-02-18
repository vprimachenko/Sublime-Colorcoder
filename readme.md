Colorcoder
==========
this plugin for Sublime Text will highlight every variable in its own, consistent color—feature known as semantic highlighting, variable-name highlighting, contextual highlighting—you name it.
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

On the first run plugin will cast magic to make everything work, but in the event you ever change your color scheme you should use `Tools`▶`Packages`▶`Colorcoder`▶` Add Colorcode to current color scheme`  (or <kbd>CTRL</kbd><kbd>SHIFT</kbd><kbd>P</kbd> it) to make everything nice again 
(note: the plugin will not actually modify the scheme but create a modified copy in its own directory and apply it)

As few language defintions provided by Sublime are insufficient for optimal Colorcoder results i bundle tailored defintions. You can set them up as default via `language menu`▶`Open all with current extension as`▶`*** (Colorcode)` or copy/hardlink `Packages/Colorcoder/***.tmLanguage` to `Packages/***/***.tmLanguage`

Extension
----------
it should work as is with most languages, to highlight even more tokens you only need to add tokens with lexical scope `colorize` eg:

	<dict>
		<key>comment</key>
		<string>this is the important thing matching the varibles and stuff, these are the tokens we will colorize</string>
		<key>match</key>
		<string>\b\w+\b</string>
		<key>name</key>
		<string>entity.name.variable.c++</string>
	</dict>

(c.f. bundled `.tmLanguage` files, you probably would only need to replace the keywords)
