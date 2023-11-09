from setuptools import setup, find_packages

setup(
    # Basic info
    name='schoginitoys',
    version='1.1.6',
    packages=find_packages(),
    # packages=['schoginitoys'],
    
    # Metadata
    author='Sreeprakash Neelakantan',
    author_email='sree@schogini.com',
    description='Schogini Toys DIY Kit Toolkit designed for electronics and coding',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://schogini.com',
    # project_urls={
    #     "Bug Tracker": "https://github.com/yourusername/SchoginiSystems/issues",
    # },

    # License
    license='Proprietary',  # Indicates that this is a proprietary software

    # Package Data
    include_package_data=True,

    # Dependencies
    install_requires=[
        # List your project dependencies here
    ],
    
    # Classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: Other/Proprietary License',  # Indicates a proprietary license
        'Natural Language :: English',
       # 'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: MicroPython',
        'Topic :: Software Development :: Libraries :: Python Modules'
        # ... other classifiers ...

    ],
    
    # ... any additional setup arguments
)
