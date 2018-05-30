# -*- coding: utf-8 -*-

# link to the api http://api.population.io/

import requests
import json
from datetime import datetime


class CountryList:
    "Returns a json list with all available countries the population-api takes as valid input"

    url = "http://api.population.io:80/1.0/countries"

    def get(self):
        ans = getrequest(self.url)
        return ans['countries']


class WPrank:
    "Determine world population rank. Returns a json object"

    def __init__(self, dob, sex, country):
        self.dob = dob
        self.sex = sex
        self.country = makehtmlformat(country)
        self.url = "http://api.population.io:80/1.0/wp-rank/{0}/{1}/{2}/".format(
            self.dob, self.sex, self.country)

    def today(self):
        """
        Calculates the world population rank of a person with the given date of birth, sex and country of origin as of today.\n
        The world population rank is defined as the position of someone's birthday among the group of living people of the same sex and country of origin, ordered by date of birth decreasing.
        The last person born is assigned rank #1.\n
        Today's date is always based on the current time in the timezone UTC.
        """
        url = self.url + "today"
        ans = getrequest(url)
        return ans["rank"]

    def on(self, date):
        """
        Calculates the world population rank of a person with the given date of birth, sex and country of origin on a certain date.\n
        The world population rank is defined as the position of someone's birthday among the group of living people of the same sex and country of origin, ordered by date of birth decreasing.
        The last person born is assigned rank #1.
        """
        url = self.url + "on/{0}".format(date)
        ans = getrequest(url)
        return ans["rank"]

    def aged(self, age):
        """
        Calculates the world population rank of a person with the given date of birth, sex and country of origin on a certain date as expressed by the person's age.\n
        The world population rank is defined as the position of someone's birthday among the group of living people of the same sex and country of origin, ordered by date of birth decreasing.
        The last person born is assigned rank #1.
        """
        url = self.url + "aged/{0}".format(age)
        ans = getrequest(url)
        return ans["rank"]

    def ago(self, ago):
        """
        Calculates the world population rank of a person with the given date of birth, sex and country of origin on a certain date as expressed by an offset towards the past from today.\n
        The world population rank is defined as the position of someone's birthday among the group of living people of the same sex and country of origin, ordered by date of birth decreasing.
        The last person born is assigned rank #1.\n
        Today's date is always based on the current time in the timezone UTC.
        """
        url = self.url + "ago/{0}".format(ago)
        ans = getrequest(url)
        return ans["rank"]

    def inn(self, inn):
        """
        Calculates the world population rank of a person with the given date of birth, sex and country of origin on a certain date as expressed by an offset towards the past from today.\n
        The world population rank is defined as the position of someone's birthday among the group of living people of the same sex and country of origin, ordered by date of birth decreasing.
        The last person born is assigned rank #1.\n
        Today's date is always based on the current time in the timezone UTC.
        """
        url = self.url + "in/{0}".format(inn)
        ans = getrequest(url)
        return ans["rank"]

    def rank(self, rank):
        """
        Calculates the day on which a person with the given date of birth, sex and country of origin has reached (or will reach) a certain world population rank.\n
        The world population rank is defined as the position of someone's birthday among the group of living people of the same sex and country of origin, ordered by date of birth decreasing.
        The last person born is assigned rank #1.\n
        Please be carefull with very small and big ranks. You´ll maybe encounter errors.
        """
        url = self.url + "ranked/{0}".format(rank)
        ans = getrequest(url)
        return ans["date_on_rank"]


class LifeExpectancy:
    "Calculate life expectancy"

    def __init__(self, sex, country):
        self.sex = sex
        self.country = makehtmlformat(country)
        self.url = "http://api.population.io:80/1.0/life-expectancy/"

    def remaining(self, date, age):
        "Calculate remaining life expectancy of a person with given sex, country, and age at a given point in time."
        url = self.url + \
            "remaining/{0}/{1}/{2}/{3}".format(self.sex,
                                               self.country, date, age)
        ans = getrequest(url)
        return ans["remaining_life_expectancy"]

    def total(self, dob):
        """
        Calculate total life expectancy of a person with given sex, country, and date of birth.\n
        Note that this function is implemented based on the remaining life expectancy by picking a reference date based on an age of 35 years.
        It is therefore of limited accuracy.
        """
        url = self.url + \
            "total/{0}/{1}/{2}/".format(self.sex, self.country, dob)
        ans = getrequest(url)
        return ans["total_life_expectancy"]

    def diabetes(self, age, hasD="yes"):
        """
        Calculate diabetes life expectancy of a person with given sex, country, age and whether has diabetes or not.\n
        Yes is default if not specified exactly (yes/no).
        """
        url = self.url + \
            "diabetes/{0}/{1}/{2}/{3}/".format(self.sex,
                                               self.country, age, hasD)
        ans = getrequest(url)
        return ans["total_life_expectancy"]


class Population:
    "Retrieve population tables"

    def __init__(self, country):
        self.country = makehtmlformat(country)
        self.url = "http://api.population.io:80/1.0/population/"

    def population(self, year, age, modus):
        """
        Retrieve population table for specific age group in the given year.\n
        Modus 1 == return total population.\n
        Modus 2 == return male population.\n
        Modus 3 == return female population.
        """
        url = self.url + "{0}/aged/{1}/".format(year, age)
        ans = getrequest(url)
        i = 0
        for name in ans:
            if name['country'] == self.country:
                ans = ans[i]
                break
            i += 1

        if modus == 1:
            return ans["total"]
        elif modus == 2:
            return ans["males"]
        elif modus == 3:
            return ans["females"]

    def bydate(self, date):
        "Determines total population for a given country on a given date. Valid dates are 2013-01-01 to 2022-12-31."

        url = self.url + "{0}/{1}/".format(self.country, date)
        ans = getrequest(url)
        return ans["total_population"]["population"]

    def today(self):
        "Determines total population for a given country for today"

        url = self.url + "{0}/today-and-tomorrow".format(self.country)
        ans = getrequest(url)
        return ans["total_population"][0]["population"]

    def tomorrow(self):
        "Determines total population for a given country for tomorrow"

        url = self.url + "{0}/today-and-tomorrow".format(self.country)
        ans = getrequest(url)
        return ans["total_population"][1]["population"]


class MortalityDistribution:
    "Retrieve mortality distribution tables"

    def __init__(self, sex, country, age):
        self.age = age
        self.sex = sex
        self.country = makehtmlformat(country)
        self.url = "http://api.population.io:80/1.0/mortality-distribution/"

    def byage(self):
        url = self.url + \
            "{0}/{1}/{2}/today/".format(self.country, self.sex, self.age)
        ans = getrequest(url)
        return ans['mortality_distribution']

    def diabetes(self, hasD="unknown"):
        url = self.url + \
            "diabetes/{0}/{1}/{2}/{3}/".format(hasD,
                                               self.country, self.sex, self.age)
        ans = getrequest(url)
        return ans['mortality_distribution']

# helper function to change spaces to %20 for the url calls


def makehtmlformat(txt):
    txt = txt.replace(" ", "%20")
    return txt

# helper function to manage the requests and checks for validity


def getrequest(url):
    try:
        r = requests.get(url)
        ans = json.loads(r.content.decode('UTF-8'))
    except:
        exit("Some critical errors were encountered in url:\n{0}\nBody:\n{1}".format(
            url, r.content))
    if not 200 == r.status_code:
        return exit(ans["detail"])

    return ans
