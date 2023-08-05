#itunes_file_system (itunesfs)
**Script for generating an iTunes Connect package (.itmsp) straight from your asset folder**

***itunesfs*** performs the following conversion:

.![pipeline](http://raw.github.com/evilwindowdog/itunesfs/master/README_PIPELINE.png)

The task of managing and uploading the localised assets of your iOS app in a tedious one. When the number of supported languages increases, the effort needed via the web interface of [iTunes Connect](<https://itunesconnect.apple.com>) is increased accordingly. Apple's **iTMSTransporter** tool gives you the ability to download and upload App Store Packages (.itmsp) from the command line. However, altering the data requires an XML file manipulation. 

An easier way is to use [**itunes_transporter_generator (itmsp)**](<https://github.com/colinhumber/itunes_transporter_generator>) , which lets you add your metadata in a **YAML** app configuration. Running *itmsp* converts the YAML file to an **.itmsp package** that can be uploaded using iTMSTransporter. However, when multiple localized assets are involved, this solution leads to editing a huge unmanageable YAML file.

This tool, **itunes_file_system (itunesfs)**, lets you organise your assets (screenshots, description, keywords etc) in a specific file hierarchy. Running *itunesfs* produces an intermediate YAML configuration file and, if you have *itmsp* installed, it uses it to generate the final .itmsp package. You can then uploaded it on iTunes Connect using iTMSTransporter.


 

##Installation

1. Download and install [**python 3**](<http://www.python.org/download/>). Python 2.x is not supported at the moment.
1. If you have **PIP** [installed](<http://pip.readthedocs.org/en/latest/installing.html>) for Python 3 type:

		$ pip3 install itunesfs  
Otherwise download the source from <https://pypi.python.org/pypi/itunesfs/> and type:

		$ sudo python3 setup.py install  

1. *(optional)* Install [itunes_transporter_generator](<https://github.com/colinhumber/itunes_transporter_generator>) running:

		$ gem install itunes_transporter_generator
		
*Note that you will need apple's iTMSTransporter, to upload the package at iTunes. If you have Xcode installed, you already have this tool on your system.*
		
##Usage

###Organise your folders

Your files have to be under a root folder and organised as shown in the "example" app, which is included in the package. Note that all files should be encoded using **UTF-8**.

.![file hierarchy](http://raw.github.com/evilwindowdog/itunesfs/master/README_FILE_HIERARCHY.png)

* At the root folder, the **config_app.yaml** contains the basic configuration for the app. 
* One or more **versions** can exist as folders under the root folder. 
* Each version can have one or more **locales**. The "master" locale, that should always be available, is "en-US". 
* Each locale can have:
    * the **config-local.yaml**, that contains locale related configuration such as the title of the app
    * the **description.txt**, that holds the App Store description
    * the **keywords.txt**, that is a comma separated list of the keywords. The spaces around each keyword, will be erased. Also a warning will be produced when they exceed the App Store 100 character limit.
    * a **screenshot** folder. It can contain ipad, iphone_3.5in, iphone_4in, iphone_4.7in or iphone_5.5in subfolders. Each device subfolder can have one or more screenshot files. The order that they will be used is alphabetical.

The "en-US" locale must always contain the following files: **config-local.yaml**, **description.txt**, **keywords.txt**. Even though screenshots are optional, itmsp will fail to produce the .itmsp without them.

For the other locales, these files are **optional**. If a file is not found, the corresponding "en-US" file will be used instead.



###Generate the .itmsp

If your Python 3's bin folder is in yout PATH, then **itunesfs** can be executed from the command line.

####To generate the .itmsp package

If you have installed *itmsp*, *itunesfs* will call it by default to generate the package from the YAML file.:

		$ itunesfs <path_to_asset_folder>

####To generate *only* the intermediate YAML configuration file

		$ itunesfs <path_to_asset_folder> -t YAML
		
e.g. `$itunesfs /example -t YAML`: this parses the "example" directory and generates an *output.yaml* file under it. 

If you want to change the output directory use:

		$ itunesfs <path_to_asset_folder> -o <output_path> -t YAML
This will also copy the screenshot files.


		
###Verifying and uploading the package

Here's a really small guide for Apple's iTMSTransporter.

For ease of use, add this alias to your bash profile.

* run: ``$open ~/.bash_profile``
* add this line and save: ``alias iTMSTransporter='`xcode-select --print-path`/../Applications/Application\ Loader.app/Contents/MacOS/itms/bin/iTMSTransporter'``

####Using iTMSTransporter:

Remember to escape with "\" special characters like "$" in the password field. Also the path can be either the path for one package or the path for a folder containing one or more packages.

To verify the package:
	
	$ iTMSTransporter -m verify  -u <username> -p <password>  -f <path_for_package>

To uplaod the package:
	
	$ iTMSTransporter -m upload  -u <username> -p <password>  -f <path_for_package>
	
More information: <http://stackoverflow.com/a/17824838>