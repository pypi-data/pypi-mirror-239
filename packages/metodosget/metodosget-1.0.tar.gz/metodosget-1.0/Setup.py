from distutils.core import setup

setup(
    # Breve descripción de la librería
    description = 'Ejercicio Final',

    # Nombre del autor

    author = 'Oscar Caraballero Galvez',

    # Email del autor

    author_email='xxx@gmail.com',
    package='ejerciciofinal',
    license='MIT',
    version='1.0',
    install_requires=[
        'pandas'
    ],
    # Palabras claves de la librería
    keywords = ['pokemon'],

    classifiers = [

        'Development Status :: 3 - Alpha',
         # Se define el público de la librería
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ]
)