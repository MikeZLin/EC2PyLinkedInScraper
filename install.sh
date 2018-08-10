sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:canonical-chromium-builds/stage
sudo apt-get update
sudo apt-get install chromium-browser unzip -y
sudo apt-get install python3 python3-pip -y
sudo curl -SL https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip > chromedriver.zip
sudo unzip chromedriver.zip -d /usr/local/bin/
pip3 install selenium 
pip3 install boto3 
pip3 install bs4 
pip3 install beautifulsoup4 
pip3 install botocore 
pip3 install joblib 
pip3 install requests 
pip3 install lxml 
pip3 install dateutils 
pip3 install docutils 
pip3 install chromedriver_installer