'''
Copyright 2012-2014 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import datetime
from qualitylib import domain, utils
from qualitylib.metric_source import url_opener


class HolidayPlanner(domain.MetricSource, url_opener.UrlOpener):
    # pylint: disable=too-few-public-methods,abstract-class-not-used
    ''' Class representing the ICTU holiday planner. '''

    metric_source_name = 'ICTU Vakantie Planner'

    def __init__(self, *args, **kwargs):
        self.__api_url = kwargs.pop('api_url')
        super(HolidayPlanner, self).__init__(*args, **kwargs)

    def days(self, team):
        ''' Return the number of consecutive days that multiple team members
            are absent. '''
        absence_days = self.__absence_days(team)
        longest_stretch = current_stretch = 0
        current_start = longest_start = longest_end = None
        today = datetime.date.today()
        for day_offset in range(366):
            day = today + datetime.timedelta(days=day_offset)
            if day.weekday() >= 5:
                continue  # Weekend
            if absence_days.get(day.isoformat(), 0) > 1:
                if not current_start:
                    current_start = day
                current_stretch += 1
            else:
                if current_stretch > longest_stretch:
                    longest_stretch = current_stretch
                    longest_start = current_start
                    longest_end = day
                current_stretch = 0
                current_start = None
        return longest_stretch, longest_start, longest_end

    def __absence_days(self, team):
        ''' Return the days one or more team members are absent. '''
        member_ids = [member.metric_source_id(self) \
                      for member in team.members()]
        json = utils.eval_json(self.url_open(self.__api_url).read())
        absence_list = json['afwezig']
        # Filter out people not in the team and absences other than whole days
        absence_list = [absence for absence in absence_list \
                        if absence[1] in member_ids and absence[3] == '3']
        days = {}
        for absence in absence_list:
            date = absence[2]
            days[date] = days.get(date, 0) + 1
        return days
