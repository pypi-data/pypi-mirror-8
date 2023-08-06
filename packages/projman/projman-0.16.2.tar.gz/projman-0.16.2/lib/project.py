# -*- coding: utf-8 -*-
# Copyright (c) 2005-2013 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

"""
"""

from warnings import warn
from pprint import pprint
from mx.DateTime import today

from logilab.common.table import Table
from logilab.common.tree import NodeNotFound

from projman.lib.constants import *
from projman.lib.constants import HOURS_PER_DAY
from projman.lib._exceptions import ProjectValidationError

class Project(object):
    """A project is made of a hierachy of tasks, a dictionary of calendars,
    a dictionary of resources, and can optionally include a list of activities
    and a list of scheduled activities

    :attr root_task: root of task hierarchy
    :attr resources: dictionary of resources
    :attr resources_roles: dictionary of resource roles
    :attr calendars: dictionary of calendars
    :attr milestones: dictionary of milestones
    :attr activities: task information
    :attr schedule: Schedule() instance (planned activities)
    """

    TYPE = 'project'

    def __init__(self):
        self._root_task = None
        self.resources = {}
        self.resources_roles = {}
        self.calendars = {}
        self._is_scheduled = False
        self.activities = Table(default_value=None,
                                col_names=['begin', 'end', 'resource', 'task',
                                           'usage', 'src'])
        # Stores computation results based on data from self.activities
        #  (here, 'cost' represents the global cost for the task)
        self.tasks = Table(default_value=None,
                           col_names=['begin', 'end', 'status', 'cost', 'unit'])
        # Stores computation results based on data from self.activities
        #  (here, 'cost' represents the resource's cost for the task)
        self.costs = Table(default_value=None,
                           col_names=['task', 'resource', 'cost', 'unit'])
        self.milestones = {}
        self.factor = 1
        self.priority = 3
        # traite les contraintes de priorité jusque 3 (ie 1, 2 et 3)
        self.nb_solution = 0

    def get_factor(self):
        """find if we must schedule on day, half  or quarter of day
        and return the appropriate factor
        """
        pass # valeur donnee en option ou egale a 1
#        factor = 1
#        factor_ = 1
#        for leaf in self.root_task.leaves():
#            mod = (leaf.duration % 1 )
#            if mod > 0:
#                if mod >= 0.13:
#                    factor_ = mod
#                if mod > 0.5 and mod -0.5 >= 0.13 and mod<0.83:
#                    if mod >= 0.13:
#                        factor_ = (leaf.duration % 1 ) - 0.5
#            factor = min(factor, factor_)

#        dist=abs(factor-1.)
#        _factor = 1.
#        for f in [1., 0.5, 0.25]:
#             d=abs(factor-f)
#             if d<dist:
#                _factor = f
#                dist = d
#        factor = _factor
#        self.factor = int(1 / factor)

    def get_root_task(self):
        return self._root_task

    def set_root_task(self, value):
        assert self._root_task is None
        self._root_task = value

    root_task = property(get_root_task, set_root_task)

    def check_consistency(self):
        errors = []
        errors += self.root_task.check_consistency()
        return errors

    def check_tasks(self):
        resources = self.resources
        roles = self.resources_roles
        for leaf in self.root_rask.leaves():
            leaf.check_duration()
            leaf.check_role(self)
        for role in roles:
            for res in role.resource_roles:
                if res.id not in self.resources:
                    raise ProjmanError

    # schedule methods ########################################################

    def add_schedule(self, activities):
        """update activities and cache with new schedule-based information"""
        self._is_scheduled = True
        for begin, end, resource, task, usage in activities:
            self.activities.append_row((begin, end, resource, task,
                                        usage, 'plan'))
        self.update_caches()

    def reset_schedule(self):
        self._is_scheduled = False
        self.activities.remove('src', 'plan')
        self.update_caches()

    def compute_task_status(self, task, begin, end):
        if task.progress == 1:
            status = 'done'
        elif task.progress > 0:
            status = 'current'
        else:
            status = 'todo'
        for c_type, date, priority in task.get_date_constraints():
            if c_type == BEGIN_AFTER_DATE and not date <= begin and \
                            priority  <= self.priority:
                print "task %s should begin after %s" % (task.id, begin)
                status = 'problem'
                break
            elif c_type == END_BEFORE_DATE and not end <= date and \
                            priority  <= self.priority:
                print "task %s should end before %s" % (task.id, begin)
                status = 'problem'
                break
        return status

    def update_caches(self):
        """updates self.tasks and self.costs"""
        # FIXME: Table has no empty() method
        self.tasks = Table(default_value=None,
                           col_names=['begin', 'end', 'status', 'cost', 'unit'])
        self.costs = Table(default_value=None,
                           col_names=['task', 'resource', 'cost', 'unit'])
        for task in self.root_task.flatten():
            try:
                begin, end = self.get_task_date_range(task)
                status = self.compute_task_status(task, begin, end)
                cost = self.get_task_total_cost(task, task.duration)
                self.tasks.append_row((begin, end, status, cost, 'XXX'),
                                      row_name=task.id)
            except ValueError, exc:
                #print 'while building cache, ignoring', exc
                pass #print 'x',
            else:
                pass #print '.',

        grouped = self.activities.groupby('task', 'resource')
        for task_id, resources in grouped.iteritems():
            for res_id, rows in resources.iteritems():
                cost = sum([row[4] for row in rows])
                self.costs.append_row((task_id, res_id, cost, 'XXX'))


    # calendar, role, and resource methods ###################################

    # calendars
    def add_calendar(self, cal):
        if cal.id in self.calendars:
            raise ProjectValidationError('Calendar ID "%s" already exists' % cal.id)
        self.calendars[cal.id] = cal

    def get_calendar(self, cal_id):
        return self.calendars[cal_id]

    def has_calendar(self, cal_id):
        """tests if the given <cal_id> is used"""
        return cal_id in self.calendars

    # roles
    def add_role(self, role):
        if role.id in self.resources_roles:
            raise ProjectValidationError('Role ID "%s" already exists' %
                                         role.id)
        #assert role.id not in self.resources_roles
        self.resources_roles[role.id] = role

    def get_role(self, role_id):
        return self.resources_roles[role_id]

    # resources
    def add_resource(self, res):
        if res.id in self.resources:
            raise ProjectValidationError('Resource ID "%s" already exists' % res.id)
        self.resources[res.id] = res

    def has_resource(self, res_id):
        """tests if resource <res_id> is used"""
        return res_id in self.resources

    def get_resources(self):
        """return all the resources available for the project"""
        return self.resources.values()

    def get_resource(self, resource_id):
        return self.resources[resource_id]

    # tasks methods ###########################################################

    def get_task(self, task_id):
        """return the task asociated to id"""
        return self.root_task.get_node_by_id(task_id)

    def get_nb_tasks(self):
        """returns number of task/milestone in project plus one
        (project itself)"""
        return len(self.root_task.flatten())

    def has_task_id(self, task_id):
        """return True if there is a task with given <task_id>"""
        return task_id in [t.id for t in self.root_task.flatten()]

    def update_task_ids(self, task, new_id):
        """set the new_id for a task and update the other tasks"""
        assert not self.has_task_id(new_id)
        old_id, task.id = task.id, new_id
        # update constraints; XXX do we have other task_id dependencies ?
        for c_task, constraint in self.get_constraints(old_id):
            c_task.task_constraints.remove(constraint)
            c_task.task_constraints.add((constraint[0], new_id, constraint[2]))

    def get_constraints(self, constr_id):
        '''return list of tasks and constraints with given <constr_id>'''
        dependencies = []
        for task in self.root_task.flatten():
            for c_type, task_id, priority in task.task_constraints:
                if task_id == constr_id:
                    dependencies.append((task, (c_type, task_id, priority)))
        return dependencies

    def is_in_allocated_time(self, task_id, date):
        """
        tests if day is in allocated time for task t_id
        """
        for begin, end, _, _, _, _ in self.activities.select('task', task_id):
            if begin <= date < end:
                return True
        return False

    def set_task_property(self, task_id, attr, value):
        assert self._is_scheduled, "Project not scheduled"
        self.tasks.set_cell_by_ids(task_id, attr, value)

    def get_task_status(self, task):
        """
        return the status computed during the scheduling
        if task_id is not oredered, return default value todo
        """
        assert self._is_scheduled, "Project not scheduled"
        ordered_status = ['problem', 'todo', 'current', 'done']
        status_list = []
        for leaf in task.leaves():
            if leaf.TYPE == 'Milestone':
                # as leaf.id is int, self.tasks[leaf.id] will mistake it
                _, _, status, _, _ = self.tasks.get_row_by_id(leaf.id)
                status_list.append(status)
            for status in ordered_status:
                if status in status_list:
                    return status
        return 'todo'

    def task_has_info(self, task_id):
        """
        indicates if the task_id has any info stored in the object
        useful for example when writing xml for object
        """
        assert self._is_scheduled, "Project not scheduled"
        return len(self.tasks.get_row_by_id(task_id)) > 0
        return False

    def get_task_date_range(self, task):
        if task.TYPE == "milestone":
            date = self.milestones.get(task.id)
            return date, date

        begins, ends = [], []
        for leaf in task.leaves():
            for begin, end, __resource, __task, __usage, __src \
                    in self.activities.select('task', leaf.id):
                begins.append(begin)
                ends.append(end)
        try:
            begin = min(begins)
        except ValueError:
            raise ValueError('Task %s has no begin' % (task.id,))
        try:
            end = max(ends)
        except ValueError:
            raise ValueError('Task %s has no end' % task.id)
        return begin, end

    # activities methods ######################################################

    def add_activity(self, begin, end, resource_id, task_id,
                     usage=1., src='past'):
        """add an activity"""
        assert src in ['past', 'plan']
        self.activities.append_row([begin, end, resource_id, task_id,
                                    usage, src])

    def add_activities(self, rows):
        """concatenates another activities entity"""
        for row in rows:
            self.add_activity(*row)
        self.update_caches()

    def has_activity(self, t_id):
        return len(self.activities.select('task', t_id)) > 0

    def get_nb_of_activities(self):
        rowsize, colsize = self.activities.get_dimensions()
        return rowsize

    def clear_activities(self):
        self.activities = Table(default_value=None,
                                col_names=['begin', 'end', 'resource', 'task',
                                           'usage', 'src'])

    # usage & costs methods ###################################################

    def get_resources_duration_per_task(self, task_id):
        result = {}
        grouped = self.activities.groupby('task', 'resource')
        try:
            grouped = grouped[task_id]
        except KeyError:
            return {}
        for r_id, rows in grouped.items() :
            duration = 0.0
            for begin, end, resource, task, usage, src in rows:
                duration += self.compute_duration(begin, end, usage)
            result[r_id] = duration
        return result


    def get_usage(self, resource_id, task_id, date):
        """
        get the usage in percentage for the specified task, resource and date
        """
        grouped = self.activities.groupby('resource', 'task')
        # FIXME: remove try/catch?
        try:
            rows = grouped[resource_id][task_id]
        except KeyError:
            return 0.
        total_usage = 0.
        for begin, end, resource, task, usage, src in rows:
            if begin <= date <= end:
                total_usage += usage
        return total_usage

    def get_total_usage(self, resource_id, date):
        """
        get the usage in percentage at date for resource_id
        """
        total_usage = 0.0
        for begin, end, resource, task, usage, src \
                in self.activities.select('resource', resource_id):
            if begin <= date <= end:
                total_usage += usage
        return total_usage

    def get_resource_disponibility(self, resource_id, date):
        """get disponibility of a resource on a given date"""
        return 1 - self.get_total_usage(resource_id, date)

    def get_duration_worked_for_t(self, task_id):
        """gets the duration of work in days (float) of a given task"""
        warn('Project.get_duration_worked_for_t() is to be removed soon',
             DeprecationWarning)
        duration = 0.0
        for begin, end, resource, task, usage, src \
                in self.activities.select('task', task_id):
            duration += self.compute_duration(begin, end, usage)
        return duration


    def get_task_total_cost(self, task ,task_tot_duration):
        """
        obtain concatenation of costs for a task
        """
        costs = self.get_task_costs(task, task_tot_duration)[0]
        return sum(costs.values())

    def get_task_costs(self, task, task_tot_duration):
        """
        run through all activities and sum up duration * usage
        # FIXME - do we really need to send back durations
        from here? (simpler in tasks_costs_writer)
        """
        costs = {}
        durations = {}
        rounded=0
        if task.resources_role is None:
            return {}, {}
        role = self.get_role(task.resources_role)
        cost_rate = role.hourly_cost
        activities = self.activities.select('task', task.id)
        if 0 < task_tot_duration % (1./self.factor) < (1./self.factor):
            rounded = task_tot_duration % (1./self.factor) - 1./self.factor

        for begin, end, resource, task, usage, src in activities:
            costs.setdefault(resource, 0)
            durations.setdefault(resource, 0)
            # FIXME - presuming 8 hour /day work
            # FIXME - leaving behind the currency
            duration = self.compute_duration(begin, end, usage)
            durations[resource] += duration
        # gestion des arrondis
        if len(durations) > 0:
            rounded  = rounded / len(durations)
            for res in durations:
                # using resources old definition
                durations[res] += rounded
                costs[res] += durations[res] * cost_rate * HOURS_PER_DAY
        return costs, durations

    def compute_duration(begin, end, usage):
        delta = end.day - begin.day
        days = 1 + delta
        return days * usage
    compute_duration = staticmethod(compute_duration)

