.PHONY: dry clean fmt

PY=python3

 dry:
	$(PY) src/gbclean.py --dry-run --days 120

 clean:
	$(PY) src/gbclean.py --days 120 --delete-merged --yes

 fmt:
	@autopep8 -i src/gbclean.py || true
