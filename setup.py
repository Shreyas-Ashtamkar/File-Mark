from setuptools import setup, find_packages

long_description = """
# File-Mark

<b>Filemark</b> This is a Simple Files' Bookmarks Manager.

Making developers' life easy by helping to bookmark a certain folder and opening smartly opening the requiredPP softwares on basis of what development you do. 

The open-the-file behavior is configurable easily. 

The Main purpose of this is to handle <b>bookmarking</b> of files/folders.

<br>

***
<br>

## INSTALLATION
```shell
sudo pip install filemark
```

***
<br>

## SYNOPSIS

```shell
usage: filemark [OPTION] [FILE_OR_FOLDER]
```

***
<br>

## OPTIONS:

| Short |     Options       |        ARGS        |                         Description                          |
| ----- | ----------------- |--------------------| ------------------------------------------------------------ |
| `-v`  |   `--version`     |                    |  Display Version Information of Command<br>                  |
| `-h`  |   `--help`        |                    |  Display this HELP message.<br>                              |
| `-a`  |   `--add`         |    FILE \| FOLDER  |  Bookmark some particular File or Folder <br>                |
| `-s`  |   `--show`        |      BOOKMARK      |  Show bookmarked items <br>                                  |
|       |   `--show-only`   |                    |  Show details of some specific bookmarked item <br>          |
|       |   `--show-all`    |                    |  Show all the currently set bookmarks. <br>                  |
| `-o`  |   `--open`        |      BOOKMARK      |  Open a specific bookmarked file location. Open IDE. <br>    |
| `-a`  |   `--delete`      |    FILE \| FOLDER  |  Delete a bookmarked entry<br>                               |
|       |   `--full-path`   |    TRUE \| FALSE   |  Extra Flag with --show to entire path (not short). <br>     |
|       |   `--not-smart`   |    TRUE \| FALSE   |  Extra Flag with --open for terminal-open only. <br>         |


***
<br>

## EXAMPLE :

```python
#COMING SOON
```
"""

setup(
	name='filemark',
	version='0.1.0',
	license='MIT',
	
	description='A Python-built Command line tool for bookmarking and smartly-reopening project folders (for developers)',
	long_description=long_description,
    long_description_content_type="text/markdown",
    
    author="Shreyas Ashtamkar",
    author_email="shreyu@programmer.net",
    url="https://github.com/Shreyas-Ashtamkar/File-Mark",

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],

	python_requires='>=3.6',
    install_requires=['autopep8>=1.5.4', 'pycodestyle>=2.6.0', 'tabulate>=0.8.7', 'toml>=0.10.2'],

    packages=find_packages(),
    py_modules=['filemark.filemarkutils'],

    entry_points={
		'console_scripts': ['filemark=filemark.command_line:main'],
  	},

  	include_package_data=True,
  	zip_safe=False
)
