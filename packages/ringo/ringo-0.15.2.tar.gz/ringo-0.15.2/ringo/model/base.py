import logging
import json
import re
import uuid
from pyramid.threadlocal import get_current_request
from formbar.config import Config, load
from sqlalchemy import Column, CHAR
from sqlalchemy.orm import joinedload, ColumnProperty, class_mapper
from sqlalchemy.orm.attributes import get_history
from ringo.lib.helpers import get_path_to_form_config, serialize
from ringo.lib.cache import CACHE_TABLE_CONFIG, CACHE_FORM_CONFIG
from ringo.lib.sql import DBSession
from ringo.lib.sql.cache import regions
from ringo.lib.imexport import JSONExporter
from ringo.lib.sql.query import FromCache, set_relation_caching
from ringo.model.mixins import Logged, StateMixin, Owned

log = logging.getLogger(__name__)

def nonecmp(a, b):
  if a is None and b is None:
    return 0
  if a is None:
    return -1
  if b is None:
    return 1
  return cmp(a, b)

def attrgetter(field, expand):
    def g(obj):
        return resolve_attr(obj, field, expand)
    return g


def resolve_attr(obj, attr, expand):
    return obj.get_value(attr, expand=expand)


class BaseItem(object):

    _modul_id = None
    _sql_eager_loads = []
    """Configure a list of relations which are configured to be
    eager loaded."""

    # Added UUID column for every BaseItem. This is needed to identify
    # item on imports and exports.
    uuid = Column('uuid', CHAR(32),
                  default=lambda x: '%.32x' % uuid.uuid4())

    def render(self):
        """This function can be used to render a different
        representation of the item. On default it also returns the
        simple string representation. Usefull to build some HTML used in
        links e.g overviews and lists"""
        return self.__str__()

    def __str__(self):
        return self.__unicode__()

    def __cmp__(self, other):
        """Comparision of the elements are done on their string
        representation"""
        s = unicode(self)
        o = unicode(other)
        if s < o:
            return -1
        elif s == o:
            return 0
        else:
            return 1

    def __getitem__(self, name):
        return self.get_value(name)

    def __getattr__(self, name):
        """This function tries to get the given attribute of the item if
        it can not be found using the usual way to get attributes. In
        this case we will split the attribute name by "." and try to get
        the attribute along the "." separated attribute name. The
        function also offers basic support for accessing individual
        elements in lists in case one attribute is a list while
        iterating over all attributes. Currently only flat lists are
        supported.

        Example: x.y[1].z"""
        element = self
        attributes = name.split('.')
        for attr in attributes:
            splitmark_s = attr.find("[")
            splitmark_e = attr.find("]")
            if splitmark_s > 0:
                index = int(attr[splitmark_s + 1:splitmark_e])
                attr = attr[:splitmark_s]
                element_list = object.__getattribute__(element, attr)
                if len(element_list) > 0:
                    element = element_list[index]
                else:
                    log.error("IndexError in %s on %s for %s"
                              % (name, attr, self))
                    element = None
                    break
            else:
                element = object.__getattribute__(element, attr)
        return element

    def __unicode__(self):
        """Will return the string representation for the item based on a
        configured format string in the modul settings. If no format str
        can be found return the id of the item.

        The format string must have the following syntax:
        format_str|field1,field2,....fieldN. where format_str in a
        string with %s placeholders and fields is a comma separated list
        of fields of the item"""
        modul = self.get_item_modul()
        format_str, fields = modul.get_str_repr()
        if format_str:
            return format_str % tuple([self.get_value(f) for f in fields])
        else:
            return "%s" % str(self.id or self.__class__)

    @classmethod
    def get_columns(cls, include_relations=False):
        return [prop.key for prop in class_mapper(cls).iterate_properties
                if isinstance(prop, ColumnProperty) or include_relations]

    @classmethod
    def get_item_factory(cls):
        return BaseFactory(cls)

    @classmethod
    def get_item_list(cls, request, user=None, cache=None):
        if not request.cache_item_list.get(cls._modul_id):
            listing = BaseList(cls, request, user, cache)
            request.cache_item_list.set(cls._modul_id, listing)
        return request.cache_item_list.get(cls._modul_id)

    @classmethod
    def get_item_actions(cls, request=None):
        """Returns a list of ActionItems which are available for items
        modul. If you want to add custom actions to the modul please
        overwrite this method.

        :returns: List of ActionItems.
        """
        modul = cls.get_item_modul(request)
        return modul.actions

    @classmethod
    def get_item_modul(cls, request=None):
        if not request:
            request = get_current_request()
            #if request:
            #    log.warning("Calling get_item_modul with no request although "
            #                "there is a request available. "
            #                "Using 'get_current_request'...")
        if not request or not request.cache_item_modul.get(cls._modul_id):
            from ringo.model.modul import ModulItem
            factory = BaseFactory(ModulItem)
            modul = factory.load(cls._modul_id)
            if request:
                if not request.cache_item_modul.get(cls._modul_id):
                    request.cache_item_modul.set(cls._modul_id, modul)
            else:
                return modul
        return request.cache_item_modul.get(cls._modul_id)

    @classmethod
    def get_action_routename(cls, action, prefix=None):
        routename = "%s-%s" % (cls.__tablename__, action)
        if prefix:
            return "%s-%s" % (prefix, routename)
        return routename

    @classmethod
    def get_table_config(cls, tablename=None):
        """Returns the table (overview, listing) configuration with the
        name 'tablename' of this Item from the configuration file. If
        the default table configuration will be returned. The table
        configuration is cached for later requests."""
        # As this is a class method of the BaseItem we need to build a
        # unique cachename for tableconfigs among all inherited classes.
        cachename = "%s.%s" % (cls.__name__, tablename)
        from ringo.lib.renderer import TableConfig
        if not CACHE_TABLE_CONFIG.get(cachename):
            CACHE_TABLE_CONFIG.set(cachename, TableConfig(cls, tablename))
        return CACHE_TABLE_CONFIG.get(cachename)

    def get_form_config(self, formname):
        """Return the Configuration for a given form. The configuration
        tried to be loaded from the application first. If this fails it
        tries to load it from the ringo application."""
        cfile = "%s.xml" % self.__class__.__tablename__
        cachename = "%s.%s" % (self.__class__.__name__, formname)
        if not CACHE_FORM_CONFIG.get(cachename):
            try:
                loaded_config = load(get_path_to_form_config(cfile))
            except IOError:
                loaded_config = load(get_path_to_form_config(cfile, 'ringo'))
            config = Config(loaded_config)
            CACHE_FORM_CONFIG.set(cachename, config.get_form(formname))
        return CACHE_FORM_CONFIG.get(cachename)

    def reset_uuid(self):
        self.uuid = '%.32x' % uuid.uuid4()

    def get_changes(self):
        """Will return dictionary which attributes which have been
        changes. The value for each attribute is a tuple with the old
        and new value.

        The function uses sqlalchemy history object which has
        information on changed attributes of the item to check which
        attributes have changed.  See
        http://docs.sqlalchemy.org/en/rel_0_8/orm/session.html \
        ?highlight=get_history#sqlalchemy.orm.attributes.get_history
        for more details.

        :returns: Dictionary whith changes.
        """

        # FIXME: History is empty if the item as relations set.
        # Reproduce: Task item in plorma. Set more than one member in
        # the team. (None) <2013-10-31 23:14>
        changes = {}
        for col in self.get_columns():
            history = get_history(self, col)
            if history.has_changes():
                changes[col] = (history.deleted, history.added)
        return changes

    def get_value(self, name, form_id="read", expand=False):
        """Return the value of the given attribe of the item. Unlike
        accessing the raw value through the attribite directly this
        function will apply all configured transformations to the value
        before returing it."""
        try:
            raw_value = getattr(self, name)
        except:
            # This error is only acceptable for blobforms as attributes
            # can be added and removed by the user on the fly. So there
            # is a good chance that older items do not have this attribute.
            log.error("Attribute '%s' not found in '%s'; id:%s"
                      % (name, repr(self), self.id))
            raw_value = None
        if expand:
            form_config = self.get_form_config(form_id)
            try:
                field_config = form_config.get_field(name)
                for option in field_config.options:
                    if str(raw_value) == str(option[1]):
                        return option[0]
            except KeyError:
                log.error("Field %s not found in form config" % name)
        return raw_value

    def get_values(self, include_relations=False, serialized=False):
        """Will return a dictionary with the values of the item. If
        include_relations is true, than the realtion values are
        included. Else only scalar values are included"""
        values = {}
        for field in self.get_columns(include_relations):
            # Ignore private form fields
            if field.startswith("_"):
                continue
            if serialized:
                value = serialize(getattr(self, field))
            else:
                value = getattr(self, field)
            values[field] = value
        return values

    def set_values(self, values):
        """Will set the values of the items attributes to the given
        values in the dictionary. Attributes beginning with "_" are
        considred private and are ignored.

        This function will not handle saving the changed data. This can
        be by either calling the save method of the item, or
        automatically at the transactions end if autocommit is enabled.

        Please note that setting the values for foreign key attributes
        might not work as expected. This is especially true for foreign
        keys to already existing items. You are not able to change a
        existing relation in the items by changing the foreign key value
        (You must do this by setting the related item). In this case the
        value for the foreign key seems to be ignored and replaced by
        the one of the actual related item.
        In contrast you can set a new relation by setting the foreign
        key if this is a new relation.

        :values: Dictionary with values to be set
        """

        for key, value in values.iteritems():
            # Ignore private form fields
            if key.startswith('_'):
                continue
            if hasattr(self, key):
                log.debug("Setting value '%s' in %s" % (value, key))
                setattr(self, key, value)
            else:
                log.warning('Not saving "%s". Attribute not found' % key)

    def save(self, data, request=None):
        """Will save the given data into the item. If the current item
        has no value for the id attribute it is assumed that this item
        must be added to the database as a new item. In this case you
        need to provide a dbsession as the new item is not linked to any
        dbsession yet.

        Please note, that you must ensure that the submitted values are
        validated. This function does no validation on the submitted
        data.

        :data: Dictionary with key value pairs.
        :request: Current request session. Used when saving new items.
        :returns: item with new data.

        """
        if request:
            dbsession = request.db
        else:
            dbsession = None
        # Use repr here a the __unicode__ method default to self.id
        # which might not be available here
        log.debug("Saving %s" % repr(self))

        old_values = self.get_values()
        # Set values
        self.set_values(data)

        # Handle statechange
        if isinstance(self, StateMixin):
            for key in self.list_statemachines():
                new_state_id = data.get(key)
                old_state_id = old_values.get(key)
                if ((new_state_id and old_state_id)
                   and (new_state_id != old_state_id)):
                    try:
                        self.change_state(request, key, old_state_id, new_state_id)
                    except Exception as error:
                        log.error(error)
                        self.change_state(request, key, old_state_id, old_state_id)

        # Handle logentry
        if isinstance(self, Logged):
            if not self.id:
                subject = "Create"
                text = json.dumps(self.build_changes(old_values, data))
            else:
                subject = "Update"
                text = json.dumps(self.build_changes(old_values, data))
            self.add_log_entry(subject, text, request)

        # If the item has no id, then we assume it is a new item. So
        # add it to the database session.
        if not self.id and dbsession:
            dbsession.add(self)
            # flush the session to make the new id in the element
            # presistent.
            dbsession.flush()

            # Check if uid or gid or uid inheritance is configured.
            if isinstance(self, Owned):
                gid_relation = getattr(self, '_inherit_gid')
                if gid_relation:
                    parent = getattr(self, gid_relation)
                    # FIXME: Check why this attribute can be None. (ti)
                    # <2014-04-01 13:37>
                    if parent:
                        self.group = parent.group
                    else:
                        log.warning("Inheritance of group '%s' failed. "
                                    "Was None" % gid_relation)
                uid_relation = getattr(self, '_inherit_uid')
                if uid_relation:
                    parent = getattr(self, uid_relation)
                    if parent:
                        self.owner = parent.owner
                    else:
                        log.warning("Inheritance of group '%s' failed. "
                                    "Was None" % gid_relation)
        return self


class BaseList(object):
    def __init__(self, clazz, request, user=None, cache="", items=None):
        """A List object of. A list can be filterd, and sorted.

        :clazz: Class of items which will be loaded.
        :request: Current request
        :user: If provided only items readable for the
               given user are included in the list
        :cache: Name of the cache region. If empty then no caching is
                done.
        """
        self.clazz = clazz
        self.request = request
        # TODO: Check which is the best loading strategy here for large
        # collections. Tests with 100k datasets rendering only 100 shows
        # that the usual lazyload method seems to be the fastest which is
        # not what if have been expected.
        #self.items = db.query(clazz).options(joinedload('*')).all()

        if items is None:
            q = request.db.query(self.clazz)
            if cache in regions.keys():
                q = set_relation_caching(q, self.clazz, cache)
                q = q.options(FromCache(cache))
            for relation in self.clazz._sql_eager_loads:
                q = q.options(joinedload(relation))
            self.items = self._filter_for_user(q.all(), user)
        else:
            self.items = items
        self.search_filter = []

    def __iter__(self):
        return iter(self.items)

    def _filter_for_user(self, items, user):
        """Returns a filterd item list. The items are filterd based on
        the permission of the given user. Only items are included where
        the given user has read access. This means:

         1. The user has aproriate role (read access)
         2. Is owner or member of the items group

        If no user is provided the list is not filtered and all origin
        items are included in the returned list.
        """
        # Filter items based on the uid
        from ringo.lib.security import has_permission
        filtered_items = []
        if user and not user.has_role("admin"):
            # Iterate over all items and check if the user has generally
            # access to the item.
            for item in items:
                # Only check ownership if the item provides a uid.
                if has_permission('read', item, self.request):
                    filtered_items.append(item)
            return filtered_items
        else:
            return items

    def sort(self, field, order, expand=False):
        """Will return a sorted item list. Sorting is done based on the
        string version of the value in the sort field.

        :field: Name of the field on which the sort will be done
        :order: If "desc" then the order will be reverted.
        :expand: If True, then the sorting will be done on the expanded values.
        :returns: Sorted item list

        """
        sorted_items = sorted(self.items, cmp=nonecmp, key=attrgetter(field, expand))
        if order == "desc":
            sorted_items.reverse()
        self.items = sorted_items

    def filter(self, filter_stack):
        """This function will filter the list of items by only leaving
        those items in the list which match all search criterias in the
        filter stack. The list will get reduced with every iteration on
        the filter stack.

        For each filter in the stack The search word will be compiled to
        the regular expression. Then all items are iterated.  For each
        item the function will try to match the value of either all, or
        from the configued search field with the regular expression. If
        the value matches, then the item is kept in the list.
        """
        self.search_filter = filter_stack
        log.debug('Length filterstack: %s' % len(filter_stack))
        table_config = self.clazz.get_table_config()
        table_columns = {}

        # Save cols in the tableconfig for later access while getting values.
        for col in table_config.get_columns():
            table_columns[col.get('name')] = col

        for search, search_field, regexpr in filter_stack:
            # Build a regular expression
            if regexpr:
                re_expr = re.compile(search, re.IGNORECASE)
            else:
                re_expr = re.compile(re.escape(search), re.IGNORECASE)
            filtered_items = []
            log.debug('Filtering "%s" in "%s" on %s items'
                      % (search, search_field, len(self.items)))
            if search_field != "":
                fields = [search_field]
            else:
                fields = table_columns.keys()
            for item in self.items:
                for field in fields:
                    expand = table_columns[field].get('expand')
                    value = item.get_value(field, expand=expand)
                    if isinstance(value, list):
                        value = ", ".join([unicode(x) for x in value])
                    else:
                        value = unicode(value)
                    if re_expr.search(value):
                        filtered_items.append(item)
                        break
            self.items = filtered_items


class BaseFactory(object):

    def __init__(self, clazz):
        """Factory to create of load instances of the clazz.

        :clazz: The clazz of which new items will be created

        """
        self._clazz = clazz

    def create(self, user):
        """Will create a new instance of clazz. The instance is it is not saved
        persistent at this moment. The method will also take care of
        setting the correct ownership.

        :user: User instance will own the new created item
        :returns: Instance of clazz

        """
        item = self._clazz()
        # Try to set the ownership of the entry if the item provides the
        # fields.
        if (hasattr(item, 'uid')
           and user is not None):
            item.uid = user.id
        if (hasattr(item, 'gid')):
            if (user is not None and user.gid):
                item.gid = user.gid
            else:
                modul = item.get_item_modul()
                default_gid = modul.gid
                item.gid = default_gid
        return item

    def load(self, id, db=None, cache="", uuid=False):
        """Loads the item with id from the database and returns it.

        :id: ID of the item to be loaded
        :db: DB session to load the item
        :cache: Name of the cache region. If empty then no caching is
                done.
        :uuid: If true the given id is a uuid. Default to false
        :returns: Instance of clazz

        """
        if db is None:
            db = DBSession
        q = db.query(self._clazz)
        if cache in regions.keys():
            q = set_relation_caching(q, self._clazz, cache)
            q = q.options(FromCache(cache))
        for relation in self._clazz._sql_eager_loads:
            q = q.options(joinedload(relation))
        if uuid:
            return q.filter(self._clazz.uuid == id).one()
        else:
            return q.filter(self._clazz.id == id).one()
