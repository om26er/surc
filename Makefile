default:
	@echo "Targets:"
	@echo "  deps"
	@echo "  run"
	@echo "  clean"

deps:
	sudo apt install curl jq wget -y
	pip3 install -r requirements.txt

run:
	python3 -u surc.py

clean:
	rm -f surc.sqlite
