all:
	zip -r rek.zip lib/python3.6/site-packages
	zip -g rek.zip lambda_function.py
