from os.path import join, dirname
from distutils.core import setup


LONG_DESCRIPTION = """
KSP Login is an app for easy authentication management with support for
social as well as traditional authentication.
"""


def long_description():
    """Return long description from README.rst if it's present
    because it doesn't get installed."""
    try:
        return open(join(dirname(__file__), 'README.rst')).read()
    except IOError:
        return LONG_DESCRIPTION


install_requires = [
    'Django>=1.4',
    'python-social-auth',
]


try:
    import importlib
except ImportError:
    install_requires.append('importlib')


setup(
    name='ksp-login',
    version='0.3.0',
    author='Michal Petrucha',
    author_email='michal.petrucha@ksp.sk',
    url='https://github.com/koniiiik/ksp_login',
    packages=['ksp_login', 'ksp_login.templatetags'],
    package_data={
        'ksp_login': [
            'templates/ksp_login/*.html',
            'templates/ksp_login/parts/*.html',
            'static/ksp_login/img/*.svg',
            'static/ksp_login/img/*.png',
            'static/ksp_login/img/*.txt',
            'static/ksp_login/css/*.css',
            'static/ksp_login/js/*.js',
        ],
    },
    license='LICENSE',
    description='A Django app for both traditional and social authentication',
    long_description=long_description(),
    install_requires=install_requires,
)
