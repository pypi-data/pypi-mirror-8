# -*- coding: utf8 -*-
################################################################################
#
# Copyright (c) 2012 STEPHANE MANGIN. (http://le-spleen.net) All Rights Reserved
#                    Stéphane MANGIN <stephane.mangin@freesbee.fr>
# Copyright (c) 2012 OSIELL SARL. (http://osiell.com) All Rights Reserved
#                    Eric Flaux <contact@osiell.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
################################################################################

"""
Fields / columns binding
^^^^^^^^^^^^^^^^^^^^^^^^

"""
from csv2odoo import exceptions
from csv2odoo.constants_and_vars import STATS


class Field(object):
    """ Specify the column number (or custom value) and some special treatments
    from which the current model's field will be allocated to the object's creation.

    :param column: The column number to map to
    :type column: int
    :param field: The actual field name to map to
    :type field: str
    :param callback: Pre-treatment by a callback function
    :type callback: :class:`csv2odoo.callbaks.callback_model`
    :param search: Search for same value before object creation
    :type search: bool
    :param default: Default value if no value found or if custom value (column=None)
    :type default: object
    :param required: Is this field is required
    :type required: bool
    :param skip: Is this field is skippable
    :type skip: bool
    :param ignore: Is this field is ignorable (So object creation is skipped)
    :type ignore: bool
    :param replace: Is this field is replaceable (So it can be redifined)
    :type replace: bool
    :param update: Is this field have not to be updated if existing in database
    :type update: bool
    :param unique: Is this field value must be unique inside current model
    :type unique: bool
    :param relation: Relation to link to (:class:`csv2odoo.Model` or list of :class:`csv2odoo.Model`)
    :type relation: :class:`csv2odoo.Model`
    :param concatenate: Force concatenation of returned values
    :type concatenate: bool
    :param overwrite: Overwrite the field value in OpenERP (relation)
    :type overwrite: bool

    """

    __slots__ = ['columns', 'default', 'name', 'relation', 'unique', 'callbacks',
                 'required', 'skip', 'ignore', 'replace', 'update', 'readonly',
                 'metadata', 'overwrite', 'concatenate', 'add', 'context',
                 'init_state', 'string', 'separator']

    def __init__(self, name, columns=None, default=None, callbacks=None,
                 relation=None, required=False, readonly=False, skip=False,
                 ignore=False, replace=False, update=False, unique=False,
                 overwrite=True, separator=u',', concatenate=True, context=None):

        if context is None:
            context = {}

        if callbacks is None and columns is None\
                and relation is None and default is None:
            raise Exception(u"Columns or Callbacks are missing !")

        # This variable allow to call init each time a line begin to be
        # processed to not be forced to create an new instance by line
        self.init_state = {
            'name': name,
            'columns': columns,
            'default': default,
            'callbacks': callbacks,
            'relation': relation,
            'required': required,
            'readonly': readonly,
            'skip': skip,
            'ignore': ignore,
            'replace': replace,
            'update': update,
            'unique': unique,
            'overwrite': overwrite,
            'concatenate': concatenate,
            'separator': separator,
            'context': context,
        }

        # Saves arguments
        # ---------------
        self.name = unicode(name)
        self.string = u""
        self.default = default or u""
        self.relation = relation
        self.required = required
        self.readonly = readonly
        self.skip = skip
        self.ignore = ignore
        self.replace = replace
        self.update = update
        self.unique = unique
        self.overwrite = overwrite
        self.concatenate = concatenate
        self.separator = separator
        self.context = context

        # Metadata
        self.metadata = None

        # Check relation
        # --------------
        if relation is not None:
            if not isinstance(relation, list)\
                    and not isinstance(relation, tuple):
                self.relation = (relation, )

        # Check column
        # ------------
        if columns is not None:
            if not isinstance(columns, list)\
                    and not isinstance(columns, tuple):
                columns = (columns, )

            for index in columns:
                if not isinstance(index, int):
                    raise Exception(
                        u'Columns must be an int or a  list of int.')
        self.columns = columns

        # Check callback
        # --------------
        if callbacks is not None:
            if not isinstance(callbacks, list)\
                    and not isinstance(callbacks, tuple):
                callbacks = (callbacks,)

            for callback in callbacks:
                if not callable(callback):
                    raise Exception(u'Callbacks must be callable.')
        self.callbacks = callbacks

    def reinit(self):
        self.__init__(**self.init_state)

    def check(self, session, model, context=None):
        """Check field access fr openerp server

        :param session: An instance of :class:`csv2odoo.Session`
        :param model: An instance of :class:`csv2odoo.Model`

        """
        if context is None:
            context = {}
        session.log('debug', model, u'Checking field %(name)s...' % self)
        # FIXME: documentation on openerp priority of these two attributes if
        # FIXME: they are false, overwrite value from openerp field properties
        self.required = self.required or self._is_required(
            session, model, context=context)
        self.readonly = self.readonly or self._is_readonly(
            session, model, context=context)

    def get_metadata(self, session, model, context=None):
        """Get metadatas from fields_get methods

        :param session: An instance of :class:`csv2odoo.Session`
        :param model: An instance of :class:`csv2odoo.Model`
        :returns: dict

        example::

            {
                'string': 'Parent product',
                'required': True,
                'readonly': True,
                'relation': 'product.product',
                'context': {},
                'domain': [],
                'selectable': True,
                'type': 'many2one'
                'selectable': True,
                'size': 64,
                'selection': ((u'key',u'value'),)
                }

        """
        if context is None:
            context = {}
        if self.name in (u'id',):
            return {u'id': {}}

        res = None

        if not self.metadata:
            try:
                res = session.server.fields_get(
                    model.name, [self.name], context=context)
                if not res:
                    raise
            except Exception:
                raise exceptions.ModelDefinitionError(
                    u'Field `%s` doesn\'t seems to be configured in this model `%s`.'
                    % (self.name, model.name))
            self.metadata = res[str(self.name)]
        else:
            res = self.metadata

        if 'context' not in self.metadata:
            self.metadata['context'] = {}
        self.metadata['context'].update(context)

        return res

    def _is_readonly(self, session, model, context=None):
        """Check field access

        :param session: An instance of :class:`csv2odoo.Session`
        :param model: An instance of :class:`csv2odoo.Model`
        :returns: bool

        """
        if context is None:
            context = {}

        res = self.get_metadata(session, model, context=context)
        self.readonly = 'readonly' in res and res['readonly']
        return self.readonly

    def _is_required(self, session, model, context=None):
        """Check field requirability

        :param session: An instance of :class:`csv2odoo.Session`
        :param model: An instance of :class:`csv2odoo.Model`
        :returns: bool

        """
        if context is None:
            context = {}

        res = self.get_metadata(session, model, context=context)
        self.required = 'required' in res and res['required']
        return self.required

    def _is_field(self, session, model, context=None):
        """Check field validity

        :param session: An instance of :class:`csv2odoo.Session`
        :param model: An instance of :class:`csv2odoo.Model`
        :returns: bool

        """
        if context is None:
            context = {}
        return self.name in self.get_metadata(session, model, context=context)

    def _get_callback(self, callback, session, model, value, line):
        """Call the callback function after adding it some usefull stuff
        * get_lines method which allow to retreive a line matching values from
            columns in the actual specified line's columns
        * get_line retrieve a line by its index

        We don't intercept any Exceptions, these from callback would be masqued

        :param callback: A :class:`csv2odoo.callbacks.callback_model`
        :param session: An instance of :class:`csv2odoo.Session`
        :param model: An instance of :class:`csv2odoo.Model`
        :param value: Value to be transmitted to callback
        :type value: object
        :param line: Current full line
        :type line: list
        :returns: object

        """
        return callback(session, model.name, self.name, value, line)

    def get_data(self, session, model, line):
        """Return the value relative to the line in argument.

        :param session: An instance of :class:`csv2odoo.Session`
        :param model: An instance of :class:`csv2odoo.Model`
        :param line: The line to search for
        :type line: list
        :raises: SkipLineException, SkipObjectException, RequiredFieldError
        :returns: object

        """
        global STATS
        def _apply_callbacks(value):
            # Apply callbacks successively
            if self.callbacks:
                for callback in self.callbacks:
                    session.log(
                        u'debug', model, 
                        u'"%s" before callback `%s`: %s' % (self.name, callback.__name__, value))
                    value = self._get_callback(
                        callback, session, model, value, line)
                    session.log(
                        u'debug', model, 
                        u'"%s" after callback `%s`: %s' % (self.name, callback.__name__, value))
            return value

        def _get_columns_values():
            value = []
            if self.columns:
                # TODO: gérer chaque valeur de chaque colonne indépendamment
                try:
                    if self.default:
                        value = self.default
                    brut_values = [line[column] for column in self.columns]
                    if self.concatenate:
                        brut_values = self.separator.join(brut_values)
                    value = _apply_callbacks(brut_values)
                    if value and type(value) in (list, tuple):
                        value = u','.join(list(set(value)))
                except IndexError:
                    session.log(u'error', model, u'Columns `%s` mismatch, out of range.' % (self.columns))
            return value

        def _get_relation_values(value):
            if self.relation:

                if datatype in ('many2one', 'one2one'):
                    session.log(
                        u'debug', model, u'Create relation `%s`...' % datatype)
                    for relation in self.relation:
                        data = relation.get_data(session, line)
                        if data:
                            value = session.create(
                                relation,
                                data)
                            STATS[u'objects'][relation.string]['ids'].append(value)
                    session.log(u'debug', model, u'Result: %s' % value)

                elif datatype in ('one2many', 'many2many'):
                    value = []
                    session.log(u'debug', model,
                                u'Create relation `%s`...' % datatype)
                    for m in self.relation:
                        # TODO: manage overwrite option
                        #if self.overwrite:
                        data = m.get_data(session, line)
                        id_ = 0
                        if data:
                            id_ = session.create(m, data)
                        if id_:
                            value.append(id_)

                        session.log(u'debug', model, u'Result: %s' % value)
                        STATS[u'objects'][m.string]['ids'].extend(value)

                else:  # datatype not in (u'one2one', u'one2many', u'many2one', u'many2many'):
                    raise exceptions.BadFieldType(model, self.name)

                # Apply callbacks successively
                value = _apply_callbacks(value)

            return value


        # Retrieving field metadatas
        self.get_metadata(session, model)
        try:
            datatype = self.metadata['type']
        except:
            datatype = None

        value = _get_columns_values()
        value = _get_relation_values(value)
        if datatype in ('many2one', 'one2one'):

            session.log(u'debug', model, u'Relation `%s`...' % datatype)
            session.log(u'debug', model, u'Result: %s' % value)

        elif datatype in ('one2many', 'many2many'):

            if self.overwrite:
                session.log(u'debug', model, u'Relation `%s`...' % datatype)
                ids = []
                value = [(6, 0, value)]
                session.log(u'debug', model, u'Result: %s' % value)

            else:
                values = []
                session.log(u'debug', model, u'Relation `%s`...' % datatype)
                for m in value:
                    values.append(
                        #(4, session.create(m, m.get_data(session, line))),)
                        (4, m),)
                value = values
                session.log(u'debug', model, u'Result: %s' % value)

        # If skippable
        if self.skip and not value:
            raise exceptions.SkipLineException(u"field '%s' has value '%s'" % (self.name, value))
        # If ignorable
        if self.ignore and not value:
            session.log(u'info', model, u'%s: %s' % (self.name, value))
            raise exceptions.SkipObjectException(u"field '%s' has value '%s'" % (self.name, value))

        # Manage null values
        #===================================================================
        try:
            value.strip(u' \t\n\r\r\n')
        except:
            pass

        #Cleaning dict items with null value and ignored field
        #if data not in (0, '0', False, True) and not data[field]:
        #    if self.required:
        #        raise exceptions.RequiredFieldError(
        #            u'%s %s field is required. Skipped.' % (model, field))
        #    ToRemove_fields.append(self.name)
        #if self.router:
        #    self.router(value)
        #    del data
        # If default
        if self.default and not value:
            value = self.default

        return value

    def __str__(self):
        from_ = self.columns or (self.relation and [r.name for r in self.relation])
        return u"<Field `%s` => %s>" % (self.name, from_)

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return getattr(self, item)


class Router(Field):
    """ Specify the column number and special treatments from which the current
    model's field will be allocated to the object's creation.

    :param column: The actual column number (mandatory)
    :type column: int
    :param callback: The actual callback function
    :type callback: function

    """

    __slots__ = ['column', 'default', 'field', 'unique', 'callback', 'search',
                 'required', 'skip', 'ignore', 'replace', 'update']

    def __init__(self, column, callback):
        self.column = column
        self.default = None
        self.field = None
        self.callback = callback
        self.search = False
        self.required = False
        self.skip = False
        self.ignore = False
        self.replace = False
        self.update = False
        self.unique = False

    def configure(self, server):
        pass

    def __str__(self):
        return u"<Router %s from columns %s>" % (self.name, self.columns)
