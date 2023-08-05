#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
import colander
import deform
import sqlalchemy
from deform import Form
from sqlalchemy import types as sa_types
from sqlalchemy.dialects.postgresql import HSTORE, JSON

from sacrud.common import get_relationship
from sacrud.exttype import ChoiceType, ElfinderString, FileStore, GUID, SlugType

from .widgets import (ElfinderWidget, HiddenCheckboxWidget, HstoreWidget,
                      SlugWidget)

# Map sqlalchemy types to colander types.
_TYPES = {
    sa_types.BigInteger: colander.Integer,
    sa_types.Boolean: colander.Boolean,
    sa_types.Date: colander.Date,
    sa_types.DateTime: colander.DateTime,
    sa_types.Enum: colander.String,
    sa_types.Float: colander.Float,
    sa_types.Integer: colander.Integer,
    sa_types.Numeric: colander.Decimal,
    sa_types.SmallInteger: colander.Integer,
    sa_types.String: colander.String,
    sa_types.Text: colander.String,
    sa_types.Time: colander.Time,
    sa_types.Unicode: colander.String,
    sa_types.UnicodeText: colander.String,
    JSON: colander.String,
    HSTORE: colander.String,
    sqlalchemy.ForeignKey: colander.String,
    ChoiceType: colander.String,
    FileStore: deform.FileData,
    SlugType: colander.String,
}

# Map sqlalchemy types to deform widgets.
_WIDGETS = {
    sa_types.BigInteger: deform.widget.TextInputWidget,
    sa_types.Boolean: HiddenCheckboxWidget,
    sa_types.Date: deform.widget.DateInputWidget,
    sa_types.DateTime: deform.widget.DateTimeInputWidget,
    sa_types.Enum: deform.widget.SelectWidget,
    sa_types.Float: deform.widget.TextInputWidget,
    sa_types.Integer: deform.widget.TextInputWidget,
    sa_types.Numeric: deform.widget.TextInputWidget,
    sa_types.SmallInteger: deform.widget.TextInputWidget,
    sa_types.String: deform.widget.TextInputWidget,
    sa_types.Text: deform.widget.TextAreaWidget,
    sa_types.Time: deform.widget.TextInputWidget,
    sa_types.Unicode: deform.widget.TextInputWidget,
    sa_types.UnicodeText: deform.widget.TextAreaWidget,
    JSON: deform.widget.TextAreaWidget,
    HSTORE: HstoreWidget,
    sqlalchemy.ForeignKey: deform.widget.SelectWidget,
    ChoiceType: deform.widget.SelectWidget,
    FileStore: deform.widget.FileUploadWidget,
    ElfinderString: ElfinderWidget,
    SlugType: SlugWidget,
}


def _get_column_type_by_sa_type(sa_type):
    """
    Returns the colander type that correspondents to the sqlalchemy type
    'sa_type'.
    """
    return _TYPES.get(sa_type) or colander.String


def _get_widget_type_by_sa_type(sa_type):
    """
    Returns the deform widget that correspondents to the sqlalchemy type
    'sa_type'.
    """
    return _WIDGETS.get(sa_type) or deform.widget.TextInputWidget


class HTMLText(object):
    def __init__(self, text):
        self.text = text

    def __html__(self):
        try:
            return unicode(self.text)
        except NameError:           # pragma: no cover
            return str(self.text)   # pragma: no cover


class GroupShema(colander.Schema):
    def __init__(self, group, table, obj, dbsession):
        colander.SchemaNode.__init__(self, colander.Mapping('ignore'))
        self.obj = obj
        self.table = table
        self.relationships = get_relationship(table)
        self.dbsession = dbsession
        self.js_list = []

    def get_column_title(self, col):
        if 'verbose_name' in col.info:
            name = col.info['verbose_name']
        else:
            name = col.name
        if 'sacrud_position' in col.info:
            if col.info['sacrud_position'] == 'inline':
                if 'verbose_name' in col.info:
                    name = col.info['verbose_name']
                else:
                    name = col.sacrud_name
        return name

    def get_column_description(self, col):
        if 'description' in col.info:
            return HTMLText(col.info['description'])
        return None

    def get_column_css_styles(self, col):
        css_class = []
        if hasattr(self.table, 'sacrud_css_class'):
            for key, value in self.table.sacrud_css_class.items():
                if col in value:
                    css_class.append(key)
            return ' '.join(css_class)
        return None

    def get_column_type(self, col):
        if hasattr(col, 'type'):
            return col.type.__class__
        return None

    def get_col_default_value(self, col, obj):
        value = None
        col_type = self.get_column_type(col)
        if obj and hasattr(col, 'instance_name'):
            value = getattr(obj, col.instance_name)
        elif obj and hasattr(col, 'name'):
            try:
                value = getattr(obj, col.name, colander.null)
            except UnicodeEncodeError:
                value = colander.null
        if value is None:
            value = colander.null
        elif col_type == ChoiceType:
            value = value[0]
        if col_type == sa_types.Boolean:
            value = bool(value)
        return value

    def get_widget(self, widget_type, values, mask, css_class,
                   col):
        if widget_type == deform.widget.FileUploadWidget:
            return widget_type(None)
        return widget_type(values=values,
                           mask=mask,
                           col=col,
                           mask_placeholder='_',
                           css_class=css_class)

    def get_node(self, values=None, mask=None, **kwargs):
        column_type = _get_column_type_by_sa_type(kwargs['sa_type'])
        widget_type = _get_widget_type_by_sa_type(kwargs['sa_type'])
        if kwargs['sa_type'] == sa_types.Enum and not values:
            values = [(x, x) for x in kwargs['col'].type.enums]
        if kwargs['sa_type'] == GUID and not mask:
            mask = 'hhhhhhhh-hhhh-hhhh-hhhh-hhhhhhhhhhhh'
        if kwargs['sa_type'] == ChoiceType and not values:
            values = [(v, k) for k, v in kwargs['col'].type.choices.items()]
        if kwargs['sa_type'] == ElfinderString:
            self.js_list.append('elfinder.js')
        if kwargs['sa_type'] == SlugType:
            self.js_list.append('speakingurl.min.js')
        widget = self.get_widget(widget_type, values, mask,
                                 kwargs['css_class'],
                                 kwargs['col'])
        if widget_type == deform.widget.FileUploadWidget:
            kwargs['description'] = kwargs['default']
            kwargs['default'] = colander.null
        node = colander.SchemaNode(column_type(),
                                   title=kwargs['title'],
                                   name=kwargs['col'].name,
                                   default=kwargs['default'],
                                   description=kwargs['description'],
                                   widget=widget,
                                   )
        return node

    # TODO: rewrite it
    def get_foreign_key_node(self, **kwargs):
        from sacrud.common import pk_to_list
        fk_schema = colander.Schema()
        kwargs['sa_type'] = sqlalchemy.ForeignKey
        for rel in self.relationships:
            if kwargs['col'] in rel.remote_side or kwargs['col'] in rel.local_columns:
                choices = self.dbsession.query(rel.mapper).all()
                choices = [('', '')] + [(getattr(ch, pk_to_list(ch)[0]),
                                         ch.__repr__()) for ch in choices]
                node = self.get_node(values=choices, **kwargs)
                fk_schema.add(node)
                break
        return fk_schema

    def build(self, columns):
        for col in columns:
            node = None
            if isinstance(col, (list, tuple)):
                group = col[0]
                c = col[1]
                node = GroupShema(self.relationships, group, c,
                                  self.table, self.obj, self.dbsession)
                self.add(node)
                continue
            title = self.get_column_title(col)
            default = self.get_col_default_value(col, self.obj)
            description = self.get_column_description(col)
            css_class = self.get_column_css_styles(col)
            sa_type = self.get_column_type(col)
            params = {'col': col,
                      'sa_types': sa_type,
                      'title': title,
                      'description': description,
                      'default': default,
                      'css_class': css_class,
                      'sa_type': sa_type,
                      }

            if hasattr(col, 'foreign_keys'):
                if col.foreign_keys:
                    node = self.get_foreign_key_node(**params)
            if not node:
                node = self.get_node(**params)
            self.add(node)


class SacrudShemaNode(colander.SchemaNode):
    def __init__(self, dbsession, obj, table, columns):
        colander.SchemaNode.__init__(self, colander.Mapping('ignore'))
        self.obj = obj
        self.table = table
        self.visible_columns = columns
        self.dbsession = dbsession
        self.js_list = []

        self.build()

    def build(self):
        for group, columns in self.visible_columns:
            gs = GroupShema(group, self.table, self.obj,
                            self.dbsession)
            gs.build(columns)
            self.add(gs)
            for lib in gs.js_list:
                self.js_list.append(lib)


def form_generator(dbsession, obj, table, columns):
    schema = SacrudShemaNode(dbsession, obj, table, columns)
    return {'form': Form(schema, ),
            'js_list': schema.js_list,
            }
