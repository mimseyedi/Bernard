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
    
    * [Rule 1: Everything starts in the init function](#rule1)
    * [Rule 2: Bernard is always looking for the scripts directory](#rule2)
    * [Rule 3: Guides are required](#rule3)
    * [Rule 4: Do not disturb the settings](#rule4)
    * [Rule 5: All scripts must be inplace](#rule5)
    * [Rule 6: Don't forget the dependencies!](#rule6)
    * [Rule 7: Always use the pathlib module for routing](#rule7)
    * [Rule 8: Versatility of terminals](#rule8)



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
$ curl -o Bernard_installation.py https://raw.githubusercontent.com/mimseyedi/Bernard/master/Bernard_installation.py
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
You can install and update new scripts with the help of scripts command:
```
scripts install script_name
scripts update script_name
```

Also you can find new scripts:
```
scripts -n
```

Or find out about available updates:
```
scripts -u
```


You can also use the -h parameter to find out the help of any command!
For example:
```
trans -h
```
Output:
```
With the trans command, you can translate words into different 
natural languages or receive a complete file with the translated 
output.

Parameters:
trans <word> <language> -> exmaple: trans hello persian
-d detect language
-f read file to translate
-fo translate file with .txt output
```


* [Table of contents](#contents)


## Executable Bernard: <a class="anchor" id="bernard_exe"></a>
If you want Bernard to become an executable directly in the terminal:

### In Unix Systems (Linux/macOS):
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

### In Windows:
On Windows systems, there is no notion of an “executable mode”. The Python installer automatically associates .py files with python.exe so that a double-click on a Python file will run it as a script. The extension can also be .pyw, in that case, the console window that normally appears is suppressed.

Also you can use **pyinstaller** module:
```
python -m pip install pyinstaller
```

* [Table of contents](#contents)


## Development of Bernard: <a class="anchor" id="bernard_dev"></a>
There are rules for the development of Bernard, if you want to be a part of the development of this program, you must follow them. I also encourage you to make your own terminal and make your own rules and have fun doing it.

## Rule 1: Everything starts in the init function <a class="anchor" id="rule1"></a>
For easier reading, the starting point of the program is from the init function.
Always write your executable code from this point:
```python
def init():
    #start here
    pass

if __name__ == "__main__":
    init()
```


## Rule 2: Bernard is always looking for the scripts directory <a class="anchor" id="rule2"></a>
All scripts or small programs that are executed by Bernard's script reader are located in the scripts directory, and Bernard will find them in the scripts directory by the file name of these scripts and execute them if they exist.
So please don't change the script directory name or path!
```
.
└── Bernard/
    ├── Bernard.py
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
        
## Rule 3: Guides are required <a class="anchor" id="rule3"></a>
Every script that is written must accept a parameter called **-h** so that the usage guide and necessary explanations about the desired script or command can be received. You can easily control this parameter using **sys.argv**
```
orgdir -h
```
output:
```
With the orgdir command, you can organize and sort your 
directories in two classic or custom ways.

Parameters:
-c classic way -> example: orgdir -c
-x custom way -> exmaple: orgdir -x .pdf Doc
```



## Rule 4: Do not disturb the settings <a class="anchor" id="rule4"></a>
A json file called settings is located in the main location of the Bernard, which contains important information such as: home path, script directory path, root path and user password hash.
Please do not manipulate this file and do not change its path in any way.
To change this file, first familiarize yourself with its structure and do it as much as you can using the **settings** command.
```json
{"path_settings": {"scripts_path": "/a/b/c/Bernard/scripts", 
                   "home_path": "/a/b/c", 
                   "root_path": "a/b/c/Bernard"}, 
 "password": "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"}
```


## Rule 5: All scripts must be inplace <a class="anchor" id="rule5"></a>
All scripts must be inplace! In the sense that their final processing should be done by themselves and not return a value. Bernard's script reader is not able to receive data from scripts and can only call them to do their work.
So be careful! Forget the **return**!


## Rule 6: Don't forget the dependencies! <a class="anchor" id="rule6"></a>
If you want to use a non-standard library or module for the script you are writing, be sure to install it according to the desired protocols at the beginning of the script so as not to encounter an error.
However, it is better to use standard and reliable modules as much as you can.
```python
import sys
import subprocess

try:
    import rich
except ImportError as module:
    python_interpreter = sys.executable
    subprocess.run([python_interpreter, '-m', 'pip', 'install', module.name], stdout=subprocess.DEVNULL)
finally:
    import rich
```

Another way:

```python
import sys
import subprocess
import pkg_resources

required = {'rich', 'requests'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python_interpreter = sys.executable
    subprocess.check_call([python_interpreter, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

```

## Rule 7: Always use the pathlib module for routing

Since paths or addresses are regulated differently in different operating systems, these paths must be written dynamically to run without problems. For this, the **pathlib** module is the best and simplest solution. With this module, you can connect the addresses dynamically and create the desired route. This module correctly corrects the path according to the operating system on which the program is running.

For example:
```python
import os
from pathlib import Path

print(Path(os.getcwd(), "test.txt"))
```

Output in Unix systems(Linux/macOS):
```
/home/user/Desktop/test.txt
```

Output in Windows:
```
C:\Users\user\Desktop\test.txt
```

For more information visit: https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f

## Rule 8: Versatility of terminals <a class="anchor" id="rule8"></a>
If you want to use a specific command in the terminal in your scripts, make sure that this command exists in all operating systems, otherwise you have to do the adaptation process:
```python
import platform
import subprocess

os = platform.system()

if os in ["Linux", "Darwin"]:
    subprocess.run(["clear"])
    
elif os == "Windows":
    subprocess.run(["cls"])
```



