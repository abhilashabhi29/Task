
import re
import calendar
import datetime
from dateutil.relativedelta import relativedelta

class UrlCreation():


    def findDay(self,date):
        """ findDay of the week
        :param date: date in "%d %m %Y " format (07 03 2020)
        :return: Str day of the week
        """
        born = datetime.datetime.strptime(date, '%d %m %Y').weekday()
        return (calendar.day_name[born])



    def create_url_pattern(self,current_url,working_days):
        """ create a url pattern based on the day of the week
        :param
            current_url:  demo url of the csv.zip file
            working_days[] : list of working days in the week ex:["Monday","Tuesday",...]
        :return: Str day of the week
        """
        urls = []
        for i in range(-30,0):
            date = datetime.datetime.now() + relativedelta(days=i)
            day = (self.findDay(date.strftime("%d %m %Y")))
            if day in working_days:

                date_formated = date.strftime("%d %b %Y")
                date_split =  date_formated.split()
                rep = {"2020": date_split[2], "FEB": date_split[1].upper(),"cm06":"cm"+date_split[0]}
                rep = dict((re.escape(k), v) for k, v in rep.iteritems())
                pattern = re.compile("|".join(rep.keys()))
                new_url = pattern.sub(lambda m: rep[re.escape(m.group(0))], current_url)
                urls.append(new_url)
        return urls

