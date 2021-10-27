.PHONY: clean-pyc clean-build

	@echo "    clean-pyc"
	@echo "        Remove python artifacts."

run:
	#  make SUBNET=192.168.0.0/24 CONCURRENT=8 TIMEOUT=2
	python pingdiscover.py  --subnet $(SUBNET) --concurrent $(CONCURRENT) --timeout $(TIMEOUT)