[![Actions Status](https://github.com/botlabsDev/npkpy/workflows/Pytest/badge.svg)](https://github.com/botlabsDev/npkpy/actions)
[![codecov](https://codecov.io/gh/botlabsDev/npkpy/branch/master/graph/badge.svg?token=4ns6uIqoln)](https://codecov.io/gh/botlabsDev/npkpy)



# npkPy
The npkPy package module is an unpacking tool for MikroTiks custom NPK container format. The tool is capable 
to display to the content of any NPK package and to export all container.

["NPK stands for MikroTik RouterOS upgrade package"](https://whatis.techtarget.com/fileformat/NPK-MikroTik-RouterOS-upgrade-package)
and since there is no solid unpacking tool for the format available, I want to share my approach of it.
The format, in general, is used by MikroTik to install and update the software on MikroTiks routerOs systems.

NPK packages can be found here: [MikroTik Archive](https://mikrotik.com/download/archive)

The code covers the ability to modify the container payload. Yet, this ability won't be available for cli.
Please be aware, that you can't create or modify __valid__ packages [since they are signed](https://forum.mikrotik.com/viewtopic.php?t=87126). 

```
All recent packages are signed with EC-KCDSA signature, 
and there's no way to create a valid npk file unless you know a secret key.
```

## Usage

```
$ npkPy is an unpacking tool for MikroTiks custom NPK container format

optional arguments:
  -h, --help            show this help message and exit

input:
  --files FILES         Select one or more files to process
  --srcFolder SRCFOLDER
                        Process all NPK files found recursively in given source folder.
  --glob GLOB           Simple glob. Filter files from --srcFolder which match the given string.

output:
  --dstFolder DSTFOLDER
                        Extract container into given folder

actions:
  --showContainer       List all container from selected NPK files
  --exportAll           Export all container from selected NPK files
  --exportSquashFs      Export all SquashFs container from selected NPK files
  --exportZlib          Export all Zlib compressed container from selected NPK files

```

Common understanding: A file represents an NPK package with multiple containers. 
Each container 'contains' payloads like descriptions, SquashFs images or Zlib compressed data.

## Other unpacking tools 
If npkPy does not work for you, check out older approaches of NPK unpacking tools:
* [mikrotik-npk](https://github.com/kost/mikrotik-npk)
* [npk-tools](https://github.com/rsa9000/npk-tools)




