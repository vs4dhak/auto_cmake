# Set python
cd .. || exit
python3 -m venv ./venv
. venv/bin/activate

# Build
rm -rf dist
python3 setup.py sdist
twine upload dist/*