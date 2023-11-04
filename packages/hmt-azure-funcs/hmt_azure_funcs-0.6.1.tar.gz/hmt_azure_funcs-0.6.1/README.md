
# 
# A Message For You!
If you have done something in Azure which is repeated at least semi-often, do consider adding it as a function to this repo!

Just make sure you're not including any secret keys or sensitive information, as the code goes onto the open internet



# Overview
In-progress repo for functions for working with Azure in HMT. You can copy and paste the code from the repo, or load the functions with pip (pip version not currently working - Adam, October 2023).


# Putting into PyPi

**Skynet note**: twine can be slow or not work at all when you're using a proxy, which SkyNet does. I couldn't get the package to upload to pypi from SkyNet. To carry out the steps below I cloned the repo onto an ML Studio notebook and did the below steps in the ML Studio terminal. 

Process to put package in pypi:
1. Create pypi login, inc 2FA and API key
2. Build package `python3 setup.py sdist bdist_wheel`. Install wheel if you don't have it prior to this `pip3 install wheel`
3. Install twine `pip3 install twine`. Twine is used to connect and upload to pypi from your machine.
4. Upload package using your pipy API key `twine upload -u __token__ -p pypi-Ag_**full_long_key** dist/*`


# Use the package

`pip install hmt-azure-funcs`

See the version: `pip show hmt-azure-funcs`

Load a function in python: `from hmt_azure_funcs import read_buffer`



# Issues

On an m1 macbook: hard a hardware issue I don't understand when importing. Could be a discrepency between the hardware the code was compiled on and the actual. Fernet may have some dependencies which makes this harder. 

On ML Studio notebook: it doesnt work. Probably because the AzureML kernel isnt compatible. 

It seems to work fine in SkyNet! Tested in a virtual environment: I strongly suggest you use it in a virtual environment too.



# Uploading new version to PyPi

Go to code in terminal and delete folders used in build: `rm -rf dist build hmt_azure_funcs.egg-info`

Update version in setup.py. Without this pypi won't accept the upload.

Build and upload with Twine, as per steps 2 and 4 in the section above. 

Then load the new version: `pip install --upgrade hmt-azure-funcs`

To confirm the version: `pip show hmt-azure-funcs`


# Future improvements

Some testing for functions that are added. 



