# COVID-19 Coronavirus Disease Spread Time Series Analyses for German Regions and Selected Countries

Scripts for daily 
* fetching of updated data
* converting data to common format
* calculating new entities from data
* plotting charts and uploading them to my report https://entorb.net/COVID-19-coronavirus/
* empowering an [interactive country comparison chart](https://entorb.net/COVID-19-coronavirus/#CountriesCustomChart) for the data
* empowering https://covid19-trends.de

Resulting data in JSON and CSV/TSV format can be browsed [here at GitHub](https://github.com/entorb/COVID-19-Coronavirus-German-Regions/tree/master/data). 

Sources
* [German states data](https://github.com/entorb/COVID-19-Coronavirus-German-Regions/tree/master/data/de-states) is from [Robert Koch Institut](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html) obtaind via [swildermann/COVID-19](https://github.com/swildermann/COVID-19)
* [German districts data](https://github.com/entorb/COVID-19-Coronavirus-German-Regions/tree/master/data/de-districts) is from [ArcGIS Covid19_RKI_Sums](https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/)
* [International data](https://github.com/entorb/COVID-19-Coronavirus-German-Regions/tree/master/data/int) is from Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE)  obtained via [pomber/covid19](https://github.com/pomber/covid19)

List of provided/generated data fields
* Date
* Days_Past
* Cases
* Deaths
* Cases_New
* Deaths_New
* Cases_Last_Week
* Deaths_Last_Week
* Cases_Per_Million
* Deaths_Per_Million
* Cases_New_Per_Million
* Deaths_New_Per_Million
* Cases_Last_Week_Per_Million
* Deaths_Last_Week_Per_Million
* Cases_Doubling_Time
* Deaths_Doubling_Time

Nomenclature of data fields
* New = Difference to previous day
* Last_Week = Difference to 7 days past
* Per_Million = Scaled by 1 Million Population
* Doubling_Time = Derived by fitting data with exp. growth function
