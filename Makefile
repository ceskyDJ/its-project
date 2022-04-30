.PHONY: all pack clean test

all: pack

pack:
	zip -j xsmahe01.zip features/*.feature README.md

pack2:
	zip -j xsmahe01.zip feafures/*.feature feafures/environment.py features/steps/*.py requirements.txt report.pdf

clean:
	rm xsmahe01.zip

test:
	mkdir tmp
	mv xsmahe01.zip tmp
	cd tmp && unzip xsmahe01.zip
	cd tmp && [-f requirements.txt ] && pip3 install-r requirements.txt
	cd tmp && docker-compose up -d
	cd tmp && behave
	@echo -e "\033[0;32mFinal ZIP archive is OK\033[0m"
	rm -rf tmp
