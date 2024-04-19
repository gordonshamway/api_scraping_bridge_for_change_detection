# How to install
1. pip install -r requirements.txt
2. playwright install

# What to configure before the start
1. composer credentials in config.cfg

# How to start the program
python api.py

# How to call for the endpoints (in browser):
-> for composer: visit http://127.0.0.1:8000/composer/?symphony_id=v9joaHizwHRlN4twG0S8 (or whatever symphony_id you have)
-> for portfolio_visualizer: visit http://127.0.0.1:8000/pv/?link=https:\\xyz.com?name=something (or whatever link you have)

# Docker
1. Build the image:
```bash
docker build -t api_scraping_bridge_for_change_detection .
```

2. Start the container with the following command:
```bash
docker run -d \
  --name=api_scraping_bridge_for_change_detection \
  --net=bridge \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  --privileged=false \
  -e COMPOSER_EMAIL=myemail@gmail.com \
  -e COMPOSER_PASSWORD=mypassword \
  -e COMPOSER_TIMEOUT_SECONDS=10 \
  -e PV_EMAIL=myemail@gmail.com \
  -e PV_PASSWORD=mypassword \
  -e PV_TIMEOUT_SECONDS=10 \
  -p 8118:8000/tcp \
  gordonshamway/api_scraping_bridge_for_change_detection
```	