# !/bin/sh
""""eval 'exec python "$0" ${1+"$@"};' " """

import os.path
import sys

from ascend.utils import numbered, commas, wrap
from ascend.research import Research , AmbiguousResearchProjectException,\
    NoSuchResearchProjectException

def main(args):
    research = Research(os.path.join(os.path.dirname(__file__), 'Ascend.Research'))

    print wrap(["Enter research projects that have been completed.", "To query how to get to a research project, enter the project name preceded by '?'.  Use '?+' to append the project to the current working list.  Multiple projects can be entered, separated by commas (,).  To look for a technology instead of a project, use '?<technology>' for the project name.  Example: '?+?Nanotwirler'."])
    
    if len(research.initial_research) > 0:
        print 'Suggested iniital project list:'
        print '  ?' + ', '.join(research.initial_research)
    
    proj = '?'
    
    while len(proj) > 0:
        proj = proj.lower()
        # initial ? means we're querying the completed research, or replacing or adding to the research path
        if proj[0] == '?':
            proj = proj[1:]
            # a ? by itself queries the completed research
            if len(proj) == 0:
                print "You have completed the following research projects:"
                print "    " + commas(sorted(research.completed), '')
            else:
                # ?+ means add to the research path; ? without a + means replace the research path
                if proj[0] == '+':
                    proj = proj[1:]
                else:
                    research.clear_working_path()
                    research.clear_working_projects()
                # get the list of projects
                projects = [proj.strip() for proj in proj.split(',')]
                i = 0
                while i < len(projects):
                    try:
                        if projects[i][0] == '?':
                            proj = research.find_technology(projects[i][1:])
                        else:
                            proj = research.find_project(projects[i])
                        if research.is_completed(proj):
                            print "You have already completed " + proj + "!"
                            del projects[i]
                        else:
                            projects[i] = proj
                            i += 1
                    except AmbiguousResearchProjectException,e:
                        print "Project %s is ambiguous - which did you mean? %s" % (repr(e[0]), commas(e[1], 'or'))
                        del projects[i]
                    except NoSuchResearchProjectException,e:
                        print "There is no such project as %s" % (repr(e[0]),)
                        del projects[i]
                print repr(projects)
                if len(projects) > 0:
                    for proj in projects:
                        research.add_project(proj)
        else:
            projects = [proj.strip() for proj in proj.split(',')]
            while len(projects):
                proj = projects.pop(0)
                if proj == '!':
                    proj = '!1'
                recurse = (proj[0] == '!')
                if (recurse): proj = proj[1:]
                if proj.isdigit():
                    if int(proj) <= len(research.working_path):
                        proj = research.working_path[int(proj) - 1]
                try:
                    proj = research.find_project(proj)
                    if research.is_completed(proj):
                        print "You have already completed " + proj + "!"
                    else:
                        completing = [proj]
                        if recurse:
                            i = 0
                            while (i < len(completing)):
                                if research.is_completed(completing[i]):
                                    del completing[i]
                                else:
                                    completing.extend([p for p in research.get_project_req(completing[i]) if p not in completing and not research.is_completed(p)])
                                    i += 1
                        completing.reverse()
                        for p in completing:
                            print "Completed " + p + "."
                            research.complete(p)
                        research.clear_working_path()
                        for p in research.working_projects:
                            research.add_project(p)
                except NoSuchResearchProjectException,e:
                    print "There is no such project as %s" % (repr(e[0]),)
                except AmbiguousResearchProjectException,e:
                    print "Project %s is ambiguous - which did you mean? %s" % (repr(e[0]), commas(e[1], 'or'))
        if len(research.working_projects) > 0:
            print "Working on:    " + commas(research.working_projects)
            print "Research path: " + commas(numbered(research.working_path))
        proj = ""
        while len(proj) == 0:
            print "> ",
            proj = sys.stdin.readline()
            sys.stdout.write("")
            if proj == '':
                print ""
                break
            proj = proj.strip()
        if proj.lower() == 'quit' or proj.lower() == 'exit':
            proj = ''
    
    print "Bye!"
