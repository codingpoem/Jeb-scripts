'''
this script trace Id to public.xml and string.xml
version: jeb3.0
'''


# -*- coding: utf-8
from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core.output.text import ITextDocument

import re

class TraceId(IScript):

    def run(self, ctx):
        focus_view = ctx.getFocusedView()
        try:
            active_fra = focus_view.getActiveFragment()
        except:
            print("keep focus on string ID")
            return
        ele_name = active_fra.getActiveItemAsText()
        print("----------- "+ele_name)


        self.pattern = re.compile(ele_name, re.I)
        # self.pattern = re.compile("0x7f010018", re.I)

        engctx = ctx.getEnginesContext()    #IEnginesContext
        if not engctx:
            print('Back-end engines not initialized')
            return

        projects = engctx.getProjects()     #list <IRuntimeProject>
        if not projects:
            print('There is no opened project')
            return

        prj = projects[0]
        # for art in prj.getLiveArtifacts():
        #     for unit in art.getUnits():
        #         print(unit)
        art = prj.getLiveArtifacts()[0]     #ILiveArtifact
        unit = art.getUnits()[0]            #IUnit      com.huawei.wallet

        self.checkUnit(unit)


    fg = 0
    strName = ""
    def checkUnit(self, unit, level=0):
        # print('--' * level + unit.getName(), self.fg)
        if self.fg == 1:
            return
        if unit.getName() == "public.xml":
            doc = self.getTextDocument(unit)
            searchResults = self.searchTextDocument(doc, self.pattern)
            for lineIndex, matchText, fullText in searchResults:
                # print('Found in unit: %s (%s) on line %d : "%s" (full text: "%s")' % (unit.getName(), unit.getFormatType(), lineIndex, matchText, fullText))
                print("public.xml:", fullText)
                # print(fullText.split('"')[3])
                self.strName = fullText.split('"')[3]
                # self.fg = 1
            return

        if unit.getName() == "strings.xml":
            doc = self.getTextDocument(unit)
            searchResults = self.searchTextDocument1(doc, re.compile(self.strName, re.I))
            for lineIndex, matchText, fullText in searchResults:
                # print('Found in unit: %s (%s) on line %d : "%s" (full text: "%s")' % (unit.getName(), unit.getFormatType(), lineIndex, matchText, fullText))
                print("string.xml:", fullText)
                self.fg = 1
            return

        # recurse over children units
        for c in unit.getChildren():
            if self.fg == 1:
                break
            self.checkUnit(c, level + 1)

    def getTextDocument(self, srcUnit):
        formatter = srcUnit.getFormatter()      #IUnitFormatter
        # if formatter and formatter.getDocumentPresentations():      #list <IUnitDocumentPresentation>
        #     doc = formatter.getDocumentPresentations()[0].getDocument()     #IGenericDocument
        if formatter and formatter.getPresentation(0):
            doc = formatter.getPresentation(0).getDocument()
            if isinstance(doc, ITextDocument):
                return doc
        return None

    def searchTextDocument(self, doc, pattern):
        r = []
        alldoc = doc.getDocumentPart(0, 10000000)
        for i, line in enumerate(alldoc.getLines()):
            s = line.getText().toString()
            matches = pattern.findall(s)
            for match in matches:
                r.append((i + 1, match, s))
        return r


    def searchTextDocument1(self, doc, pattern):
        r = []
        des = -1
        alldoc = doc.getDocumentPart(0, 10000000)
        for i, line in enumerate(alldoc.getLines()):
            # print(i)
            s = line.getText().toString()
            matches = pattern.findall(s)
            for match in matches:
                r.append((i + 1, match, s))
                des = i + 1
            if i == des:
                r.append((i + 1, "match+1", s))
        # print("r:",r)
        # print(des)
        return r
