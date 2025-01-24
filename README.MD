curl -X POST http://127.0.0.1:5000/scrape \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.teepublic.com/t-shirt/41148236-freak-in-the-sheets-green-design"}'



curl -X POST https://flaskwebpulpoulapp.azurewebsites.net/scrape \
-H "Content-Type: application/json" \
-d '{"url": "https://www.teepublic.com/t-shirt/41148236-freak-in-the-sheets-green-design"}'



az group create --name FlaskResourceGroup --location "East US"
az appservice plan create --name FlaskAppPlan --resource-group FlaskResourceGroup --sku B1 --is-linux
az webapp create --resource-group FlaskResourceGroup --plan FlaskAppPlan --name FlaskWebPulpoulApp --runtime "PYTHON:3.9"


az webapp deploy --resource-group FlaskResourceGroup --name FlaskWebPulpoulApp --src-path scraper_api.zip



curl --location 'http://localhost:8080/scrape' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url":"https://www.fravega.com/p/heladera-ciclica-drean-277lts-hdr280f00b-blanco-160879/",
    "proxy":"https://sp11k0ggf4:2jTgk6n2d8qgxLSr+R@dc.smartproxy.com:10000"
}'