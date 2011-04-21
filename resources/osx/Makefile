all:
	python build.py -c openlp.cfg

view:
	python build.py -c openlp.cfg --package-view --compress-view

package:

	python build.py -c openlp.cfg --package --package-view

bundle:

	python build.py -c openlp.cfg --compress --compress-view

clean:
	# remove old configuration files
	rm -f openlp.spec
	rm -f Info.plist
	rm -f .version

	# remove old build artifacts
	rm -rf build
	rm -rf dist
	rm -rf Macopenlp.app
	rm -rf OpenLP.app
	rm -f warnopenlp.txt
	rm -f *dmg
        
