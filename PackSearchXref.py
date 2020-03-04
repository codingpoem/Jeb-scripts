

from com.pnfsoftware.jeb.client.api import IScript, IGraphicalClientContext
from com.pnfsoftware.jeb.core.units.code.android import IApkUnit, IDexUnit
from com.pnfsoftware.jeb.core.actions import ActionContext
from com.pnfsoftware.jeb.core.actions import ActionXrefsData
from com.pnfsoftware.jeb.core.actions import Actions
# from com.pnfsoftware.jeb.core.units.code import ICodeUnit
# from com.pnfsoftware.jeb.core import RuntimeProjectUtil


class PackSearchXref(IScript):
    ICodeItems = []
    rows = []
    base_dir = 'hello'

    def run(self, ctx):
        if not isinstance(ctx, IGraphicalClientContext):
            print('This script must be run within a graphical client')
            return

        focus_view = ctx.getFocusedView()   #IUnitView
        if not focus_view:
            print("get view fail,please keep the caret at package in hierarchy")
            return

        focus_unit = focus_view.getUnit()   #IUnit (bytecode)
        active_item = focus_view.getActiveItem()  # return Item type,ICodeNode inherit from Item
        if not active_item:
            print("please keep the caret at package in hierarchy")
            return

        self.base_dir = active_item.getObject().getAddress()[1:-1]
        print(focus_view)
        print("focus_unit:", focus_unit)
        print("active_item:", active_item)
        print("base_dir:", self.base_dir)   # "com/android"

        #1-generate childs
        print("-----childrenClasses:-----")
        self.GenChilds(active_item)

        #2-query outside corss-reference of childs
        print("-----cross_reference outside-------")
        for item in self.ICodeItems:
            self.getCroccReference(item, focus_unit)

        #3-show results in box
        self.showBox(ctx)


    def GenChilds(self, Item):
        # type = str(Item).split(':')[0][1:]
        print(Item)
        print(Item.toString())
        type = Item.toString().split(':')[0][1:]
        if type == 'DexPackage':
            for child in Item.getChildren():
                self.GenChilds(child)
        elif type == 'Class':
            # print(Item)
            self.ICodeItems.append(Item.getObject())
            for child in Item.getChildren():
                self.GenChilds(child)
        elif type =='Field' or type =='Method':
            # print(Item)
            self.ICodeItems.append(Item.getObject())


    def getCroccReference(self, ICodeItem, unit):
        data = ActionXrefsData()
        index = 0
        if unit.prepareExecution(ActionContext(unit, Actions.QUERY_XREFS, ICodeItem.getItemId(), ICodeItem.getAddress()),data):
            addrs = data.getAddresses()
            details = data.getDetails()

            for i in range(0,len(details)):
                if details[i] != "Not a direct reference" and addrs[i].find(self.base_dir) != 1 :
                    if index == 0:
                        print("Cross-Reference:", ICodeItem.toString())
                    index += 1
                    print(addrs[i])
                    self.rows.append([addrs[i], ICodeItem.getAddress()])
        return None


    def showBox(self, ctx):
        box_caption = "cross-ref"
        box_mess = "this is optional message"
        box_headers = ["address", "address_by"]
        index = ctx.displayList(box_caption, box_mess, box_headers, self.rows)

        if index < 0:
            return
        addr = self.rows[index][0]
        print(addr)

        # find, bring up, and focus on the DEX unit Disassembly fragment
        dex = ctx.getMainProject().findUnit(IDexUnit)  # IDexUnit
        for view in ctx.getViews(dex):
            for fragment in view.getFragments():
                if view.getFragmentLabel(fragment) == 'Disassembly':
                    view.setFocus()
                    view.setActiveFragment(fragment)
                    fragment.setActiveAddress(addr)
                    return
        print('Assembly fragment was not found?')

