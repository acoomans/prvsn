prvsn manual
============

## Runbooks

A configuration is called a `runbook`. Runbooks are just python files. Extra files used by the runbook are stored in a `files` directory.

	|- my_runbook.py
	|- files
	   |- httpd.conf
	   |- ...

### Tasks

Runbooks are composed of tasks.

Common task options include:

- `secure`: no output will be shown on console nor logs. 

#### Command Tasks

##### command(interpreter, cmd)

Run command in given interpreter.

##### bash(cmd)

Run command in bash.

    bash('echo "hello"')

	bash('''
	    echo "hello"
	    ls
	    ps
	''')

#### File Extension Handler Tasks

##### file_handler()

(mac only) 
Associate an application with a file extension.

    file_handler('.txt', 'com.macromates.TextMate')

The application's identifier can be found with:

    mdls -name kMDItemCFBundleIdentifier -r /Applications/TextMate.app

#### File Tasks

##### mkdir(path)

Create all directories, similar to bash's `mkdir -p`.

    mkdir(path, owner, group)

##### file(src, dst, replacements={}, owner, group)

Copy a file. `source` can either be a URL or a file's path relative to the role's `files` directory.

	file('httpd.conf', '/etc/httpd.conf')
	
	file(
	    src='http://example.org/httpd.conf', 
	    dst='/etc/httpd.conf'
	)

Replacements rules can be specified, so the file can be used as a template.

	file(
		src='http://example.org/httpd.conf', 
	    dst='/etc/httpd.conf',
		replacements={
		    'MY_IPADDRESS': '192.168.0.1'
		}
	)

##### file_contains(path, string, owner, group)

Append `string` to the file at `path` if `string` is not already in file.

#### Hostname tasks

##### hostname(name)

Set the hostname.

    hostname('my_machine')

#### Kernel Tasks

##### module(name)

(linux only)
Adds and loads a module.

	module('v4l')

#### Package Tasks

##### package(name, action)

Manage packages. This command will use the first package manager it finds.

    package('vim')

If multiple managers are present, it is possible to explicitly specify which to use as below.

##### homebrew_package(name)

(mac only)
Manage packages with homebrew.

##### cask_package(name)

(mac only)
Manage packages with homebrew cask.

##### mac_app_store(name)

(mac only)
Manage packages with the Apple app store. Might require signing in, either through the App store app or command line.

    mac_app_store_signin()

    mac_app_store('937984704')

Application identifiers can be found with:
    
    mas search app_name

##### apt_package(name)

Manage packages with APT.

##### yum_package(name)

Manage packages Yum.


### Helpers

Helpers do not alter the system. They only return information.

#### User Helpers

##### real_home()

Returns the home of the user, ignoring sudo.

##### real_user()

Returns the name of the user, ignoring sudo.


### Command line

#### init

Creates a new runbook.

    prvsn init path/to/runbook.py
    
Additional files can be added to a `files` directory in the same directory as the runbook.

#### run

Default command.
Run a runbook. By default, uses `runbook.py` if none was specified.

    prvsn run runbook.py
    
 Alternatively, it is possible to specify a package:
 
    prvsn run package.pyz

By default, runs as currently logged in user. `--sudo` can be specified to provision as root.

By default, runs on the local host. A remote target host can be specified:

    prvsn run runbook.py 192.168.0.1

When provisioning a remote host, prvsn will execute the following steps:

1. copy ssh keys
2. create a package 
3. copy the package
4. run the package
    
A ssh public key will be installed on the remote host (if no key exists, one is created). To disable this behavior, use `--no-copy-keys`.

#### package

Creates an executable package with the runbook, its files and the bootstrap. The default package name is `package.pyz`.

    prvsn package path/to/runbook.py -o package.pyz

The package can then be run independently:

    python mypackage.pyz