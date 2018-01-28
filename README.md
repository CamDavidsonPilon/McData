# McData

A data repository for fast food nutrition and ingredients. 

To scrape historic nutritional information, use the [waybackpack](https://github.com/jsvine/waybackpack) command line tool. To get unique McDonald's nutritional PDFs until 2018, run the following from the command line:

`pip install waybackpack`
`waybackpack http://nutrition.mcdonalds.com/usnutritionexchange/nutritionfacts.pdf -d DESTINATIONDIRECTORY --to-date 2018 --uniques-only`

Note: McDonald's previously stored its nutritional PDFs [here](http://nutrition.mcdonalds.com/getnutrition/nutritionfacts.pdf) 
