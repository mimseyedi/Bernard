# Bernard
 
Bernard is an assistant and application to customize the terminal to do the tasks you need, which can be run on all bash Unix shells.
Bernard consists of a script reader and a directory of scripts. With the help of script reader, Bernard can read and execute smaller programs by Python interpreter.
In this way, it will be easier to develop Bernard by writing small and separate programs.

## Table of Contents: <a class="anchor" id="contents"></a>
* [What is Bernard?](#bernard_what)
* [How was Bernard made?](#bernard_made)

    * [Bernard's first draft](#bernard_draft)

* [How to use Bernard?](#bernard_use)
* [Executable Bernard](#bernard_exe)
* [Development of Bernard](#bernard_dev)

    * [Rule 1: Bernard is always looking for the scripts directory](#rule1)
    * [Rule 2: Guides are required](#rule2)
    * [Rule 3: Do not disturb the settings](#rule3)
    * [Rule 4: All scripts must be inplace](#rule4)
    * [Rule 5: Don't forget the dependencies!](#rule5)


## What is Bernard? <a class="anchor" id="bernard_what"></a>
Bernard is a platform for executing Python scripts or subroutines that come in the form of commands with different parameters. Bernard has a central kernel that executes Python scripts stored in a directory of the same name, and can also download and install scripts from the repository. You can customize the terminal with bernard and create your commands. Bernard can be run on all bash Unix shells!


## How was Bernard made? <a class="anchor" id="bernard_made"></a>
Bernard's idea consists of obsession and practice.
I always wanted a personal terminal with my own commands. A terminal is all I need after the OS boots. A program that knows me and my needs and can be adjusted and developed accordingly.

That's why I decided to look at this idea as a challenge and exercise and start working.
First, I thought about several architectures for the construction of Bernard, and finally I came to the conclusion that the development of Bernard is the most important issue for me. That's why I decided to design Bernard's components separately. A program was supposed to run as a parent program and read and execute smaller programs through commands. This work helped to write more accurate and faster programs and also made it possible to install or update programs from the repository more easily.
I did this with Python because it was easier and more workable for me, and of course full of fun.

**This is the first draft of Bernard and the initial scripts:**

<img src="Bernard_design.png"/> <a class="anchor" id="bernard_draft"></a>

After I went through the process of implementing the basic design, I decided to write a installer for Bernard.
Now you can start here after reading or rejecting this boring story:

But first: 
Bernard is open source under the MIT license and you can easily use it
and make any changes you like to customize your terminal and share it with others.


* [Table of contents](#contents)


## How to use Bernard? <a class="anchor" id="bernard_use"></a>
To install Bernard, it is enough to download the bernard_installation.py file:
```
$ curl -o Bernard_installation.py https://raw.githubusercontent.com/mimseyedi/bernard/master/Bernard_installation.py
```

Then you need to run the installer file through the Python3 interpreter:
```
python Bernard_installation.py
```

Make the desired settings and wait for the required scripts and libraries to be downloaded and installed.

After the installation is complete, go to the Bernard directory and run the following command:
```
python Bernard.py
```

Bernard is now running on your terminal!
You can install and update new scripts with the help of install and update commands.
```
install script_name
update script_name
```

You can also use the -h parameter to find out the help of any command!
For example:
```
deldir -h
```


* [Table of contents](#contents)


## Executable Bernard: <a class="anchor" id="bernard_exe"></a>
If you want Bernard to become an executable directly in the terminal:

**first step:**

The first thing you’ll need to do is mark your Python script as executable in the file system, like so
```
$ chmod +x bernard.py
```

**The second step:**

Add an interpreter “shebang” in top of file
```
#!/usr/bin/env python
```

**The third step:**

Change the file extension to .command then run the file with double-click

for more information: https://dbader.org/blog/how-to-make-command-line-commands-with-python


* [Table of contents](#contents)


## Development of Bernard: <a class="anchor" id="bernard_dev"></a>
There are rules for the development of Bernard, if you want to be a part of the development of this program, you must follow them. I also encourage you to make your own terminal and make your own rules and have fun doing it.

### Rule 1: Bernard is always looking for the scripts directory <a class="anchor" id="rule1"></a>
All scripts or small programs that are executed by Bernard's script reader are located in the scripts directory, and Bernard will find them in the scripts directory by the file name of these scripts and execute them if they exist.
So please don't change the script directory name or path!
```
.
└── Bernard/
    ├── Bernard.py
    ├── logs.db
    ├── settings.json
    └── scripts/
        ├── cal.py
        ├── clear.py
        ├── date.py
        ├── deldir.py
        ├── delf.py
        ├── gcc.py
        └── hash.py
```
        
### Rule 2: Guides are required <a class="anchor" id="rule2"></a>
Every script that is written must accept a parameter called **-h** so that the usage guide and necessary explanations about the desired script or command can be received. You can easily control this parameter using **sys.argv**
```
items -h
```
output:
```
With the items command, you can see all items in directories.

Parameters:
-a show all items include hidden files
```



### Rule 3: Do not disturb the settings <a class="anchor" id="rule3"></a>
A json file called settings is located in the main location of the Bernard, which contains important information such as: home path, script directory path, root path and user password hash.
Please do not manipulate this file and do not change its path in any way.
To change this file, first familiarize yourself with its structure and do it as much as you can using the **settings** command.
```json
{"path_settings": {"scripts_path": "/a/b/c/Bernard/scripts", 
                   "home_path": "/a/b/c", 
                   "root_path": "a/b/c/Bernard"}, 
 "password": "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"}
```


### Rule 4: All scripts must be inplace <a class="anchor" id="rule4"></a>
All scripts must be inplace! In the sense that their final processing should be done by themselves and not return a value. Bernard's script reader is not able to receive data from scripts and can only call them to do their work.
So be careful! Forget the **return**!


### Rule 5: Don't forget the dependencies! <a class="anchor" id="rule5"></a>
If you want to use a non-standard library or module for the script you are writing, be sure to install it according to the desired protocols at the beginning of the script so as not to encounter an error.
However, it is better to use standard and reliable modules as much as you can.
```python
import sys
import subprocess

try:
    import rich
except ImportError as module:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', module.name], stdout=subprocess.DEVNULL)
```

another way:

```python
import sys
import subprocess
import pkg_resources

required = {'rich', 'prompt_toolkit'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
```
