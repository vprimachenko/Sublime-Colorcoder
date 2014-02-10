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

The plugin need a special language definition `.tmLanguage` file and a special highlighting `.tmTheme` file. It is bundled with appropriately modified `C++` language file (forked from [Isaac Muse](https://github.com/facelessuser)s [`better C++`](https://github.com/facelessuser/sublime-languages/blob/master/Better%20C++/C++.tmLanguage)) and modified `Obisidian` color scheme

Extension
----------
To make it work with other languages you only need to provide new lexical scope `variable.colorcode` eg:

	<dict>
		<key>comment</key>
		<string>this is the important thing matching the varibles and stuff, these are the tokens we will colorize</string>
		<key>match</key>
		<string>\b\w+\b</string>
		<key>name</key>
		<string>variable.colorcode.c++</string>
	</dict>

for other color schemes you need to specify `256` highlight rules ranging from `cc0x0` to `cc0xff` eg:

	<dict>
		<key>scope</key>
		<string>cc0xef</string>
		<key>settings</key>
		<dict>
			<key>foreground</key>
			<string>#cc668f</string>
			<key>background</key>
			<string>#293133</string>
		</dict>
	</dict>

background here is 1 color unit less than the overall text background (here it was `#293134`)

Feel free to submit a push request if you add this to any language or color scheme.
