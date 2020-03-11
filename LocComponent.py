'''
This script locates a component defined in manifest.xml
usage: keep focus on a value of android:name and execute script
version: jeb3.0

'''

# -*- coding: utf-8
from com.pnfsoftware.jeb.client.api import IScript, IGraphicalClientContext
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit


class LocComponent(IScript):

    def run(self, ctx):

        engctx = ctx.getEnginesContext()
        if not engctx:
            print('Back-end engines not initialized')
            return
        # print(engctx)

        projects = engctx.getProjects()
        if not projects:
            print('There is no opened project')
            return
        # print(projects)

        prj = projects[0]
        # print('=> Listing units int project "%s":' % prj.getName())
        # for art in prj.getLiveArtifacts():
        #     # print(art)
        #     for unit in art.getUnits():
        #         print(unit.getName())
        art = prj.getLiveArtifacts()[0]
        unit = art.getUnits()[0]
        package = unit.getName()
        # print(package)


        focus_view = ctx.getFocusedView()
        try:
            active_fra = focus_view.getActiveFragment()
        except:
            print("keep focus on a android:name!")
            return
        ele_name = active_fra.getActiveItemAsText()
        # print(focus_view)
        # print(active_fra)
        # print(" active_fra.getActiveAddress()", active_fra.getActiveAddress())
        # print(" active_fra.getActiveItem()", active_fra.getActiveItem())
        # print(" active_fra.getActiveItemAsText()", active_fra.getActiveItemAsText())
        # print(" active_fra.getUnit()", active_fra.getUnit())
        # print(ele_name)


        if ele_name[0:1] == '.':
            full_path = 'L' + package + ele_name + ';'
            full_path = full_path.replace('.', '/')
        else:
            full_path = 'L' + ele_name + ';'
            full_path = full_path.replace('.', '/')
        # print(full_path)


        # find, bring up, and focus on the DEX unit Disassembly fragment
        # dex = prj.findUnit(IDexUnit)  # IDexUnit
        for view in ctx.getViews():
            for fragment in view.getFragments():
                if view.getFragmentLabel(fragment) == 'Disassembly':
                    view.setFocus()
                    view.setActiveFragment(fragment)
                    # print(view)
                    # print(fragment)
                    print(full_path)
                    if fragment.setActiveAddress(full_path):
                        print("--------get location success, see the Bytecode view !---------")
                    else: print(full_path + " no exist !")
                    return
        print('Assembly fragment was not found?')