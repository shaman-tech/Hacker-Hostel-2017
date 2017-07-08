brew install automake autoconf autoconf-archive libtool
brew install pkgconfig
brew install icu4c
brew install leptonica
brew install gcc
brew install tesseract
brew install imagemagick@6

echo "export PKG_CONFIG_PATH='/usr/local/opt/imagemagick@6/lib/pkgconfig:${PKG_CONFIG_PATH}'" >> ~/.bash_profile
echo "export LDFLAGS='-L/usr/local/opt/imagemagick@6/lib'" >> ~/.bash_profile
echo "export CPPFLAGS='-I/usr/local/opt/imagemagick@6/include'" >> ~/.bash_profile
echo "export MAGICK_HOME'=/usr/local/Cellar/imagemagick@6/6.9.8-10'" >> ~/.bash_profile
echo "export PATH'=/usr/local/Cellar/imagemagick@6/6.9.8-10/bin:${PATH}'" >> ~/.bash_profile

sudo pip install --upgrade google-api-python-client
pip install -r requirements.txt
