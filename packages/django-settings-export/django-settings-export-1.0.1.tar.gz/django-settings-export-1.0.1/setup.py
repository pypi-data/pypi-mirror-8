from setuptools import setup

try:
    import multiprocessing
except ImportError:
    pass

setup(
    name="django-settings-export",
    version='1.0.1',
    author="Jakub Roztocil",
    author_email="jakub@subtleapps.com",
    description='This Django app allows you to export'
                ' certain settings to your templates.',
    long_description=open('README.rst').read().strip(),
    license='BSD',
    url='https://github.com/jakubroztocil/django-settings-export',
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    py_modules=['django_settings_export'],
    install_requires=['django'],
)
