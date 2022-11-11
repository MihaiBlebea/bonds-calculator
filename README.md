# Bond calculator and Screener

**Using the WiseAlpha platform. You can create an account at wisealpha.com**

## How to install?

- Clone this repository

- Run "make setup" in the root folder

- Run "./install.sh"


## How to use?

You can use this CLI tool by calling the `bonds` and passing the right param flags. 

Ex: `bonds -f=wisealpha_market_221109.csv -o dataframe -c 0.07 -m s`

### Flags to use:

-f=wisealpha_market_221109.csv - *the file that you want to load the bonds from*

-o=dataframe - *the output of the result. The options are: dataframe, ticker, company*

-of=./output.csv - *if you selected dataframe as output in prev flag, you can also pass a file to save the dataframe as csv.*

-b=GB - *the country in which the company who issued the bond is based. Default: GB*

-c=0.07 - *the bond coupon (interest rate per year) must be greater than this value to be returned.*

-m=s - *Max maturity, can be s - short, m - medium, l - long.*