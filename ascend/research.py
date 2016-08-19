'''
Created on Aug 19, 2016

@author: Johnson
'''

import sys
import os.path
from ascend.utils import uncommas

class NoSuchResearchProjectException(Exception):
    pass

class NoSuchTechnologyException(NoSuchResearchProjectException):
    pass

class AmbiguousResearchProjectException(Exception):
    pass

class AmbiguousTechnologyException(AmbiguousResearchProjectException):
    pass

class Research(object):
    '''
    classdocs
    '''

    research = {}
    initial_research = []
    completed = []
    working_projects = []
    working_path = []

    def __init__(self, researchFileName):
        '''
        Constructor
        '''
        
        rfile = open(researchFileName, 'r')

        while 1:
            line = rfile.readline().split('#')[0].strip()
            if len(line) == 0:
                break

            parts = [x.strip() for x in line.split('|')]

            if len(parts) > 1:
                if parts[0] == 'INITIAL':
                    self.initial_research = uncommas(parts[1])
                else:
                    parts = [parts[0]] + [uncommas(part) for part in parts[1:]]

                    self.research['Proj ' + parts[0]] = (parts[1], parts[2])
                    self.add_research_link('Lower Proj ' + parts[0].lower(), parts[0])
        
                    for tech in parts[2]:
                        self.research['Tech ' + tech] = parts[0]
                        self.add_research_link('Lower Tech ' + tech.lower(), tech)
        
        for i in [k for (k, v) in self.research.items() if v is None]:
            del self.research[i]
        
        rfile.close()

    def add_research_link(self, name, link):
        while len(name) > 0:
            if not self.research.has_key(name):
                self.research[name] = []
            self.research[name].append(link)
            name = name[0:-1]

    def clear_working_path(self):
        self.working_path = []
        
    def clear_working_projects(self):
        self.working_projects = []

    def path_to(self, proj, completed=None):
        if completed is None:
            completed = self.completed + self.working_path
        path = []
        if proj not in completed:
            for req in self.research['Proj ' + proj][0]:
                path.extend(self.path_to(req, completed + path))
            path.append(proj)
        return path

    def complete(self, proj):
        if not self.is_completed(proj):
            self.completed.append(proj)
        while self.is_in_working_path(proj):
            self.working_path.remove(proj)
        while self.is_in_working_proj(proj):
            self.working_projects.remove(proj)

    def is_completed(self, proj):
        return proj in self.completed
    
    def is_in_working_path(self, proj):
        return proj in self.working_path
    
    def is_in_working_proj(self, proj):
        return proj in self.working_projects

    def find_project(self, proj):
        project = self.research.get('Lower Proj ' + proj.lower(), None)
        if project is None:
            raise NoSuchResearchProjectException(proj)
        if len(project) > 1:
            raise AmbiguousResearchProjectException(proj, sorted(project))
        return project[0]

    def find_technology(self, tech):
        technology = self.research.get('Lower Tech ' + tech.lower(), None)
        if technology is None:
            raise NoSuchTechnologyException(tech)
        if len(technology) > 1:
            raise AmbiguousTechnologyException(tech, sorted(technology))
        return self.research.get('Tech ' + technology[0])

    def get_project_req(self, proj):
        project = self.research.get('Proj ' + proj, None)
        if project is None:
            raise NoSuchResearchProjectException(proj)
        return project[0]

    def get_project_tech(self, proj):
        project = self.research.get('Proj ' + proj, None)
        if project is None:
            raise NoSuchResearchProjectException(proj)
        return project[1]

    def add_project(self, proj):
        if not self.is_in_working_path(proj):
            self.working_projects.append(proj)
            self.working_path.extend(self.path_to(proj))
