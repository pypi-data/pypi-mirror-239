from setuptools import setup

# with open("README.md", "r") as arq:
#     readme = arq.read()

setup(name='polar_codes_py_uerj',
      version='1.0.0',
      license='MIT License',
      author='Luiz Fernando Rangel',
      #   long_description=readme,
      long_description_content_type="text/markdown",
      author_email='lfsvrangel@gmail.com',
      keywords='polar codes',
      description=u'Wrapper para codificação e decodificação utilizando Polar Codes',
      packages=['polar_codes_py_uerj'],
      install_requires=['numpy', 'matplotlib'],)
