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
