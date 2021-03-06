# TinyCodeCounter
TinyCodeCounter is a [Sublime Text](https://www.sublimetext.com) plugin to show character count, show how close you are to 280 characters, and easily remove whitespace when writing tiny code to be posted on Twitter under [#tinycode](https://twitter.com/hashtag/tinycode), [#p5t](https://twitter.com/hashtag/p5t), [#つぶやきProcessing](https://twitter.com/hashtag/つぶやきProcessing), etc. 

## Installation

### Via Package Control (Recommended)

If you have [Package Control](https://packagecontrol.io/installation) installed, you can install TinyCodeCounter as follows:

1. Open the command palette: `cmd + shift + p` on Mac and `ctrl + shift + p` on Windows/Linux.
2. Search `Package Control: Install Package` and press `enter`.
3. Search `TinyCodeCounter` and press `enter`.

### Manually

Download and unpack, or git clone, the latest TinyCodeCounter release as `TinyCodeCounter` in the Sublime Text packages directory. You can find the packages directory by navigating to `Preferences > Browse Packages` in Sublime Text. On macOS or Linux, open a terminal and type:

```
cd /path/to/Sublime Text 3/Packages
git clone https://github.com/gkpotter/Sublime-TinyCodeCounter.git TinyCodeCounter
```
After installing manually, make sure to restart Sublime Text.

## Usage

### Character Counting
TinyCodeCounter looks for markers (by default #tinycode, #p5t, and #つぶやきProcessing) in files of specified languages (by default Javascript, Java, and Python) and counts characters in all lines preceeding and including the line containing the marker *not including whitespace.* The difference between the number of characters *not including whitespace* and the specified character limit (by default 280) is also displayed.

### Removing Whitespace
Clicking on the counter will copy all of the characters preceeding and including the line containing the marker *not including whitespace* to the clipboard.

For example given the following code, TinyCodeCounter displays after the marker at the end:

![example](./example.png)

After clicking on the counter, the following is copied to the clipboard:

```Javascript
F=[];p=0;draw=_=>{createCanvas(400,400);F.push([0,0,0]);F=F.slice(0,365);translate(200+40*cos(p),200+40*sin(p));rotate(p+=0.02);F.forEach(f=>text('🌸',f[1]=88*cos(t=(f[0]+=0.1))-48*cos(11*t/6),f[2]=88*sin(t)-48*sin(11*t/6)));text('💮',0,0)}//#tinycode #p5t #つぶやきProcessing
```

## Settings

All of the settings are documented in the [settings file](https://github.com/gkpotter/Sublime-TinyCodeCounter/blob/main/TinyCodeCounter.sublime-settings). You can override the defaults by navigating to `Preferences > Package Settings > TinyCodeCounter > Settings` in Sublime Text.
