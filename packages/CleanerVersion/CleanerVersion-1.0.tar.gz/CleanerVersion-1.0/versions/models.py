# Copyright 2014 Swisscom, Sophia Engineering
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import datetime
from django import VERSION
from django.core.exceptions import SuspiciousOperation, MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models.constants import LOOKUP_SEP

from django.db.models import Q
from django.db.models.fields import FieldDoesNotExist
from django.db.models.fields.related import ForeignKey, ReverseSingleRelatedObjectDescriptor, \
    ReverseManyRelatedObjectsDescriptor, ManyToManyField, ManyRelatedObjectsDescriptor, create_many_related_manager, \
    ForeignRelatedObjectsDescriptor
from django.db.models.query import QuerySet, ValuesListQuerySet
from django.db.models.signals import post_init
from django.utils.functional import cached_property
from django.utils.timezone import utc
import six
import uuid

from django.db import models, router


def get_utc_now():
    return datetime.datetime.utcnow().replace(tzinfo=utc)


class VersionManager(models.Manager):
    """
    This is the Manager-class for any class that inherits from Versionable
    """
    use_for_related_fields = True

    def get_queryset(self):
        return VersionedQuerySet(self.model, using=self._db)

    def as_of(self, time=None):
        """
        Filters Versionables at a given time
        :param time: The timestamp (including timezone info) at which Versionables shall be retrieved
        :return: A QuerySet containing the base for a timestamped query.
        """
        return self.get_queryset().as_of(time)

    def next_version(self, object):
        """
        Return the next version of the given object. In case there is no next object existing, meaning the given
        object is the current version, the function returns this version.
        """
        if object.version_end_date == None:
            return object
        else:
            try:
                next = self.get(
                    Q(identity=object.identity),
                    Q(version_start_date=object.version_end_date))
            except MultipleObjectsReturned as e:
                raise MultipleObjectsReturned(
                    "next_version couldn't uniquely identify the next version of object " + str(
                        object.identity) + " to be returned\n" + str(e))
            except ObjectDoesNotExist as e:
                raise ObjectDoesNotExist(
                    "next_version couldn't find a next version of object " + str(object.identity) + "\n" + str(e))
            return next

    def previous_version(self, object):
        """
        Return the previous version of the given object. In case there is no previous object existing, meaning the
        given object is the first version of the object, then the function returns this version.
        """
        if object.version_birth_date == object.version_start_date:
            return object
        else:
            try:
                previous = self.get(
                    Q(identity=object.identity),
                    Q(version_end_date=object.version_start_date))
            except MultipleObjectsReturned as e:
                raise MultipleObjectsReturned(
                    "pervious_version couldn't uniquely identify the previous version of object " + str(
                        object.identity) + " to be returned\n" + str(e))
            # This should never-ever happen, since going prior a first version of an object should be avoided by the
            # first test of this method
            except ObjectDoesNotExist as e:
                raise ObjectDoesNotExist(
                    "pervious_version couldn't find a previous version of object " + str(object.identity) + "\n" + str(
                        e))
            return previous

    def current_version(self, object):
        """
        Return the current version of the given object. The current version is the one having its version_end_date set
        to NULL. If there is not such a version then it means the object has been 'deleted' and so there is no
        current version available. In this case the function returns None.
        """
        if object.version_end_date == None:
            return object

        return self.current.filter(identity=object.identity).first()

    @property
    def current(self):
        return self.filter(version_end_date__isnull=True)

    def create(self, **kwargs):
        """
        Creates an instance of a Versionable
        :param kwargs: arguments used to initialize the class instance
        :return: a Versionable instance of the class
        """
        return self._create_at(None, **kwargs)

    def _create_at(self, timestamp=None, **kwargs):
        """
        WARNING: Only for internal use and testing.

        Create a Versionable having a version_start_date and version_birth_date set to some pre-defined timestamp
        :param timestamp: point in time at which the instance has to be created
        :param kwargs: arguments needed for initializing the instance
        :return: an instance of the class
        """
        ident = unicode(uuid.uuid4())
        if timestamp is None:
            timestamp = get_utc_now()
        kwargs['id'] = ident
        kwargs['identity'] = ident
        kwargs['version_start_date'] = timestamp
        kwargs['version_birth_date'] = timestamp
        return super(VersionManager, self).create(**kwargs)


class VersionedQuerySet(QuerySet):
    """
    The VersionedQuerySet makes sure that every objects retrieved from it has
    the added property 'query_time' added to it.
    For that matter it override the __getitem__, _fetch_all and _clone methods
    for its parent class (QuerySet).
    """

    query_time = None

    def __init__(self, model=None, query=None, using=None, hints=None):
        if VERSION >= (1, 7): # Ensure the correct constructor for Django >= v1.7
            super(VersionedQuerySet, self).__init__(model, query, using, hints)
        else: # For Django 1.6, take the former constructor
            super(VersionedQuerySet, self).__init__(model, query, using)

        self.related_table_in_filter = set()
        """We will store in it all the tables we have being using in while filtering."""

    def __getitem__(self, k):
        """
        Overrides the QuerySet.__getitem__ magic method for retrieving a list-item out of a query set.
        :param k: Retrieve the k-th element or a range of elements
        :return: Either one element or a list of elements
        """
        item = super(VersionedQuerySet, self).__getitem__(k)
        if isinstance(item, (list,)):
            for i in item:
                self._set_query_time(i)
        else:
            self._set_query_time(item)
        return item

    def _fetch_all(self):
        """
        Completely overrides the QuerySet._fetch_all method by adding the timestamp to all objects
        :return: See django.db.models.query.QuerySet._fetch_all for return values
        """
        if self._result_cache is None:
            self._result_cache = list(self.iterator())
            if not isinstance(self, ValuesListQuerySet):
                for x in self._result_cache:
                    self._set_query_time(x)
        if self._prefetch_related_lookups and not self._prefetch_done:
            self._prefetch_related_objects()

    def _clone(self, *args, **kwargs):
        """
        Overrides the QuerySet._clone method by adding the cloning of the VersionedQuerySet's query_time parameter
        :param kwargs: Same as the original QuerySet._clone params
        :return: Just as QuerySet._clone, this method returns a clone of the original object
        """
        clone = super(VersionedQuerySet, self)._clone(**kwargs)
        clone.query_time = self.query_time
        clone.related_table_in_filter = self.related_table_in_filter

        return clone

    def _set_query_time(self, item, type_check=True):
        """
        Sets the time for which the query was made on the resulting item
        :param item: an item of type Versionable
        :param type_check: Check the item to be a Versionable
        :return: Returns the item itself with the time set
        """
        if self.query_time is None:
            self.query_time = get_utc_now()
        if isinstance(item, Versionable):
            item.as_of = self.query_time
        elif isinstance(item, VersionedQuerySet):
            item.query_time = self.query_time
        else:
            if type_check:
                raise TypeError("This item is not a Versionable, it's a " + str(type(item)))
        return item

    def as_of(self, qtime=None):
        """
        Sets the time for which we want to retrieve an object.
        :param qtime: The date and time; set to now if left empty
        :return: A VersionedQuerySet
        """
        time = self.set_as_of(qtime)
        return self.filter(Q(version_end_date__gt=time) | Q(version_end_date__isnull=True),
                           version_start_date__lte=time)

    def set_as_of(self, time=None):
        """
        Sets the query_time for this queryset, which is used to restrict the
        selected records to only those that are valid as of this time.
        :param time: query time to use, defaults to get_utc_now()
        :return: datetime
        """
        self.query_time = time or get_utc_now()
        return self.query_time

    def get_query_time(self):
        """
        Gets the query time for this queryset.  If none was set previously,
        it will be set to the default value.
        :return: datetime
        """
        if self.query_time is None:
            return self.set_as_of()
        return self.query_time

    def propagate_querytime(self, relation_table=None):
        """
        Propagate the query_time information found on the VersionedQuerySet
        object to the given table or on table on which we have filtered on.

        When relation_table is given it will be used and a clause will be
        added to the generated query so that the matching object found on the
        given relation_table will be restricted to the query_time specified
        on the QuerySet. This usage is only use in the VersionManyRelatedManager.

        When relation_table is not given then the function will use the list
        of table we have build while using the filter(). Every time we
        use filter() to filter on the other side of a relation we gather the tables
        on which we have filtered (see _filter_or_exclude()). This list is then
        used by propagate_querytime() to add to the QuerySet where clauses
        restricting the matching records to the one that were active at the
        query_time specified on the QuerySet.

        :param relation_table: name of table to apply the limit on.
        """
        if relation_table:
            relation_tables = [relation_table]
        else:
            relation_tables = self.related_table_in_filter

        query_time = self.get_query_time()
        where_clauses = []
        params = []
        for relation_table in relation_tables:
            where_clauses.append(
                "{0}.version_end_date > %s OR {1}.version_end_date is NULL".format(relation_table, relation_table))
            where_clauses.append("{0}.version_start_date <= %s".format(relation_table))
            params.append(query_time)
            params.append(query_time)

        return self.extra(where=where_clauses, params=params)

    def _filter_or_exclude(self, negate, *args, **kwargs):
        queryset = super(VersionedQuerySet, self)._filter_or_exclude(negate, *args, **kwargs)
        model_class = self.model

        def path_stack_to_tables(model_class, paths_stack, tables=None):
            """
            Recursive function that will navigate the tables found in 'paths_stack'
            and build up a list of all the tables we have visited.

            The found tables are gathered in the collector variable 'tables' which
            is initially empty on the first call.

            On each recursive call we pop from 'paths_stack' until there is no more
            tables to navigate.

            The 'paths_stack' is created by exploding a filter expression on the
            lookup separator, dropping the last item of the expression and then
            reversing the obtained list.

            Example:
                filter expression: student__professor__name__startswith
                after exploding: ['student', 'professor', 'name']
                paths_stack: ['name', 'professor', 'student']
            """
            if not tables:
                tables = []

            attribute = paths_stack.pop()
            try:
                field_object, model, direct, m2m = model_class._meta.get_field_by_name(attribute)

                # This is the counter part of one-to-many field
                if not direct:
                    table_name = field_object.model._meta.db_table
                    queryset.related_table_in_filter.add(table_name)

                if m2m:
                    if isinstance(field_object, VersionedManyToManyField):
                        table_name = field_object.m2m_db_table()
                    else:
                        table_name = field_object.field.m2m_db_table()

                    tables.append(table_name)

            except FieldDoesNotExist:
                # Of course in some occasion the filed might not be found,
                # that's accepted
                pass

            if not paths_stack:
                return tables
            else:
                if isinstance(field_object, VersionedManyToManyField):
                    model_class = field_object.rel.to
                else:
                    model_class = field_object.model
                return path_stack_to_tables(model_class, paths_stack, tables)

        for filter_expression in kwargs:
            paths_stack = list(reversed(filter_expression.split(LOOKUP_SEP)[:-1]))
            if paths_stack:
                tables = path_stack_to_tables(model_class, paths_stack)
                queryset.related_table_in_filter = queryset.related_table_in_filter.union(tables)

        # #TODO: take the necessary steps for reverse relationships
        #                 relation_set = set(attr_obj.field.rel.through.objects.as_of(self.query_time).values_list('pk'))
        #                 queryset = super(VersionedQuerySet, queryset)._filter_or_exclude(False, **{attr_obj.field._m2m_reverse_name_cache + '__in': list(relation_set)})
        #                 instance = attr_obj.field.rel.to
        return queryset


class VersionedForeignKey(ForeignKey):
    """
    We need to replace the standard ForeignKey declaration in order to be able to introduce
    the VersionedReverseSingleRelatedObjectDescriptor, which allows to go back in time...
    """

    def contribute_to_class(self, cls, name, virtual_only=False):
        super(VersionedForeignKey, self).contribute_to_class(cls, name, virtual_only)
        setattr(cls, self.name, VersionedReverseSingleRelatedObjectDescriptor(self))

    def contribute_to_related_class(self, cls, related):
        """
        Override ForeignKey's methods, and replace the descriptor, if set by the parent's methods
        """
        # Internal FK's - i.e., those with a related name ending with '+' -
        # and swapped models don't get a related descriptor.
        super(VersionedForeignKey, self).contribute_to_related_class(cls, related)
        accessor_name = related.get_accessor_name()
        if hasattr(cls, accessor_name):
            setattr(cls, accessor_name, VersionedForeignRelatedObjectsDescriptor(related))


class VersionedManyToManyField(ManyToManyField):
    def __init__(self, *args, **kwargs):
        super(VersionedManyToManyField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        """
        Called at class type creation. So, this method is called, when metaclasses get created
        """
        # self.rel.through needs to be set prior to calling super, since super(...).contribute_to_class refers to it.
        # Classes pointed to by a string do not need to be resolved here, since Django does that at a later point in
        # time - which is nice... ;)
        #
        # Superclasses take care of:
        # - creating the through class if unset
        # - resolving the through class if it's a string
        # - resolving string references within the through class
        if not self.rel.through and not cls._meta.abstract and not cls._meta.swapped:
            self.rel.through = VersionedManyToManyField.create_versioned_many_to_many_intermediary_model(self, cls,
                                                                                                         name)
        super(VersionedManyToManyField, self).contribute_to_class(cls, name)

        # Overwrite the descriptor
        if hasattr(cls, self.name):
            setattr(cls, self.name, VersionedReverseManyRelatedObjectsDescriptor(self))

    def contribute_to_related_class(self, cls, related):
        """
        Called at class type creation. So, this method is called, when metaclasses get created
        """
        super(VersionedManyToManyField, self).contribute_to_related_class(cls, related)
        accessor_name = related.get_accessor_name()
        if hasattr(cls, accessor_name):
            descriptor = VersionedManyRelatedObjectsDescriptor(related, accessor_name)
            setattr(cls, accessor_name, descriptor)
            if hasattr(cls._meta, 'many_to_many_related') and isinstance(cls._meta.many_to_many_related, list):
                cls._meta.many_to_many_related.append(descriptor)
            else:
                cls._meta.many_to_many_related = [descriptor]

    @staticmethod
    def create_versioned_many_to_many_intermediary_model(field, cls, field_name):
        # Let's not care too much on what flags could potentially be set on that intermediary class (e.g. managed, etc)
        # Let's play the game, as if the programmer had specified a class within his models... Here's how.
        # TODO: Test references to 'self'

        from_ = cls._meta.model_name
        to = field.rel.to

        # Force 'to' to be a string (and leave the hard work to Django)
        if not isinstance(field.rel.to, six.string_types):
            to = field.rel.to._meta.object_name
        name = '%s_%s' % (from_, field_name)

        meta = type('Meta', (object,), {
            # 'unique_together': (from_, to),
            'auto_created': cls,
        })
        return type(str(name), (Versionable,), {
            'Meta': meta,
            '__module__': cls.__module__,
            from_: VersionedForeignKey(cls, related_name='%s+' % name),
            to: VersionedForeignKey(to, related_name='%s+' % name),
        })


class VersionedReverseSingleRelatedObjectDescriptor(ReverseSingleRelatedObjectDescriptor):
    """
    A ReverseSingleRelatedObjectDescriptor-typed object gets inserted, when a ForeignKey
    is defined in a Django model. This is one part of the analogue for versioned items.

    Unfortunately, we need to run two queries. The first query satisfies the foreign key
    constraint. After extracting the identity information and combining it with the datetime-
    stamp, we are able to fetch the historic element.
    """

    def __get__(self, instance, instance_type=None):
        """
        The getter method returns the object, which points instance, e.g. choice.poll returns
        a Poll instance, whereas the Poll class defines the ForeignKey.
        :param instance: The object on which the property was accessed
        :param instance_type: The type of the instance object
        :return: Returns a Versionable
        """
        current_elt = super(VersionedReverseSingleRelatedObjectDescriptor, self).__get__(instance, instance_type)
        if not isinstance(current_elt, Versionable):
            raise TypeError("It seems like " + str(type(self)) + " is not a Versionable")
        return current_elt.__class__.objects.as_of(instance.as_of).get(identity=current_elt.identity)


class VersionedForeignRelatedObjectsDescriptor(ForeignRelatedObjectsDescriptor):
    """
    This descriptor generates the manager class that is used on the related object of a ForeignKey relation
    """

    @cached_property
    def related_manager_cls(self):
        # return create_versioned_related_manager
        manager_cls = super(VersionedForeignRelatedObjectsDescriptor, self).related_manager_cls
        rel_field = self.related.field

        class VersionedRelatedManager(manager_cls):
            def __init__(self, instance):
                super(VersionedRelatedManager, self).__init__(instance)

                # This is a hack, in order to get the versioned related objects
                for key in self.core_filters.keys():
                    if '__exact' in key:
                        self.core_filters[key] = instance.identity

            def get_queryset(self):
                queryset = super(VersionedRelatedManager, self).get_queryset()
                if self.instance.as_of is not None:
                    queryset = queryset.as_of(self.instance.as_of)
                return queryset

            def add(self, *objs):
                cloned_objs = ()
                for obj in objs:
                    if not isinstance(obj, Versionable):
                        raise TypeError("Trying to add a non-Versionable to a VersionedForeignKey relationship")
                    cloned_objs += (obj.clone(),)
                super(VersionedRelatedManager, self).add(*cloned_objs)

            if 'remove' in dir(manager_cls):
                def remove(self, *objs):
                    val = rel_field.get_foreign_related_value(self.instance)
                    cloned_objs = ()
                    for obj in objs:
                        # Is obj actually part of this descriptor set? Otherwise, silently go over it, since Django
                        # handles that case
                        if rel_field.get_local_related_value(obj) == val:
                            # Silently pass over non-versionable items
                            if not isinstance(obj, Versionable):
                                raise TypeError(
                                    "Trying to remove a non-Versionable from a VersionedForeignKey realtionship")
                            cloned_objs += (obj.clone(),)
                    super(VersionedRelatedManager, self).remove(*cloned_objs)

        return VersionedRelatedManager


def create_versioned_many_related_manager(superclass, rel):
    """
    The "casting" which is done in this method is needed, since otherwise, the methods introduced by
    Versionable are not taken into account.
    :param superclass: This is usually a models.Manager
    :param rel: Contains the ManyToMany relation
    :return: A subclass of ManyRelatedManager and Versionable
    """
    many_related_manager_klass = create_many_related_manager(superclass, rel)

    class VersionedManyRelatedManager(many_related_manager_klass):
        def __init__(self, *args, **kwargs):
            super(VersionedManyRelatedManager, self).__init__(*args, **kwargs)
            # Additional core filters are: version_start_date <= t & (version_end_date > t | version_end_date IS NULL)
            # but we cannot work with the Django core filters, since they don't support ORing filters, which
            # is a thing we need to consider the "version_end_date IS NULL" case;
            # So, we define our own set of core filters being applied when versioning
            try:
                version_start_date_field = self.through._meta.get_field('version_start_date')
                version_end_date_field = self.through._meta.get_field('version_end_date')
            except (FieldDoesNotExist) as e:
                print str(e) + "; available fields are " + ", ".join(self.through._meta.get_all_field_names())
                raise e
                # FIXME: this probably does not work when auto-referencing

        def get_queryset(self):
            """
            Add a filter to the queryset, limiting the results to be pointed by relationship that are
            valid for the given timestamp (which is taken at the current instance, or set to now, if not
            available).
            Long story short, apply the temporal validity filter also to the intermediary model.
            """

            queryset = super(VersionedManyRelatedManager, self).get_queryset()
            if self.instance.as_of is not None:
                queryset = queryset.as_of(self.instance.as_of)

            return queryset.propagate_querytime(self.through._meta.db_table)

        def _remove_items(self, source_field_name, target_field_name, *objs):
            """
            Instead of removing items, we simply set the version_end_date of the current item to the
            current timestamp --> t[now].
            Like that, there is no more current entry having that identity - which is equal to
            not existing for timestamps greater than t[now].
            """
            return self._remove_items_at(None, source_field_name, target_field_name, *objs)

        def _remove_items_at(self, timestamp, source_field_name, target_field_name, *objs):
            if objs:
                if timestamp is None:
                    timestamp = get_utc_now()
                old_ids = set()
                for obj in objs:
                    if isinstance(obj, self.model):
                        # The Django 1.7-way is preferred
                        if hasattr(self, 'target_field'):
                            fk_val = self.target_field.get_foreign_related_value(obj)[0]
                        # But the Django 1.6.x -way is supported for backward compatibility
                        elif hasattr(self, '_get_fk_val'):
                            fk_val = self._get_fk_val(obj, target_field_name)
                        else:
                            raise TypeError("We couldn't find the value of the foreign key, this might be due to the "
                                            "use of an unsupported version of Django")
                        old_ids.add(fk_val)
                    else:
                        old_ids.add(obj)
                db = router.db_for_write(self.through, instance=self.instance)
                qs = self.through._default_manager.using(db).filter(**{
                    source_field_name: self.instance.id,
                    '%s__in' % target_field_name: old_ids
                }).as_of(timestamp)
                for relation in qs:
                    relation._delete_at(timestamp)

        # FIXME: There could potentially be a problem when trying to remove and re-add an item from/to a relationship; see django/db/models/fields/related.py:654-658

        if 'add' in dir(many_related_manager_klass):
            def add_at(self, timestamp, *objs):
                """
                This function adds an object at a certain point in time (timestamp)
                """
                # First off, define the new constructor
                def _through_init(self, *args, **kwargs):
                    super(self.__class__, self).__init__(*args, **kwargs)
                    self.version_birth_date = timestamp
                    self.version_start_date = timestamp

                # Through-classes have an empty constructor, so it can easily be overwritten when needed;
                # This is not the default case, so the overwrite only takes place when we "modify the past"
                self.through.__init_backup__ = self.through.__init__
                self.through.__init__ = _through_init

                # Do the add operation
                self.add(*objs)

                # Remove the constructor again (by replacing it with the original empty constructor)
                self.through.__init__ = self.through.__init_backup__
                del self.through.__init_backup__

            add_at.alters_data = True

        if 'remove' in dir(many_related_manager_klass):
            def remove_at(self, timestamp, *objs):
                """
                Performs the act of removing specified relationships at a specified time (timestamp);
                So, not the objects at a given time are removed, but their relationship!
                """
                self._remove_items_at(timestamp, self.source_field_name, self.target_field_name, *objs)

                # For consistency, also handle the symmetrical case
                if self.symmetrical:
                    self._remove_items_at(timestamp, self.target_field_name, self.source_field_name, *objs)

            remove_at.alters_data = True

    return VersionedManyRelatedManager


class VersionedReverseManyRelatedObjectsDescriptor(ReverseManyRelatedObjectsDescriptor):
    """
    Beside having a very long name, this class is useful when it comes to versioning the
    ReverseManyRelatedObjectsDescriptor (huhu!!). The main part is the exposure of the
    'related_manager_cls' property
    """

    def __get__(self, instance, owner):
        """
        Reads the property as which this object is figuring; mainly used for debugging purposes
        :param instance: The instance on which the getter was called
        :param owner: no idea... alternatively called 'instance_type by the superclasses
        :return: A VersionedManyRelatedManager object
        """
        return super(VersionedReverseManyRelatedObjectsDescriptor, self).__get__(instance, owner)

    @cached_property
    def related_manager_cls(self):
        return create_versioned_many_related_manager(
            self.field.rel.to._default_manager.__class__,
            self.field.rel
        )


class VersionedManyRelatedObjectsDescriptor(ManyRelatedObjectsDescriptor):
    """
    Beside having a very long name, this class is useful when it comes to versioning the
    ManyRelatedObjectsDescriptor (huhu!!). The main part is the exposure of the
    'related_manager_cls' property
    """

    via_field_name = None

    def __init__(self, related, via_field_name):
        super(VersionedManyRelatedObjectsDescriptor, self).__init__(related)
        self.via_field_name = via_field_name

    def __get__(self, instance, owner):
        """
        Reads the property as which this object is figuring; mainly used for debugging purposes
        :param instance: The instance on which the getter was called
        :param owner: no idea... alternatively called 'instance_type by the superclasses
        :return: A VersionedManyRelatedManager object
        """
        return super(VersionedManyRelatedObjectsDescriptor, self).__get__(instance, owner)

    @cached_property
    def related_manager_cls(self):
        return create_versioned_many_related_manager(
            self.related.model._default_manager.__class__,
            self.related.field.rel
        )


class Versionable(models.Model):
    """
    This is pretty much the central point for versioning objects.
    """

    #: id stands for ID and is the primary key; sometimes also referenced as the surrogate key
    id = models.CharField(max_length=36, primary_key=True)

    #: identity is used as the identifier of an object, ignoring its versions; sometimes also referenced as the natural key
    identity = models.CharField(max_length=36)

    #: version_start_date points the moment in time, when a version was created (ie. an versionable was cloned). This means,
    #: it points the start of a clone's validity period
    version_start_date = models.DateTimeField()

    #: version_end_date, if set, points the moment in time, when the entry was duplicated (ie. the entry was cloned). It
    #: points therefore the end of a clone's validity period
    version_end_date = models.DateTimeField(null=True, default=None, blank=True)

    #: version_birth_date contains the timestamp pointing to when the versionable has been created (independent of any
    #: version); This timestamp is bound to an identity
    version_birth_date = models.DateTimeField()

    #: Make the versionable compliant with Django
    objects = VersionManager()

    #: Hold the timestamp at which the object's data was looked up. Its value must always be in between the
    #: version_start_date and the version_end_date
    as_of = None

    class Meta:
        abstract = True
        unique_together = ('id', 'identity')

    def delete(self, using=None):
        self._delete_at(get_utc_now(), using)

    def _delete_at(self, timestamp, using=None):
        """
        WARNING: This method if only for internal use, it should not be used
        from outside.

        It is used only in the case when you want to make sure a group of
        related objects are deleted at the exact same time.

        It is certainly not meant to be used for deleting an object and give it
        a random deletion date of your liking.
        """
        if self.version_end_date is None:
            self.version_end_date = timestamp
            self.save(using=using)
        else:
            raise Exception('Cannot delete anything else but the current version')

    @property
    def is_current(self):
        return self.version_end_date is None

    def _clone_at(self, timestamp):
        """
        WARNING: This method if only for internal use, it should not be used
        from outside.

        This function is mostly intended for testing, to allow us creating
        realistic test cases.
        """
        return self.clone(forced_version_date=timestamp)

    def clone(self, forced_version_date=None):
        """
        Clones a Versionable and returns a fresh copy of the original object.
        Original source: ClonableMixin snippet (http://djangosnippets.org/snippets/1271), with the pk/id change
        suggested in the comments

        :param forced_version_date: a timestamp including tzinfo; this value is usually set only internally!
        :return: returns a fresh clone of the original object (with adjusted relations)
        """
        if not self.pk:
            raise ValueError('Instance must be saved before it can be cloned')

        if self.version_end_date:
            raise ValueError('This is a historical item and can not be cloned.')

        if forced_version_date:
            if not self.version_start_date <= forced_version_date <= get_utc_now():
                raise ValueError('The clone date must be between the version start date and now.')
        else:
            forced_version_date = get_utc_now()

        earlier_version = self

        later_version = copy.copy(earlier_version)
        later_version.version_end_date = None
        later_version.version_start_date = forced_version_date

        # set earlier_version's ID to a new UUID so the clone (later_version) can
        # get the old one -- this allows 'head' to always have the original
        # id allowing us to get at all historic foreign key relationships
        earlier_version.id = unicode(uuid.uuid4())
        earlier_version.version_end_date = forced_version_date
        earlier_version.save()

        later_version.save()

        # re-create ManyToMany relations
        for field in earlier_version._meta.many_to_many:
            earlier_version.clone_relations(later_version, field.attname)

        if hasattr(earlier_version._meta, 'many_to_many_related'):
            for rel in earlier_version._meta.many_to_many_related:
                earlier_version.clone_relations(later_version, rel.via_field_name)

        later_version.save()

        return later_version

    def at(self, timestamp):
        """
        Force the create date of an object to be at a certain time; This method can be invoked only on a
        freshly created Versionable object. It must not have been cloned yet. Raises a SuspitiousOperation
        exception, otherwise.
        :param timestamp: a datetime.datetime instance
        """
        # Ensure, it's not a historic item
        if not self.is_current:
            raise SuspiciousOperation(
                "Cannot relocate this Versionable instance in time, since it is a historical item")
        # Ensure it's not a versioned item (that would lead to some ugly situations...
        if not self.version_birth_date == self.version_start_date:
            raise SuspiciousOperation(
                "Cannot relocate this Versionable instance in time, since it is a versioned instance")
        # Ensure the argument is really a timestamp
        if not isinstance(timestamp, datetime.datetime):
            raise ValueError("This is not a datetime.datetime timestamp")
        self.version_birth_date = self.version_start_date = timestamp
        return self

    def clone_relations(self, clone, manager_field_name):
        # Source: the original object, where relations are currently pointing to
        source = getattr(self, manager_field_name)  # returns a VersionedRelatedManager instance
        # Destination: the clone, where the cloned relations should point to
        destination = getattr(clone, manager_field_name)
        for item in source.all():
            destination.add(item)

        # retrieve all current m2m relations pointing the newly created clone
        m2m_rels = source.through.objects.filter(**{source.source_field.attname: clone.id})  # filter for source_id
        for rel in m2m_rels:
            # Only clone the relationship, if it is the current one; Simply adjust the older ones to point the old entry
            # Otherwise, the number of pointers pointing an entry will grow exponentially
            if rel.is_current:
                rel.clone(forced_version_date=self.version_end_date)
            # On rel, set the source ID to self.id
            setattr(rel, source.source_field_name, self)
            rel.save()


class VersionedManyToManyModel(object):
    """
    This class is used for holding signal handlers required for proper versioning
    """

    @staticmethod
    def post_init_initialize(sender, instance, **kwargs):
        """
        This is the signal handler post-initializing the intermediate many-to-many model.
        :param sender: The model class that just had an instance created.
        :param instance: The actual instance of the model that's just been created.
        :param kwargs: Required by Django definition
        :return: None
        """
        if isinstance(instance, sender) and isinstance(instance, Versionable):
            ident = unicode(uuid.uuid4())
            now = get_utc_now()
            if not hasattr(instance, 'version_start_date') or instance.version_start_date is None:
                instance.version_start_date = now
            if not hasattr(instance, 'version_birth_date') or instance.version_birth_date is None:
                instance.version_birth_date = now
            if not hasattr(instance, 'id') or not bool(instance.id):
                instance.id = ident
            if not hasattr(instance, 'identity') or not bool(instance.identity):
                instance.identity = ident


post_init.connect(VersionedManyToManyModel.post_init_initialize)
