
#!/usr/bin/python
import os
import sys
sys.path.insert(0, '/var/www/html/captcha')
from captcha import app as application
application.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
if __name__ == "__main__":
    application.run(debug=True,host='0.0.0.0',port=80)
