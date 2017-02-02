HOST=mahiabd
ADB=/home/maho/.buildozer/android/platform/android-sdk-20/platform-tools/adb
BUILDOZER=buildozer

#export VERSION_kivy=master
export URL_kivy=https://github.com/mahomahomaho/kivy/archive/master.zip
export URL_kivent_core=https://github.com/mahomahomaho/kivent/archive/my22dev.zip
export P4A_kivent_core_DIR=$(CURDIR)/./kivent


#all: build ssh_deploy ssh_run ssh_log
all: buildrunlog

localfullclean: 
	rm -rf .buildozer

deepclean: localfullclean
	rm -rf $(HOME)/.buildozer bin

build: 
	$(BUILDOZER) --verbose android_new debug 

deploy: 
	$(BUILDOZER) --verbose android_new deploy 

run: 
	$(BUILDOZER) --verbose android_new run

log:
	$(BUILDOZER) --verbose android_new logcat  | egrep --color 'python|maho|khamster|$$'

buildrunlog: 
	$(BUILDOZER) android_new debug deploy run logcat 

dopip:
	pip install --upgrade --user pip
	pip install --user pexpect
	pip install --user --upgrade buildozer cython colorama appdirs sh

connect_adb:
	$(ADB) connect $(HOST)
	$(ADB) devices

devices:
	$(ADB) devices

