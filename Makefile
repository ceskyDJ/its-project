.PHONY: all pack clean

all: pack

pack:
	zip -j xsmahe01.zip features/*.feature README.md

clean:
	rm xsmahe01.zip
