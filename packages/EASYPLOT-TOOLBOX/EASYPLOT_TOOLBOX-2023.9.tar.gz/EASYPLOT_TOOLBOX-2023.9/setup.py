from setuptools import setup, find_packages

setup(
    	name = 'EASYPLOT_TOOLBOX',
    	version = '2023.9',
		url = 'https://wmpjrufg.github.io/EASYPLOTPY/',
    	description = 'The Easyplotpy toolboox is an algorithm that aims to facilitate the plotting of charts for use in articles and lectures.',
		keywords = ["Plot", "Learning"],
		license = 'MIT License',
        readme = 'readme.md',
		authors = ['Wanderlei Malaquias Pereira Junior', 'Sergio Francisco da Silva', 'Nilson Jorge Leão Junior', 'Mateus Pereira da Silva'],
		author_email = 'wanderlei_junior@ufcat.edu.br',
    	maintainers = ['Wanderlei Malaquias Pereira Junior', 'Mateus Pereira da Silva'],
    	install_requires = ["matplotlib", "seaborn", "squarify", "joypy"],
		classifiers = [	
            			'Development Status :: 4 - Beta',
            			'Topic :: Education',
                        'Topic :: Multimedia :: Graphics',
                        'License :: OSI Approved :: MIT License',
                  		'Framework :: Matplotlib', 
						'Programming Language :: Python',
                        ],
        packages = find_packages()
    )

# https://pypi.org/classifiers/
# https://www.alura.com.br/artigos/como-publicar-seu-codigo-python-no-pypi