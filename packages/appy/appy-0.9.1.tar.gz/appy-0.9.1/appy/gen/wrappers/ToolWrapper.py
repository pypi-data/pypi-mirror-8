# ------------------------------------------------------------------------------
import os.path, time
import appy
from appy.px import Px
from appy.gen.mail import sendMail
from appy.gen.wrappers import AbstractWrapper
from appy.shared.utils import executeCommand
# ------------------------------------------------------------------------------
class ToolWrapper(AbstractWrapper):

    # --------------------------------------------------------------------------
    # Navigation-related PXs
    # --------------------------------------------------------------------------
    # Icon for hiding/showing details below the title of an object shown in a
    # list of objects.
    pxShowDetails = Px('''
     <img if="(field.name == 'title') and ztool.subTitleIsUsed(className)"
          class="clickable" src=":url('toggleDetails')"
          onclick="toggleSubTitles()"/>''')

    # Displays up/down arrows in a table header column for sorting a given
    # column. Requires variables "sortable", 'filterable' and 'field'.
    pxSortAndFilter = Px('''
     <x if="sortable">
      <img if="(sortKey != field.name) or (sortOrder == 'desc')"
           onclick=":navBaseCall.replace('**v**', '0,%s,%s,%s' % \
                     (q(field.name), q('asc'), q(filterKey)))"
           src=":url('sortDown.gif')" class="clickable"/>
      <img if="(sortKey != field.name) or (sortOrder == 'asc')"
           onclick=":navBaseCall.replace('**v**', '0,%s,%s,%s' % \
                     (q(field.name), q('desc'), q(filterKey)))"
           src=":url('sortUp.gif')" class="clickable"/>
     </x>
     <x if="filterable"
        var2="filterId='%s_%s' % (ajaxHookId, field.name);
              filterIdIcon='%s_icon' % filterId">
      <!-- Pressing the "enter" key in the field clicks the icon (onkeydown)--> 
      <input type="text" size="7" id=":filterId"
             value=":filterKey == field.name and filterValue or ''"
             onkeydown=":'if (event.keyCode==13) document.getElementById ' \
                         '(%s).click()' % q(filterIdIcon)"/>
      <img id=":filterIdIcon" class="clickable" src=":url('funnel')"
           onclick=":navBaseCall.replace('**v**', '0, %s,%s,%s' % \
                     (q(sortKey), q(sortOrder), q(field.name)))"/>
     </x>''')

    # Buttons for navigating among a list of objects (from a Ref field or a
    # query): next,back,first,last...
    pxNavigate = Px('''
     <div if="totalNumber &gt; batchSize" align=":dright"
          var2="mustSortAndFilter=ajaxHookId == 'queryResult';
                sortAndFilter=mustSortAndFilter and \
                    ',%s,%s,%s' % (q(sortKey),q(sortOrder),q(filterKey)) or ''">
       
      <!-- Go to the first page -->
      <img if="(startNumber != 0) and (startNumber != batchSize)"
           class="clickable" src=":url('arrowsLeft')" title=":_('goto_first')"
           onClick=":navBaseCall.replace('**v**', '0'+sortAndFilter)"/>

      <!-- Go to the previous page -->
      <img var="sNumber=startNumber - batchSize" if="startNumber != 0"
           class="clickable" src=":url('arrowLeft')" title=":_('goto_previous')"
           onClick=":navBaseCall.replace('**v**', str(sNumber)+sortAndFilter)"/>

      <!-- Explain which elements are currently shown -->
      <span class="discreet"> 
       <x>:startNumber + 1</x> <img src=":url('to')"/> 
       <x>:startNumber + batchNumber</x> <b>//</b> 
       <x>:totalNumber</x>
      </span>

      <!-- Go to the next page -->
      <img var="sNumber=startNumber + batchSize" if="sNumber &lt; totalNumber"
           class="clickable" src=":url('arrowRight')" title=":_('goto_next')"
           onClick=":navBaseCall.replace('**v**', str(sNumber)+sortAndFilter)"/>

      <!-- Go to the last page -->
      <img var="lastPageIsIncomplete=totalNumber % batchSize;
                nbOfCompletePages=totalNumber/batchSize;
                nbOfCountedPages=lastPageIsIncomplete and \
                                 nbOfCompletePages or nbOfCompletePages-1;
                sNumber= nbOfCountedPages * batchSize"
           if="(startNumber != sNumber) and \
               (startNumber != sNumber-batchSize)" class="clickable"
           src=":url('arrowsRight')" title=":_('goto_last')"
           onClick=":navBaseCall.replace('**v**', str(sNumber)+sortAndFilter)"/>

      <!-- Go to the element number... -->
      <x var="gotoNumber=gotoNumber|False" if="gotoNumber"
         var2="sourceUrl=obj.url">:obj.pxGotoNumber</x>
     </div>''')

    # --------------------------------------------------------------------------
    # PXs for graphical elements shown on every page
    # --------------------------------------------------------------------------
    # Global elements included in every page.
    pxPagePrologue = Px('''
     <!-- Include type-specific CSS and JS. -->
     <x if="cssJs">
      <link for="cssFile in cssJs['css']" rel="stylesheet" type="text/css"
            href=":url(cssFile)"/>
      <script for="jsFile in cssJs['js']" type="text/javascript"
              src=":url(jsFile)"></script></x>

     <!-- Javascript messages -->
     <script type="text/javascript">::ztool.getJavascriptMessages()</script>

     <!-- Global form for deleting an object -->
     <form id="deleteForm" method="post" action="do">
      <input type="hidden" name="action" value="Delete"/>
      <input type="hidden" name="objectUid"/>
     </form>
     <!-- Global form for deleting an event from an object's history -->
     <form id="deleteEventForm" method="post" action="do">
      <input type="hidden" name="action" value="DeleteEvent"/>
      <input type="hidden" name="objectUid"/>
      <input type="hidden" name="eventTime"/>
     </form>
     <!-- Global form for (un)linking (an) object(s) -->
     <form id="linkForm" method="post" action="do">
      <input type="hidden" name="action" value="Link"/>
      <input type="hidden" name="linkAction"/>
      <input type="hidden" name="sourceUid"/>
      <input type="hidden" name="fieldName"/>
      <input type="hidden" name="targetUid"/>
      <input type="hidden" name="semantics"/>
     </form>
     <!-- Global form for unlocking a page -->
     <form id="unlockForm" method="post" action="do">
      <input type="hidden" name="action" value="Unlock"/>
      <input type="hidden" name="objectUid"/>
      <input type="hidden" name="pageName"/>
     </form>
     <!-- Global form for generating/freezing a document from a pod template -->
     <form id="podForm" name="podForm" method="post"
           action=":ztool.absolute_url() + '/doPod'">
      <input type="hidden" name="objectUid"/>
      <input type="hidden" name="fieldName"/>
      <input type="hidden" name="template"/>
      <input type="hidden" name="podFormat"/>
      <input type="hidden" name="queryData"/>
      <input type="hidden" name="customParams"/>
      <input type="hidden" name="showSubTitles" value="true"/>
      <input type="hidden" name="checkedUids"/>
      <input type="hidden" name="checkedSem"/>
      <input type="hidden" name="mailing"/>
      <input type="hidden" name="action" value="generate"/>
     </form>''')

    pxPageBottom = Px('''
     <script var="info=zobj.getSlavesRequestInfo(page)"
             type="text/javascript">:'initSlaves(%s,%s,%s,%s)' % \
                    (q(zobj.absolute_url()), q(layoutType), info[0], info[1])
     </script>''')

    pxPortlet = Px('''
     <x var="toolUrl=tool.url;
             queryUrl='%s/query' % toolUrl;
             currentSearch=req.get('search', None);
             currentClass=req.get('className', None);
             currentPage=req['PATH_INFO'].rsplit('/',1)[-1];
             rootClasses=ztool.getRootClasses()">

      <!-- One section for every searchable root class -->
      <x for="rootClass in rootClasses" if="ztool.userMaySearch(rootClass)"
         var2="className=ztool.getPortalType(rootClass)">

       <!-- A separator if required -->
       <div class="portletSep" if="loop.rootClass.nb != 0"></div>

       <!-- Section title (link triggers the default search) -->
       <div class="portletContent"
            var="searchInfo=ztool.getGroupedSearches(rootClass)">
        <div class="portletTitle">
         <a var="queryParam=searchInfo.default and \
                            searchInfo.default.name or ''"
            href=":'%s?className=%s&amp;search=%s' % \
                   (queryUrl, className, queryParam)"
            class=":(not currentSearch and (currentClass==className) and \
                    (currentPage=='query')) and \
                    'current' or ''">::_(className + '_plural')</a>
        </div>

        <!-- Create instances of this class -->
        <form if="ztool.userMayCreate(rootClass) and \
                  ('form' in ztool.getCreateMeans(rootClass))" class="addForm"
              var2="target=ztool.getLinksTargetInfo(rootClass)"
              action=":'%s/do' % toolUrl" target=":target.target">
         <input type="hidden" name="action" value="Create"/>
         <input type="hidden" name="className" value=":className"/>
         <input type="hidden" name="popup"
               value=":(inPopup or (target.target != '_self')) and '1' or '0'"/>
         <input type="submit" class="buttonSmall button"
                var="label=_('query_create')" value=":label"
                onclick=":target.openPopup"
                style=":'%s; %s' % (url('add', bg=True), \
                                    ztool.getButtonWidth(label))"/>
        </form>

        <!-- Searches -->
        <x if="ztool.advancedSearchEnabledFor(rootClass)">
         <!-- Live search -->
         <form action=":'%s/do' % toolUrl">
          <input type="hidden" name="action" value="SearchObjects"/>
          <input type="hidden" name="className" value=":className"/>
          <table cellpadding="0" cellspacing="0">
           <tr valign="bottom">
            <td><input type="text" size="14" name="w_SearchableText"
                       class="inputSearch"/></td>
            <td>
             <input type="image" class="clickable" src=":url('search')"
                    title=":_('search_button')"/></td>
           </tr>
          </table>
         </form>

         <!-- Advanced search -->
         <div var="highlighted=(currentClass == className) and \
                               (currentPage == 'search')"
              class=":highlighted and 'portletSearch current' or \
                     'portletSearch'"
              align=":dright" style="margin-bottom: 4px">
          <a var="text=_('search_title')" style="font-size: 88%"
             href=":'%s/search?className=%s' % (toolUrl, className)"
             title=":text"><x>:text</x>...</a>
         </div>
        </x>

        <!-- Predefined searches -->
        <x for="search in searchInfo.searches" var2="field=search">
         <x if="search.type == 'group'">:search.px</x>
         <x if="search.type != 'group'">:search.pxView</x>
        </x>
        <!-- Portlet bottom, potentially customized by the app -->
        <x>::ztool.portletBottom(rootClass)</x>
       </div>
      </x>
     </x>''')

    # The message that is shown when a user triggers an action.
    pxMessage = Px('''
     <div class=":inPopup and 'messagePopup message' or 'message'"
          style="display:none" id="appyMessage">
      <!-- The icon for closing the message -->
      <img src=":url('close')" align=":dright" class="clickable"
           onclick="this.parentNode.style.display='none'"/>
      <!-- The message content -->
      <div id="appyMessageContent"></div>
     </div>
     <script type="text/javascript" var="messages=ztool.consumeMessages()"
             if="messages">::'showAppyMessage(%s)' % q(messages)</script>''')

    # The page footer.
    pxFooter = Px('''
     <table cellpadding="0" cellspacing="0" width="100%" class="footer">
      <tr>
       <td align=":dright">Made with
        <a href="http://appyframework.org" target="_blank">Appy</a></td></tr>
     </table>''')

    # Hook for defining a PX that proposes additional links, after the links
    # corresponding to top-level pages.
    pxLinks = Px('')

    # Hook for defining a PX that proposes additional icons after standard
    # icons in the user strip.
    pxIcons = Px('')

    # Displays the content of a layouted object (a page or a field). If the
    # layouted object is a page, the "layout target" (where to look for PXs)
    # will be the object whose page is shown; if the layouted object is a field,
    # the layout target will be this field.
    pxLayoutedObject = Px('''
     <table var="layoutCss=layout.css_class;
                 isCell=layoutType == 'cell'"
            cellpadding=":layout.cellpadding"
            cellspacing=":layout.cellspacing"
            width=":not isCell and layout.width or ''"
            align=":not isCell and \
                   ztool.flipLanguageDirection(layout.align, dir) or ''"
            class=":tagCss and ('%s %s' % (tagCss, layoutCss)).strip() or \
                   layoutCss"
            style=":layout.style" id=":tagId" name=":tagName">

      <!-- The table header row -->
      <tr if="layout.headerRow" valign=":layout.headerRow.valign">
       <th for="cell in layout.headerRow.cells" width=":cell.width"
           align=":ztool.flipLanguageDirection(cell.align, dir)">
       </th>
      </tr>
      <!-- The table content -->
      <tr for="row in layout.rows" valign=":row.valign">
       <td for="cell in row.cells" colspan=":cell.colspan"
           align=":ztool.flipLanguageDirection(cell.align, dir)"
           class=":not loop.cell.last and 'cellGap' or ''">
        <x for="pxName in cell.content">
         <x var="px=(pxName == '?') and 'px%s' % layoutType.capitalize() \
                                    or pxName">:getattr(layoutTarget, px)</x>
         <img if="not loop.pxName.last" src=":url('space.gif')"/>
        </x>
       </td>
      </tr>
     </table>''')

    pxHome = Px('''
     <table>
      <tr valign="middle">
       <td align="center">::_('front_page_text')</td>
      </tr>
     </table>''', template=AbstractWrapper.pxTemplate, hook='content')

    # Show on query list or grid, the field content for a given object.
    pxQueryField = Px('''
     <!-- Title -->
     <x if="field.name == 'title'">
      <x if="mayView"
         var2="navInfo='search.%s.%s.%d.%d' % \
                (className, searchName, startNumber+currentNumber, totalNumber);
               titleMode=inPopup and 'select' or 'link';
               pageName=zobj.getDefaultViewPage();
               selectJs=inPopup and 'onSelectObject(%s,%s,%s)' % (q(cbId), \
                          q(rootHookId), q(uiSearch.initiator.url))">
       <x var="sup=zobj.getSupTitle(navInfo)" if="sup">::sup</x>
       <x>::zobj.getListTitle(mode=titleMode, nav=navInfo, target=target, \
                          page=pageName, inPopup=inPopup, selectJs=selectJs)</x>
       <span style=":showSubTitles and 'display:inline' or 'display:none'"
             name="subTitle" var="sub=zobj.getSubTitle()" if="sub">::sub</span>

       <!-- Actions -->
       <table class="noStyle" if="not inPopup and zobj.mayAct()">
        <tr>
         <!-- Edit -->
         <td if="zobj.mayEdit()">
          <a var="navInfo='search.%s.%s.%d.%d' % \
               (className, searchName, loop.zobj.nb+1+startNumber, totalNumber);
                  linkInPopup=inPopup or (target.target != '_self')"
             target=":target.target" onclick=":target.openPopup"
             href=":zobj.getUrl(mode='edit', page=zobj.getDefaultEditPage(), \
                                nav=navInfo, inPopup=linkInPopup)">
          <img src=":url('edit')" title=":_('object_edit')"/></a>
         </td>
         <td>
          <!-- Delete -->
          <img if="zobj.mayDelete()" class="clickable" src=":url('delete')"
               title=":_('object_delete')"
               onClick=":'onDeleteObject(%s)' % q(zobj.id)"/>
         </td>
         <!-- Workflow transitions -->
         <td if="zobj.showTransitions('result')"
             var2="targetObj=zobj;
                   buttonsMode='small'">:targetObj.appy().pxTransitions</td>
        </tr>
       </table>
      </x>
      <x if="not mayView">
       <img src=":url('fake')" style="margin-right: 5px"/>
       <x>:_('unauthorized')</x>
      </x>
     </x>
     <!-- Any other field -->
     <x if="(field.name != 'title') and mayView">
      <x var="layoutType='cell'; innerRef=True"
         if="field.isShowable(zobj, 'result')">:field.pxRender</x>
     </x>''')

    # Show query results as a list.
    pxQueryResultList = Px('''
     <x var="showHeaders=showHeaders|True;
             checkboxes=uiSearch.search.checkboxes;
             checkboxesId=rootHookId + '_objs';
             cbShown=uiSearch.showCheckboxes();
             cbDisplay=cbShown and 'display:table-cell' or 'display:none'">
      <table class="list" width="100%">
       <!-- Headers, with filters and sort arrows -->
       <tr if="showHeaders">
        <th if="checkboxes" class="cbCell" style=":cbDisplay">
         <img src=":url('checkall')" class="clickable"
              title=":_('check_uncheck')"
              onclick=":'toggleAllCbs(%s)' % q(checkboxesId)"/>
        </th>
        <th for="column in columns"
            var2="field=column.field;
                  sortable=ztool.isSortable(field.name, className, 'search');
                  filterable=field.filterable"
            width=":column.width" align=":column.align">
         <x>::ztool.truncateText(_(field.labelId))</x>
         <x>:tool.pxSortAndFilter</x><x>:tool.pxShowDetails</x>
        </th>
       </tr>

       <!-- Results -->
       <tr if="not zobjects">
        <td colspan=":len(columns)+1">:_('query_no_result')</td>
       </tr>
       <tr for="zobj in zobjects" valign="top"
           var2="@currentNumber=currentNumber + 1;
                 obj=zobj.appy(); mayView=zobj.mayView();
                 cbId='%s_%s' % (checkboxesId, currentNumber)"
           class=":loop.zobj.odd and 'even' or 'odd'">
        <!-- A checkbox if required -->
        <td if="checkboxes" class="cbCell" id=":cbId" style=":cbDisplay">
         <input type="checkbox" name=":checkboxesId" checked="checked"
                value=":zobj.id" onclick="toggleCb(this)"/>
        </td>
        <td for="column in columns"
            var2="field=column.field" id=":'field_%s' % field.name"
            width=":column.width"
            align=":column.align">:tool.pxQueryField</td>
       </tr>
      </table>
      <!-- The button for selecting objects and closing the popup. -->
      <div if="inPopup and cbShown" align=":dleft">
       <input type="button" class="button"
              var="label=_('object_link_many')"
              value=":label"
              onclick=":'onSelectObjects(%s,%s,%s,%s,%s,%s,%s)' % \
               (q(rootHookId), q(uiSearch.initiator.url), \
                q(uiSearch.initiatorMode), q(sortKey), q(sortOrder), \
                q(filterKey), q(filterValue))"
              style=":'%s; %s' % (url('linkMany', bg=True), \
                                  ztool.getButtonWidth(label))"/>
      </div>
      <!-- Init checkboxes if present. -->
      <script if="checkboxes">:'initCbs(%s)' % q(checkboxesId)</script>
      <script>:'initFocus(%s)' % q(ajaxHookId)</script></x>''')

    # Show query results as a grid.
    pxQueryResultGrid = Px('''
     <table width="100%"
            var="modeElems=resultMode.split('_');
                 cols=(len(modeElems)==2) and int(modeElems[1]) or 4;
                 rows=ztool.splitList(zobjects, cols)">
      <tr for="row in rows" valign="middle">
       <td for="zobj in row" width=":'%d%%' % (100/cols)" align="center"
           style="padding-top: 25px"
           var2="obj=zobj.appy(); mayView=zobj.mayView()">
        <x var="currentNumber=currentNumber + 1"
           for="column in columns"
           var2="field=column.field">:tool.pxQueryField</x>
       </td>
      </tr>
     </table>''')

    # Show paginated query results as a list or grid.
    pxQueryResult = Px('''
     <div var="ajaxHookId='queryResult';
               _=ztool.translate;
               className=req['className'];
               searchName=req.get('search', '');
               uiSearch=uiSearch|ztool.getSearch(className,searchName,ui=True);
               rootHookId=uiSearch.getRootHookId();
               refInfo=ztool.getRefInfo();
               refObject=refInfo[0];
               refField=refInfo[1];
               refUrlPart=refObject and ('&amp;ref=%s:%s' % (refObject.id, \
                                                             refField)) or '';
               startNumber=req.get('startNumber', '0');
               startNumber=int(startNumber);
               sortKey=req.get('sortKey', '');
               sortOrder=req.get('sortOrder', 'asc');
               filterKey=req.get('filterKey', '');
               filterValue=req.get('filterValue', '');
               queryResult=ztool.executeQuery(className, \
                   search=uiSearch.search, startNumber=startNumber, \
                   remember=True, sortBy=sortKey, sortOrder=sortOrder, \
                   filterKey=filterKey, filterValue=filterValue, \
                   refObject=refObject, refField=refField);
               zobjects=queryResult.objects;
               totalNumber=queryResult.totalNumber;
               batchSize=queryResult.batchSize;
               batchNumber=len(zobjects);
               navBaseCall='askQueryResult(%s,%s,%s,%s,%s,**v**)' % \
                 (q(ajaxHookId), q(ztool.absolute_url()), q(className), \
                  q(searchName),int(inPopup));
               showNewSearch=showNewSearch|True;
               newSearchUrl='%s/search?className=%s%s' % \
                   (ztool.absolute_url(), className, refUrlPart);
               showSubTitles=req.get('showSubTitles', 'true') == 'true';
               resultMode=ztool.getResultMode(className);
               target=ztool.getLinksTargetInfo(ztool.getAppyClass(className))"
          id=":ajaxHookId">

      <x if="zobjects or filterValue">
       <!-- Display here POD templates if required. -->
       <table var="fields=ztool.getResultPodFields(className);
                   layoutType='view'"
              if="not inPopup and zobjects and fields" align=":dright">
        <tr>
         <td var="zobj=zobjects[0]; obj=zobj.appy()"
             for="field in fields"
             class=":not loop.field.last and 'pod' or ''">:field.pxRender</td>
        </tr>
       </table>

       <!-- The title of the search -->
       <p if="not inPopup">
        <x>::uiSearch.translated</x> (<span class="discreet">:totalNumber</span>)
        <x if="showNewSearch and (searchName == 'customSearch')">&nbsp;&mdash;
         &nbsp;<i><a href=":newSearchUrl">:_('search_new')</a></i>
        </x>
       </p>
       <table width="100%">
        <tr valign="top">
         <!-- Search description -->
         <td if="uiSearch.translatedDescr">
          <span class="discreet">:uiSearch.translatedDescr</span><br/>
         </td>
         <!-- (Top) navigation -->
         <td align=":dright" width="150px">:tool.pxNavigate</td>
        </tr>
       </table>

       <!-- Results, as a list or grid -->
       <x var="columnLayouts=ztool.getResultColumnsLayouts(className, refInfo);
               columns=ztool.getColumnsSpecifiers(className,columnLayouts, dir);
               currentNumber=0">
        <x if="resultMode == 'list'">:tool.pxQueryResultList</x>
        <x if="resultMode != 'list'">:tool.pxQueryResultGrid</x>
       </x>

       <!-- (Bottom) navigation -->
       <x>:tool.pxNavigate</x>
      </x>

      <x if="not zobjects and not filterValue">
       <x>:_('query_no_result')</x>
       <x if="showNewSearch and (searchName == 'customSearch')"><br/>
        <i class="discreet"><a href=":newSearchUrl">:_('search_new')</a></i></x>
      </x>
    </div>''')

    pxQuery = Px('''
     <div var="className=req['className'];
               searchName=req.get('search', '');
               uiSearch=ztool.getSearch(className, searchName, ui=True);
               rootHookId=uiSearch.getRootHookId();
               cssJs=None"
          id=":rootHookId">
      <script type="text/javascript">:uiSearch.search.getCbJsInit(rootHookId)
      </script>
      <x>:tool.pxPagePrologue</x><x>:tool.pxQueryResult</x>
     </div>''', template=AbstractWrapper.pxTemplate, hook='content')

    pxSearch = Px('''
     <x var="className=req['className'];
             refInfo=req.get('ref', None);
             searchInfo=ztool.getSearchInfo(className, refInfo);
             cssJs={};
             layoutType='search';
             x=ztool.getCssJs(searchInfo.fields, 'edit', cssJs)">

      <!-- Include type-specific CSS and JS. -->
      <link for="cssFile in cssJs['css']" rel="stylesheet" type="text/css"
            href=":url(cssFile)"/>
      <script for="jsFile in cssJs['js']" type="text/javascript"
              src=":url(jsFile)"></script>

      <!-- Search title -->
      <h1><x>:_('%s_plural'%className)</x> &ndash;
          <x>:_('search_title')</x></h1>
      <!-- Form for searching objects of request/className. -->
      <form name="search" action=":ztool.absolute_url()+'/do'" method="post">
       <input type="hidden" name="action" value="SearchObjects"/>
       <input type="hidden" name="className" value=":className"/>
       <input if="refInfo" type="hidden" name="ref" value=":refInfo"/>

       <table width="100%">
        <tr for="searchRow in ztool.getGroupedSearchFields(searchInfo)"
            valign="top">
         <td for="field in searchRow" class="search"
             var2="scolspan=field and field.scolspan or 1"
             colspan=":scolspan"
             width=":'%d%%' % ((100/searchInfo.nbOfColumns)*scolspan)">
           <x if="field">:field.pxRender</x>
           <br class="discreet"/>
         </td>
        </tr>
       </table>

       <!-- Submit button -->
       <p align=":dright"><br/>
        <input type="submit" class="button" var="label=_('search_button')"
               value=":label"
               style=":'%s; %s' % (url('search', bg=True), \
                                   ztool.getButtonWidth(label))"/>
       </p>
      </form>
     </x>''', template=AbstractWrapper.pxTemplate, hook='content')

    pxBack = Px('''
     <html>
      <head>
       <script src=":ztool.getIncludeUrl('appy.js')" type="text/javascript">
       </script>
      </head>
      <body>
       <script type="text/javascript">backFromPopup()</script>
      </body>
     </html>''')

    def isManager(self):
        '''Some pages on the tool can only be accessed by managers.'''
        if self.user.has_role('Manager'): return 'view'

    def isManagerEdit(self):
        '''Some pages on the tool can only be accessed by managers, also in
           edit mode.'''
        if self.user.has_role('Manager'): return True

    def computeConnectedUsers(self):
        '''Computes a table showing users that are currently connected.'''
        res = '<table cellpadding="0" cellspacing="0" class="list">' \
              '<tr><th></th><th>%s</th></tr>' % \
              self.translate('last_user_access')
        rows = []
        for userId, lastAccess in self.o.loggedUsers.items():
            user = self.search1('User', noSecurity=True, login=userId)
            if not user: continue # Could have been deleted in the meanwhile
            fmt = '%s (%s)' % (self.dateFormat, self.hourFormat)
            access = time.strftime(fmt, time.localtime(lastAccess))
            rows.append('<tr><td><a href="%s">%s</a></td><td>%s</td></tr>' % \
                        (user.o.absolute_url(), user.title,access))
        return res + '\n'.join(rows) + '</table>'

    def getObject(self, uid):
        '''Allow to retrieve an object from its unique identifier p_uid.'''
        return self.o.getObject(uid, appy=True)

    def getDiskFolder(self):
        '''Returns the disk folder where the Appy application is stored.'''
        return self.o.config.diskFolder

    def getClass(self, zopeName):
        '''Gets the Appy class corresponding to technical p_zopeName.'''
        return self.o.getAppyClass(zopeName)

    def getAvailableLanguages(self):
        '''Returns the list of available languages for this application.'''
        return [(t.id, t.title) for t in self.translations]

    def convert(self, fileName, format):
        '''Launches a UNO-enabled Python interpreter as defined in the self for
           converting, using OpenOffice in server mode, a file named p_fileName
           into an output p_format.'''
        convScript = '%s/pod/converter.py' % os.path.dirname(appy.__file__)
        cmd = '%s %s "%s" %s -p%d' % (self.unoEnabledPython, convScript,
                                      fileName, format, self.openOfficePort)
        self.log('executing %s...' % cmd)
        return executeCommand(cmd) # The result can contain an error message

    def sendMail(self, to, subject, body, attachments=None):
        '''Sends a mail. See doc for appy.gen.mail.sendMail.'''
        mailConfig = self.o.getProductConfig(True).mail
        sendMail(mailConfig, to, subject, body, attachments=attachments,
                 log=self.log)

    def formatDate(self, date, format=None, withHour=True, language=None):
        '''Check doc @ToolMixin::formatDate.'''
        if not date: return
        return self.o.formatDate(date, format, withHour, language)

    def getUserName(self, login=None, normalized=False):
        return self.o.getUserName(login=login, normalized=normalized)

    def refreshCatalog(self, startObject=None):
        '''Reindex all Appy objects. For some unknown reason, method
           catalog.refreshCatalog is not able to recatalog Appy objects.'''
        if not startObject:
            # This is a global refresh. Clear the catalog completely, and then
            # reindex all Appy-managed objects, ie those in folders "config"
            # and "data".
            # First, clear the catalog.
            self.log('recomputing the whole catalog...')
            app = self.o.getParentNode()
            app.catalog._catalog.clear()
            nb = 1
            failed = []
            for obj in app.config.objectValues():
                subNb, subFailed = self.refreshCatalog(startObject=obj)
                nb += subNb
                failed += subFailed
            try:
                app.config.reindex()
            except:
                failed.append(app.config)
            # Then, refresh objects in the "data" folder.
            for obj in app.data.objectValues():
                subNb, subFailed = self.refreshCatalog(startObject=obj)
                nb += subNb
                failed += subFailed
            # Re-try to index all objects for which reindexation has failed.
            for obj in failed: obj.reindex()
            if failed:
                failMsg = ' (%d retried)' % len(failed)
            else:
                failMsg = ''
            self.log('%d object(s) reindexed%s.' % (nb, failMsg))
        else:
            nb = 1
            failed = []
            for obj in startObject.objectValues():
                subNb, subFailed = self.refreshCatalog(startObject=obj)
                nb += subNb
                failed += subFailed
            try:
                startObject.reindex()
            except Exception, e:
                failed.append(startObject)
            return nb, failed

    def _login(self, login):
        '''Performs a login programmatically. Used by the test system.'''
        self.request.user = self.search1('User', noSecurity=True, login=login)
# ------------------------------------------------------------------------------
