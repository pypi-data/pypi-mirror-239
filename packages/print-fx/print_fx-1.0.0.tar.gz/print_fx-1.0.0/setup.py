from setuptools import setup, find_packages

setup(
    name ='print_fx',
    version ='1.0.0',
    description = 'This package enhances textual output with effects, including a three-dot animation and a classic typewriter effect. Ideal for creating dynamic CLI applications.',
    author = "Cagla Yagmur",
    author_email = 'caglayagmuricer@gmail.com',
    license='MIT',
    keywords='CLI, typewriter, three dots, text animation, text, print, printfx',
    packages = find_packages(),
    #install_requires = ['time'],
)