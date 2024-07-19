## Service for obtaining exchange rates

### General information about the project

* Every day he receives an XML file with exchange rates from the website of the Central Bank of Russia (CBRF).
* Updates data in Redis.

#### Functional

* Responds to the /exchange command, for example: /exchange USD RUB 10 and displays the value of 10 dollars in rubles.
* Responds to the /rates command, sending the user current exchange rates.

#### Technologies used

`Python`, `Redis`, `Git`, `Docker`, `aiogram`, `aiohttp`

### Deploy

```bash
cd ~
git clone https://github.com/adieulatete/Currency-Exchange-Bot.git
cd ~/currencyexchangebot
```

fill out the .env file

```bash
docker-compose up --build -d
```