re = \w

kill:
	ps aux| egrep "dev.py -s$(re)" | awk '{print $$2}' | xargs kill

# west:
# 	fab West deploy:debug=

cs:
	fab Crawlers deploy

req:
	# pip install --upgrade pip
	pip install -r requirements.txt

clean:
	find . -name "*.pyc" -exec rm -rf {} \;
