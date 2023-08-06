from setuptools import setup, find_packages
import multimail

TDIR = 'multimail/templates/multimail/'
setup(
    name = 'django-multimail',
    version = multimail.__version__,
    description = 'Enable multiple email addresses per user in Django',
    keywords = 'django, e-mail, email, multimail, multiple addresses',
    author = multimail.__author__,
    author_email = multimail.__email__,
    url = multimail.__url__,
    requires = [],
    packages = find_packages(),
    classifiers=[
          'Framework :: Django',
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: %s' % multimail.__license__,
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
    #data_files = [
    include_package_data = True,
    package_data = {
        'multimail/templates/multimail':
            [ TDIR + 'base_multimail_email.html',
              TDIR + 'base_multimail_email.txt',
              TDIR + 'verification_email.html',
              TDIR + 'verification_email.txt',
            ]
    },
    license = multimail.__license__,
    long_description = open('README.rst').read(),
    zip_safe = False,
)
