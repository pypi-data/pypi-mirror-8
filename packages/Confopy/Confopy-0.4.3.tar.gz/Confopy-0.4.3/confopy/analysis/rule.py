# coding: utf-8
'''
File: rule.py
Author: Oliver Zscheyge
Description:
    Rule superclass.
'''

from localizable import Localizable
from confopy.model.document import *



class Rule(Localizable):
    """Base class to describe rule based knowledge.
    """
    def __init__(self, ID=u"", language=u"", brief=u"", description=u""):
        """Initializer.
        """
        super(Rule, self).__init__(ID, language, brief, description)

    def evaluate(self, node):
        """Evaluates the rule on a Node.
        Return:
            Bool whether this Rule is satisfied or not.
        """
        return False

    def message(self, node):
        return u""

#    def __str__(self):
#        return "Rule(%s, %s, %s)" % (self.ID, self.language, self.brief)
#
#    def __repr__(self):
#        return self.__str__()


# Predicates

def is_chapter(node):
    if isinstance(node, Chapter):
        return True
    elif isinstance(node, Section):
        parent = node.parent()
        if parent is not None and isinstance(parent, Document):
            return True
    return False

def is_section(node):
    return isinstance(node, Section)

def is_float(node):
    return node.is_float()

def has_introduction(node):
    children = node.children()
    if len(children) > 0:
        first_child = children[0]
        if isinstance(first_child, Paragraph):
            return True
    return False

def count_subsections(node):
    subsections = [child for child in node.children() if isinstance(child, Section)]
    return len(subsections)

def is_referenced(flt):
    parent = flt.parent()
    if parent is not None:
        siblings = list()
        children = parent.children()
        for child in children:
            if child.is_paragraph():
                siblings.append(child)
        para_texts = [sib.text for sib in siblings]
        para_texts = u"".join(para_texts)

        if flt.number != u"":
            return flt.number in para_texts
        flt_text = flt.text.strip().split(u" ")
        if len(flt_text) >= 2:
            flt_text = flt_text[0].strip() + u" " + flt_text[1].strip()
            flt_text = flt_text.replace(u":", u"")
            return flt_text in para_texts

    return False

FLT_CAPTION_MIN_SIZE = 3
FLT_CAPTION_NR_SIZE = 2
def has_caption(flt):
    flt_text = flt.text.strip().replace(u"\n", u" ").split(u" ")
    if flt.number != u"":
        return len(flt_text) >= FLT_CAPTION_MIN_SIZE
    return len(flt_text) >= FLT_CAPTION_MIN_SIZE + FLT_CAPTION_NR_SIZE



# Utility functions

def eval_doc(document, rules):
    """Evaluates a list of rules on a given document.
    Recursive: can be used for other nodes than Document nodes as well.
    Args:
        document: The Document to check.
        rules:    The rules to evaluate on document.
    Return:
        A list of unicode strings representing the messages
        of violated rules.
    """
    messages = list()
    for rule in rules:
        if not rule.evaluate(document):
            messages.append(rule.message(document))

    children = document.children()
    for child in children:
        messages = messages + eval_doc(child, rules)

    return messages



if __name__ == '__main__':
    print u"Test for " + __file__

    print u"  Building test document..."
    doc = Document()
    sec1 = Section(title=u"1. Foo")
    sec11 = Section(title=u"1.1 Bar")
    sec12 = Section(title=u"1.2 Baz")
    sec2 = Section(title=u"2. Raboof")
    para0 = Paragraph(text=u"Intro text")
    para1 = Paragraph(text=u"""\
Lorem ipsum dolor sit amet, consectetur adipiscing elit. In lacinia nec massa id interdum. Ut dolor mauris, mollis quis sagittis at, viverra ac mauris. Phasellus pharetra dolor neque, sit amet ultricies nibh imperdiet lobortis. Fusce ac blandit ex, eu feugiat eros. Etiam nec erat enim. Fusce at metus ac dui sagittis laoreet. Nulla suscipit nisl ut lacus viverra, a vestibulum est lacinia. Aliquam finibus urna nunc, nec venenatis mi dictum eget. Etiam vitae ante quis neque aliquam vulputate id sit amet massa. Pellentesque elementum sapien non mauris laoreet cursus. Pellentesque at mauris id ipsum viverra egestas. Sed nec volutpat metus, vel sollicitudin ante. Pellentesque interdum justo vel ullamcorper dictum. Phasellus volutpat nibh eget arcu venenatis, a bibendum lorem mattis. Quisque in laoreet leo.""")
    para2 = Paragraph(text=u"Tabelle 1 zeigt Foobar.")
    floatA = Float(text=u"Tabelle 1: Foo bar.")
    floatB = Float(text=u"Tabelle 2: Foo bar baz bat.")

    sec11.add_child(para1)
    sec11.add_child(floatA)
    sec11.add_child(para2)
    sec12.add_child(floatB)
    sec1.add_child(sec11)
    sec1.add_child(sec12)
    doc.add_child(para0)
    doc.add_child(sec1)
    doc.add_child(sec2)

    print u"  Testing has_caption..."
    assert not has_caption(floatA)
    assert has_caption(floatB)

    print u"  Testing is_referenced..."
    assert is_referenced(floatA)
    assert not is_referenced(floatB)

    print u"  Testing count_subsections..."
    assert count_subsections(doc) == 2
    assert count_subsections(sec1) == 2
    assert count_subsections(sec11) == 0
    assert count_subsections(sec2) == 0
    assert count_subsections(floatA) == 0

    print u"  Testing has_introduction..."
    assert has_introduction(doc)
    assert not has_introduction(sec1)
    assert not has_introduction(sec12)

    print u"  Testing is_chapter..."
    assert is_chapter(sec1)
    assert is_chapter(sec2)
    assert not is_chapter(sec11)
    assert not is_chapter(floatA)

    print u"Passed all tests!"
