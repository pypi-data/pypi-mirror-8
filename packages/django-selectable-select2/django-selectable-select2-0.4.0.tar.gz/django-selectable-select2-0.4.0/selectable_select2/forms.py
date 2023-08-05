from django import forms
from selectable_select2.widgets import AutoCompleteSelect2Widget


class Select2DependencyFormMixin(object):

    # a tuple of two-tuples of dependencies in form:
    # ('<fieldname>', { 'parents' : ['list', 'of', 'parent', fieldnames'],
    #                   'clearonparentchange' : True/False }
    # )
    select2_deps = tuple()

    def apply_select2_deps(self):
        for field, opts in self.select2_deps:
            parents_list = []
            fo = self.fields[field]    # get a field object
            if not isinstance(fo.widget, AutoCompleteSelect2Widget):
                raise ValueError("Widget on field {0} is not a subclass of {1}".
                                 format(field, AutoCompleteSelect2Widget.__name__))

            for parent_fname in opts.get('parents', []):
                # from a bound field get an HTML id
                parents_list.append(self[parent_fname].auto_id)
            fo.widget.parent_ids = ",".join(parents_list)
            fo.widget.clearonparentchange = bool(opts.get('clearonparentchange', True))

            parent_namemap = {}
            for fname, pname in opts.get('parents_namemap', {}).items():
                parent_namemap[self[fname].auto_id] = pname
            fo.widget.parent_namemap = parent_namemap


class Select2DependencyForm(Select2DependencyFormMixin, forms.Form):

    def __init__(self, *args, **kwargs):
        super(Select2DependencyForm, self).__init__(*args, **kwargs)
        self.apply_select2_deps()


class Select2DependencyModelForm(Select2DependencyFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Select2DependencyModelForm, self).__init__(*args, **kwargs)
        self.apply_select2_deps()
