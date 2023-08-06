# copyright 2011-2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-vcreview startup views"""

__docformat__ = "restructuredtext en"
_ = unicode

from logilab.common.decorators import cached
from logilab.mtconverter import xml_escape

from cubicweb import tags, view
from cubicweb.predicates import is_instance, rql_condition, anonymous_user
from cubicweb.uilib import domid
from cubicweb.web import component
from cubicweb.web.views import tableview

from cubes.vcreview.views import final_patch_states_rql

class AllActivePatches(view.StartupView):
    __regid__ = 'vcreview.allactivepatches'
    title = _('All active patches')

    rql = ('Any P,P,P,P,PB,PS,R '
           'GROUPBY R,P,PB,PS '
           'ORDERBY RT,PB '
           'WHERE P patch_revision RE, '
           '      RE branch PB, '
           '      P in_state PS,'
           '      RE from_repository R, '
           '      R title RT, '
           '      NOT PS name %s')

    @cached
    def filter_box_context_info(self):
        rset = self._cw.execute(self.rql % final_patch_states_rql(self._cw))
        return rset, 'vcreview.patches.table', domid(self.__regid__), False

    def call(self):
        self.w(u'<h1>%s</h1>' % self._cw._(self.title))
        rset, vid, divid, paginate = self.filter_box_context_info()
        self.wview(vid, rset, 'noresult', divid=divid)


class UserWorkList(AllActivePatches):
    __regid__ = 'vcreview.patches.worklist'
    title = _('My review worklist')

    rql = ('Any P,P,P,P,PB,PS,R '
           'GROUPBY R,P,PB,PS '
           'ORDERBY RT,PB '
           'WHERE U eid %(u)s, '
           '      P in_state PS, '
           '      P patch_revision RE, '
           '      RE branch PB, '
           '      RE from_repository R, '
           '      R title RT, '
           # Patch is pending review  and CWUser is reviewer
           '      EXISTS(PS name "pending-review" AND P patch_reviewer U) '
           # Patch is reviewed  and CWUser is commiter
           '      OR EXISTS(PS name "reviewed" AND P patch_committer U) '
           # Patch is reviewed  and CWUser repository or global commiter
           '      OR (EXISTS(PS name "reviewed"'
           '          AND NOT EXISTS(P patch_committer V) '
           '          AND (EXISTS(R repository_committer U)'
           '              OR EXISTS(R use_global_groups TRUE, U in_group G, G name "committers"))))')

    @cached
    def filter_box_context_info(self):
        rset = self._cw.execute(self.rql, {'u': self._cw.user.eid})
        return rset, 'vcreview.patches.table', domid(self.__regid__), False


class PatchesTable(tableview.TableView):
    __regid__ = 'vcreview.patches.table'
    # XXX selector

    def call(self, **kwargs):
        kwargs['paginate'] = True
        super(PatchesTable, self).call(cellvids={1: 'vcreview.patch.authors', 2: 'vcreview.patch.reviewers', 3: 'vcreview.patch.committers'},
                                       **kwargs)

    def column_label(self, colidx, default, translate_func=None):
        if colidx == 1:
            return self._cw._('author')
        if colidx == 2:
            return self._cw._('patch_reviewer')
        if colidx == 3:
            return self._cw._('patch_committer')
        return super(PatchesTable, self).column_label(colidx, default, translate_func)


class PatchAuthors(view.EntityView):
    __regid__ = 'vcreview.patch.authors'
    __select__ = is_instance('Patch')
    def entity_call(self, entity, **kwargs):
        self.w(u', '.join(set(xml_escape(rev.author) for rev in entity.patch_revision)))

class PatchReviewer(view.EntityView):
    __regid__ = 'vcreview.patch.reviewers'
    __select__ = is_instance('Patch')
    def entity_call(self, entity, **kwargs):
        self._cw.view('csv', entity.related('patch_reviewer'), 'null',
                      w=self.w)

class PatchCommitter(view.EntityView):
    __regid__ = 'vcreview.patch.committers'
    __select__ = is_instance('Patch')
    def entity_call(self, entity, **kwargs):
        self._cw.view('csv', entity.related('patch_committer'), 'null',
                      w=self.w)


class WorkListLink(component.CtxComponent):
    __regid__ = 'vcreview.worklist.warning'
    __select__ = (component.CtxComponent.__select__
                  & ~anonymous_user()
                  & rql_condition(
                      'P in_state PS, P patch_revision RE, RE from_repository R,'
                      'EXISTS(PS name "pending-review" AND P patch_reviewer U) '
                      'OR EXISTS(PS name IN ("reviewed", "deleted") AND (EXISTS(R repository_committer U) '
                      'OR EXISTS(U in_group G, G name "committers")))',
                      user_condition=True))
    context = 'left'
    order = -100

    def render(self, w, view=None):
        w(u'<table><tr><td>')
        w(tags.a(
            tags.img(src=self._cw.data_url('warning_icon.png'), alt=''),
            href=self._cw.build_url('', vid='vcreview.patches.worklist'),
            title=self._cw._('You have some patches in your worklist'),
            escapecontent=False)
          )
        w(u'</td><td>')
        w(tags.a(
            self._cw._('You have some patches in your worklist'),
            href=self._cw.build_url('', vid='vcreview.patches.worklist'))
          )
        w(u'</td></tr></table><br/>')
