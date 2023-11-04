## Python Simple Email Sender
Python Simple Fast Email Sending without External Library 

GitHub Repo: [https://github.com/sannjayy/py-simple-email](https://github.com/sannjayy/py-simple-email)
### Installaion
Do the following in your virtualenv:

`pip install py-simple-email`

**Import:**
```
from py_simple_email import Email
```
---

**Minimal Code Example:**
```python
from py_simple_email import Email

# SMTP Configuration:
email = Email( 
    EMAIL_HOST = 'email-smtp.ap-south-1.amazonaws.com', 
    EMAIL_HOST_USER = 'XXXXXXXXXXXXXX', 
    EMAIL_HOST_PASSWORD = 'XXXXXXXXXXXXXXXXXXX', 
    DEFAULT_FROM_EMAIL = 'Sanjay Sikdar <hello@sanjaysikdar.dev>',
    EMAIL_PORT= 587, 
    EMAIL_USE_TLS = True,
)

# Sending Email:
email.send(
    to_email='me@sanjaysikdar.dev',
    subject='Test Mail',
    msg='Hello from Simple Email.',
)
```

---

**Sending Fancy Emails:**

```python

html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://read.sanjaysikdar.dev">Sanjay Sikdar</a> 
       has many great tutorials.
    </p>
  </body>
</html>
"""

email.send(
    from_email='host@sanjaysikdar.dev',
    to_email='me@sanjaysikdar.dev',
    subject='HTML Test E-email',
    msg=html,
    is_html=True
)

```

---

[![](https://img.shields.io/github/followers/sannjayy?style=social)](https://github.com/sannjayy)  
Developed by *Sanjay Sikdar*.   
- 📫 me@sanjaysikdar.dev



