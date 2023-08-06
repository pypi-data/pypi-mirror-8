# -*- coding: utf-8 -*-
# copyright 2011-2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

"""cubicweb-inlinedit test for views"""

from lxml import etree, html, doctestcompare as dc

from cubicweb.devtools.testlib import CubicWebTC

def normalize(html):
    tree = dc.html_fromstring(html)
    return etree.tostring(tree, pretty_print=True)

def normtext(text):
    return isinstance(text, basestring) and text.strip() or None

def desc(node):
    out = ['<%s' % node.tag]
    if node.attrib:
        out.append(' ')
        for k, v in sorted(node.attrib.items()):
            out.append('%s=%s' % (k, v))
    if normtext(node.text):
        out.append(node.text)
    if normtext(node.tail):
        out.append(node.tail)
    out.append('>')
    return ''.join(out)

def nodeequal(a, b):
    trail = []
    try:
        if _equal(a, b, trail):
            return True, ''
    except Exception, ni:
        return False, '%s\n%s' % (ni.args[0],
                                  '\n'.join(desc(a) for a in trail))

def _equal(a, b, trail):
    trail.append(a)
    if a.tag != b.tag:
        raise Exception('tag differ: %s != %s' % (a.tag, b.tag))
    if a.attrib != b.attrib:
        raise Exception('attributes differ: %s != %s' % (sorted(a.attrib.items()),
                                                         sorted(b.attrib.items())))
    if normtext(a.text) != normtext(b.text):
        raise Exception('text differ: %s != %s' % (normtext(a.text), normtext(b.text)))
    if normtext(a.tail) != normtext(b.tail):
        raise Exception('tail differ: %s != %s' % (normtext(a.tail), normtext(b.tail)))
    if len(a) != len(b):
        raise Exception('len differ: %s != %s' % (len(a), len(b)))
    for x, y in zip(a, b):
        _equal(x, y, trail)
    return True

class InlineditNonRegressionTC(CubicWebTC):

    def setup_database(self):
        r = self.request()
        self.c = r.create_entity('Country', name=u'France')
        self.r = r.create_entity('Region', name=u'Idf', partof=self.c)
        self.l1 = r.create_entity('Language', name=u'Français', spoken_in=self.c)
        self.l2 = r.create_entity('Language', name=u'Parisien', spoken_in=self.r)

    def assertSameHtml(self, expected, computed):
        expected = normalize(expected)
        computed = normalize(computed)
        eq, nodemsg = nodeequal(dc.html_fromstring(expected),
                                dc.html_fromstring(computed))
        if not eq:
            msg = ('\n%s\n%s\n%s\n%s\n%s\n%s' %
                   ('-' * 20,
                    expected,
                    '=' * 20,
                    computed,
                    '-' * 20,
                    nodemsg))
            raise self.failureException(msg)

    def test_outputs(self):
        output = self.c.view('reledit', rtype='name')
        expected = """<div id="name-subject-%(eid)s-1-reledit" onmouseout="jQuery('#name-subject-%(eid)s-1').addClass('invisible')" onmouseover="jQuery('#name-subject-%(eid)s-1').removeClass('invisible')" class="releditField">
  <span id="name-subject-%(eid)s-1-value" class="editableFieldValue">France</span>
  <span id="name-subject-%(eid)s-1" class="editableField invisible">
    <div id="name-subject-%(eid)s-1-update" class="editableField" onclick="cw.inlinedit.loadInlineForm({&quot;reload&quot;: false, &quot;role&quot;: &quot;subject&quot;, &quot;eid&quot;: %(eid)s, &quot;fname&quot;: &quot;reledit_form&quot;, &quot;rtype&quot;: &quot;name&quot;, &quot;action&quot;: &quot;edit-rtype&quot;, &quot;divid&quot;: &quot;name-subject-%(eid)s-1&quot;});" title="click to edit this field">
      <img title="click to edit this field" src="http://testing.fr/cubicweb/data/pen_icon.png" alt="click to edit this field"/>
    </div>
  </span>
</div>"""
        self.assertSameHtml(expected % {'eid': self.c.eid}, output)

        computed = self.c.view('reledit', rtype='partof', role='object')
        self.assertSameHtml("""<div id="partof-object-%(eid)s-2-reledit" onmouseout="jQuery('#partof-object-%(eid)s-2').addClass('invisible')" onmouseover="jQuery('#partof-object-%(eid)s-2').removeClass('invisible')" class="releditField">
  <span id="partof-object-%(eid)s-2-value" class="editableFieldValue">
    <div class="edit-related-entity">
      <div class="edit-related-entity-item">
        <div id="none-none-%(reid)s-reledit" onmouseout="jQuery('#none-none-%(reid)s').addClass('invisible')" onmouseover="jQuery('#none-none-%(reid)s').removeClass('invisible')" class="releditField">
          <div id="none-none-%(reid)s-value" class="editableFieldValue">
            <a href="http://testing.fr/cubicweb/region/%(reid)s" title="">Idf</a>
          </div>
          <div id="none-none-%(reid)s" class="editableField invisible">
            <span id="none-none-%(reid)s-update" class="editableField" onclick="cw.inlinedit.loadInlineForm({&quot;container&quot;: %(eid)s, &quot;divid&quot;: &quot;none-none-%(reid)s&quot;, &quot;rtype&quot;: &quot;partof&quot;, &quot;topleveldiv&quot;: &quot;partof-object-%(eid)s-2&quot;, &quot;role&quot;: &quot;object&quot;, &quot;reload&quot;: false, &quot;fname&quot;: &quot;edit_related_form&quot;, &quot;action&quot;: &quot;edit-related&quot;, &quot;eid&quot;: %(reid)s});" title="click to edit this field">
              <img title="click to edit this field" src="http://testing.fr/cubicweb/data/pen_icon.png" alt="click to edit this field"/>
            </span>
            <span id="none-none-%(reid)s-delete" class="editableField" onclick="cw.inlinedit.loadInlineForm({&quot;container&quot;: %(eid)s, &quot;divid&quot;: &quot;none-none-%(reid)s&quot;, &quot;rtype&quot;: &quot;partof&quot;, &quot;topleveldiv&quot;: &quot;partof-object-%(eid)s-2&quot;, &quot;role&quot;: &quot;object&quot;, &quot;reload&quot;: false, &quot;fname&quot;: &quot;edit_related_form&quot;, &quot;action&quot;: &quot;delete-related&quot;, &quot;eid&quot;: %(reid)s});" title="click to delete this value">
              <img title="click to delete this value" src="http://testing.fr/cubicweb/data/cancel.png" alt="click to delete this value"/>
            </span>
          </div>
        </div>
      </div>
    </div>
  </span>
  <span id="partof-object-%(eid)s-2" class="editableField invisible">
    <div id="partof-object-%(eid)s-2-add" class="editableField" onclick="cw.inlinedit.loadInlineForm({&quot;reload&quot;: false, &quot;role&quot;: &quot;object&quot;, &quot;eid&quot;: %(eid)s, &quot;fname&quot;: &quot;reledit_form&quot;, &quot;rtype&quot;: &quot;partof&quot;, &quot;action&quot;: &quot;add-related&quot;, &quot;divid&quot;: &quot;partof-object-%(eid)s-2&quot;});" title="click to add a value">
      <img title="click to add a value" src="http://testing.fr/cubicweb/data/plus.png" alt="click to add a value"/>
    </div>
  </span>
</div>
"""  % {'eid': self.c.eid, 'reid': self.r.eid}, computed)

        computed = self.c.view('reledit', rtype='spoken_in', role='object')

        self.assertSameHtml("""<div id="spoken_in-object-%(eid)s-3-reledit" onmouseout="jQuery('#spoken_in-object-%(eid)s-3').addClass('invisible')" onmouseover="jQuery('#spoken_in-object-%(eid)s-3').removeClass('invisible')" class="releditField">
  <span id="spoken_in-object-%(eid)s-3-value" class="editableFieldValue">
    <a href="http://testing.fr/cubicweb/language/%(languageeid)s" title="">Fran&#231;ais</a>
  </span>
  <span id="spoken_in-object-%(eid)s-3" class="editableField invisible">
    <div id="spoken_in-object-%(eid)s-3-update" class="editableField" onclick="cw.inlinedit.loadInlineForm({&quot;reload&quot;: false, &quot;role&quot;: &quot;object&quot;, &quot;eid&quot;: %(eid)s, &quot;fname&quot;: &quot;reledit_form&quot;, &quot;rtype&quot;: &quot;spoken_in&quot;, &quot;action&quot;: &quot;edit-rtype&quot;, &quot;divid&quot;: &quot;spoken_in-object-%(eid)s-3&quot;});" title="click to edit this field">
      <img title="click to edit this field" src="http://testing.fr/cubicweb/data/pen_icon.png" alt="click to edit this field"/>
    </div>
  </span>
</div>
""" % {'eid': self.c.eid, 'languageeid': self.l1.eid}, computed)


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
