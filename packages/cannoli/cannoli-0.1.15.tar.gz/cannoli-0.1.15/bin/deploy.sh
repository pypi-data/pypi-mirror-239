cd ..
git add --all
git commit -m "updated"
git push origin dev 


rm -rf dist
rm -rf cannoli.egg-info
#python3 -m build
python3 setup.py sdist
python3 -m twine upload dist/* --verbose
