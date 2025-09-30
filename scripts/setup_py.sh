# Setup virtual environment
cd .. || exit
python3 -m venv ./venv
. venv/bin/activate

# Install packages
python3 -m pip install cryptography
python3 -m pip install web3
python3 -m pip install auto_cmake
python3 -m pip install auto_artifacts
python3 -m pip install requests
python3 -m pip install PyJWT
python3 -m pip install twine
