
from distutils.core import setup
setup(
  name = 'OU_module',         # How you named your package folder (MyLib)
  packages = ['OU_module'],   # Chose the same as "name"
  version = '1.5.0.b3',      # Start with a small number and increase it with every change you make
  license='GPL-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Models the time evolution of a spin-1/2 system with Hamiltonian subjected to random Ornstein-Uhlenbeck noise, representing an NV center spin system in diamond',   # Give a short description about your library
  author = 'Hendry',                   # Type in your name
  author_email = 'hendryadi01@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/hendry24/OU_module',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/hendry24/OU_module/archive/refs/tags/v1.0.tar.gz',    # I explain this later on
  keywords = ['NV Qubit', 'OU process'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'qutip',
          'matplotlib',
      ],
  python_requires='>=3',
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',   # Again, pick a license
  ],
)