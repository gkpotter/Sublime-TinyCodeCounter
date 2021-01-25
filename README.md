# TinyCodeCounter
TinyCodeCounter is [Sublime Text](https://www.sublimetext.com) plugin to show character count and easily remove whitespace when writing tiny code to be posted on Twitter under [#tinycode](https://twitter.com/hashtag/tinycode), [#p5t](https://twitter.com/hashtag/p5t), [#p5js](https://twitter.com/hashtag/p5js), [#つぶやきProcessing](https://twitter.com/hashtag/つぶやきProcessing), etc. 

## Installation

Download and unpack, or git clone, the latest TinyCodeCounter release as `TinyCodeCounter` in the Sublime Text packages directory. You can find the packages directory by navigating to `Preferences > Browse Packages` in Sublime Text. On macOS or Linux, open a terminal and type:

```
cd /path/to/Sublime Text 3/Packages
git clone https://github.com/gkpotter/Sublime-TinyCodeCounter.git TinyCodeCounter
```

## Usage

### Character Counting
TinyCodeCounter looks for markers (by default #tinycode and the other hashtags listed above) and counts characters in all lines preceeding and including the line containing the marker *not including whitespace.* The offset from the specified character limit (by default 280) is also displayed.

### Removing Whitespace
Clicking on the counter will copy all lines preceeding and including the line containing the marker *not including whitespace* to the clipboard.

For example given the following code, TinyCodeCounter displays after the marker at the end:

<img src="https://github.com/gkpotter/Sublime-TinyCodeCounter/blob/main/example.png" width="500">

After clicking on the counter, the following is copied to the clipboard:

```Javascript
setup=_=>{F=[],p=0,s=sin,c=cos};draw=_=>{createCanvas(400,400);F.push([0,0,0]);F=F.slice(0,365);translate(200+40*c(p),200+40*s(p));rotate(p+=0.02);F.forEach(f=>text('🌸',f[1]=88*c(t=(f[0]+=0.1))-48*c(11*t/6),f[2]=88*s(t)-48*s(11*t/6)));text('💮',0,0)}//#tinycode #p5t
```

## Settings

All of the settings are documented in the [settings file](https://github.com/gkpotter/Sublime-TinyCodeCounter/blob/main/TinyCodeCounter.sublime-settings).
