from setuptools import setup

def readme():
	with open('README.md') as f:
		return f.read()

setup(name='autowp', 
	version='1.0.0',
	description='CLI application to remotely manage your WordPress site',
	long_description=readme(),
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python :: 3 :: Only',
		'Topic :: Utilities'
	],
	keywords='wordpress automate installation',
	url='https://github.com/autowp/autowp',
	author='Hiraq',
	author_email='hiraq.dev@gmail.com',
	license='MIT',
	packages=['autowp'],
	install_requires=[
		'fabric',
		'fire',
		'pymongo'
	],
	include_package_data=True,
	test_suite='nose.collector',
	tests_require=['nose'],
	zip_safe=False)
