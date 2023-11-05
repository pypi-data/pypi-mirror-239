from setuptools import setup

# python setup.py sdist
# twine upload dist/*

setup(name='GlitchPrompts',
      version='0.0.1',
      description='Used as a quick way to add color and prompts to automation.',
      keywords='GlitchPrompts prompts color text',
      author='Clutch_Reboot',
      author_email='clutchshadow26@gmail.com',
      license='GNU General Public License v3.0',
      packages=[
            'GlitchPrompts'
      ],
      zip_safe=False,
      long_description=open('README.md', 'rt').read(),
      long_description_content_type='text/markdown',
      python_requires='>=3.10',
      project_urls={
            "Documentation": "https://clutchreboot.github.io/GlitchPrompts/",
            "Source": "https://github.com/ClutchReboot/GlitchPrompts",
      },
      )