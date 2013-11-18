LegcoCouncilVotes
=================

This is a basic scraper which uses scrapy.py (and selenium for dynamic content) to find and scrap all XML files for the Legco Council Meeting voting records.

The goal of this script is to explore the ways of working with Legco's newly released voting records in XML, in order to make suggestions about ways in which the data can be better presented and structured. As well, we will be developing ways to massage the data in order to better study patterns in the voting record.

This work is part of the OpenGov Project (http://opengov.jmsc.hku.hk) at the Journalism and Media Studies Centre, The University of Hong Kong.


<h2>Installation</h2>

Because the Lecgo XML links are generated dynamically by javascript, you will need to use Selenium to process the webpage for real. Selenium, essentially starts a webbrowser and processes that. It's an unfortunate additional step. We are hoping to encourage Legco to not produce their webpages this way.


It is advised to run this scraper inside of a virtualenv, which allows you to sandbox your python libraries from the rest of the system, reducing system-wide conflicts.

$ pip install virtualenv
$ virtualenv ve

Start the virtual environment

$ source bin/activate

Install scrapy and selenium

$ pip install Scrapy
$ pip install selenium

Download the standalone Selenium server (http://docs.seleniumhq.org/download/) and start it.

$ java -jar selenium-server-standalone-2.x.x.jar


<h2>Run the Scraper</h2>

cd into this project and run the spider

$ scrapy crawl legcovotes