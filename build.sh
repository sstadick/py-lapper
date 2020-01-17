# Update the version number

cd docs
make html
cd ..

poetry run pytest
poetry run coverage -m pytest
rm coverage.svg
poetry run coverage-badge.py -o coverage.svg

poetry build
poetry publish


