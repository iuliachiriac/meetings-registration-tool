from flask import flash
from flask import render_template, jsonify
from flask import request, redirect, url_for
from flask.ext.login import login_required
from flask.views import MethodView

from mrt.meetings import PermissionRequiredMixin
from mrt.definitions import COLORS
from mrt.forms.admin import CategoryDefaultEditForm
from mrt.models import db, CategoryDefault
from mrt.utils import unlink_uploaded_file


class Categories(PermissionRequiredMixin, MethodView):

    decorators = (login_required,)
    permission_required = ('manage_category', )

    def get(self):
        categories = (
            CategoryDefault.query.order_by(CategoryDefault.sort)
            .order_by(CategoryDefault.id)
        )
        return render_template('admin/category/list.html',
                               categories=categories)


class CategoryEdit(PermissionRequiredMixin, MethodView):

    decorators = (login_required, )
    permission_required = ('manage_category', )

    def get(self, category_id=None):
        category = (CategoryDefault.query.get_or_404(category_id)
                    if category_id else None)
        form = CategoryDefaultEditForm(obj=category)
        return render_template('admin/category/edit.html',
                               form=form,
                               category=category,
                               colors=COLORS)

    def post(self, category_id=None):
        category = (CategoryDefault.query.get_or_404(category_id)
                    if category_id else None)
        form = CategoryDefaultEditForm(request.form, obj=category)
        if form.validate():
            form.save()
            if category_id:
                flash('Category successfully updated', 'success')
            else:
                flash('Category successfully added', 'success')
            return redirect(url_for('.categories'))
        flash('Category was not saved. Please see the errors bellow',
              'danger')
        return render_template('admin/category/edit.html',
                               form=form,
                               category=category,
                               colors=COLORS)

    def delete(self, category_id):
        category = CategoryDefault.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        unlink_uploaded_file(category.background, 'backgrounds')
        flash('Category successfully deleted', 'warning')
        return jsonify(status="success", url=url_for('.categories'))


class CategoryUpdatePosition(MethodView, PermissionRequiredMixin):

    permission_required = ('manage_category', )

    def post(self):
        items = request.form.getlist('items[]')
        for i, item in enumerate(items):
            category = (
                CategoryDefault.query.filter_by(id=item)
                .first_or_404())
            category.sort = i
        db.session.commit()
        return jsonify()
