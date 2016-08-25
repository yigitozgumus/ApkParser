report_js = """
var tabs = new Object();

function initTabs() {
    var container = document.getElementById('tabs');
    tabs.tabs = findTabs(container);
    tabs.titles = findTitles(tabs.tabs);
    tabs.headers = findHeaders(container);
    tabs.select = select;
    tabs.deselectAll = deselectAll;
    tabs.select(0);
    return true;
}

window.onload = initTabs;

function switchTab() {
    var id = this.id.substr(1);
    for (var i = 0; i < tabs.tabs.length; i++) {
        if (tabs.tabs[i].id == id) {
            tabs.select(i);
            break;
        }
    }
    return false;
}

function select(i) {
    this.deselectAll();
    changeElementClass(this.tabs[i], 'tab selected');
    changeElementClass(this.headers[i], 'selected');
    while (this.headers[i].firstChild) {
        this.headers[i].removeChild(this.headers[i].firstChild);
    }
    var h2 = document.createElement('H2');
    h2.appendChild(document.createTextNode(this.titles[i]));
    this.headers[i].appendChild(h2);
}

function deselectAll() {
    for (var i = 0; i < this.tabs.length; i++) {
        changeElementClass(this.tabs[i], 'tab deselected');
        changeElementClass(this.headers[i], 'deselected');
        while (this.headers[i].firstChild) {
            this.headers[i].removeChild(this.headers[i].firstChild);
        }
        var a = document.createElement('A');
        a.setAttribute('id', 'ltab' + i);
        a.setAttribute('href', '#tab' + i);
        a.onclick = switchTab;
        a.appendChild(document.createTextNode(this.titles[i]));
        this.headers[i].appendChild(a);
    }
}

function changeElementClass(element, classValue) {
    if (element.getAttribute('className')) {
        /* IE */
        element.setAttribute('className', classValue)
    } else {
        element.setAttribute('class', classValue)
    }
}

function findTabs(container) {
    return findChildElements(container, 'DIV', 'tab');
}

function findHeaders(container) {
    var owner = findChildElements(container, 'UL', 'tabLinks');
    return findChildElements(owner[0], 'LI', null);
}

function findTitles(tabs) {
    var titles = new Array();
    for (var i = 0; i < tabs.length; i++) {
        var tab = tabs[i];
        var header = findChildElements(tab, 'H2', null)[0];
        header.parentNode.removeChild(header);
        if (header.innerText) {
            titles.push(header.innerText)
        } else {
            titles.push(header.textContent)
        }
    }
    return titles;
}

function findChildElements(container, name, targetClass) {
    var elements = new Array();
    var children = container.childNodes;
    for (var i = 0; i < children.length; i++) {
        var child = children.item(i);
        if (child.nodeType == 1 && child.nodeName == name) {
            if (targetClass && child.className.indexOf(targetClass) < 0) {
                continue;
            }
            elements.push(child);
        }
    }
    return elements;
}

"""
style_css = """


#summary {
    margin-top: 30px;
    margin-bottom: 40px;
}

#summary table {
    border-collapse: collapse;
}

#summary td {
    vertical-align: top;
}

.breadcrumbs, .breadcrumbs a {
    color: #606060;
}

.infoBox {
    width: 110px;
    padding-top: 15px;
    padding-bottom: 15px;
    text-align: center;
}

.infoBox p {
    margin: 0;
}

.counter, .percent {
    font-size: 120%;
    font-weight: bold;
    margin-bottom: 8px;
}

#duration {
    width: 125px;
}

#successRate, .summaryGroup {
    border: solid 2px #d0d0d0;
    -moz-border-radius: 10px;
    border-radius: 10px;
    behavior: url(css3-pie-1.0beta3.htc);
}

#successRate {
    width: 140px;
    margin-left: 35px;
}

#successRate .percent {
    font-size: 180%;
}

.success, .success a {
    color: #008000;
}

div.success, #successRate.success {
    background-color: #bbd9bb;
    border-color: #008000;
}

.failures, .failures a {
    color: #b60808;
}

div.failures, #successRate.failures {
    background-color: #ecdada;
    border-color: #b60808;
}

ul.linkList {
    padding-left: 0;
}

ul.linkList li {
    list-style: none;
    margin-bottom: 5px;
}


"""

base_style_css = """


body {
    margin: 0;
    padding: 0;
    font-family: sans-serif;
    font-size: 12pt;
}

body, a, a:visited {
    color: #303030;
}

#content {
    padding-left: 50px;
    padding-right: 50px;
    padding-top: 30px;
    padding-bottom: 30px;
}

#content h1 {
    font-size: 160%;
    margin-bottom: 10px;
}

#footer {
    margin-top: 100px;
    font-size: 80%;
    white-space: nowrap;
}

#footer, #footer a {
    color: #a0a0a0;
}

ul {
    margin-left: 0;
}

h1, h2, h3 {
    white-space: nowrap;
}

h2 {
    font-size: 120%;
}

ul.tabLinks {
    padding-left: 0;
    padding-top: 10px;
    padding-bottom: 10px;
    overflow: auto;
    min-width: 800px;
    width: auto !important;
    width: 800px;
}

ul.tabLinks li {
    float: left;
    height: 100%;
    list-style: none;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 5px;
    padding-bottom: 5px;
    margin-bottom: 0;
    -moz-border-radius: 7px;
    border-radius: 7px;
    margin-right: 25px;
    border: solid 1px #d4d4d4;
    background-color: #f0f0f0;
    behavior: url(css3-pie-1.0beta3.htc);
}

ul.tabLinks li:hover {
    background-color: #fafafa;
}

ul.tabLinks li.selected {
    background-color: #c5f0f5;
    border-color: #c5f0f5;
}

ul.tabLinks a {
    font-size: 120%;
    display: block;
    outline: none;
    text-decoration: none;
    margin: 0;
    padding: 0;
}

ul.tabLinks li h2 {
    margin: 0;
    padding: 0;
}

div.tab {
}

div.selected {
    display: block;
}

div.deselected {
    display: none;
}

div.tab table {
    min-width: 350px;
    width: auto !important;
    width: 350px;
    border-collapse: collapse;
}

div.tab th, div.tab table {
    border-bottom: solid #d0d0d0 1px;
}

div.tab th {
    text-align: left;
    white-space: nowrap;
    padding-left: 6em;
}

div.tab th:first-child {
    padding-left: 0;
}

div.tab td {
    white-space: nowrap;
    padding-left: 6em;
    padding-top: 5px;
    padding-bottom: 5px;
}

div.tab td:first-child {
    padding-left: 0;
}

div.tab td.numeric, div.tab th.numeric {
    text-align: right;
}

span.code {
    display: inline-block;
    margin-top: 0em;
    margin-bottom: 1em;
}

span.code pre {
    font-size: 11pt;
    padding-top: 10px;
    padding-bottom: 10px;
    padding-left: 10px;
    padding-right: 10px;
    margin: 0;
    background-color: #f7f7f7;
    border: solid 1px #d0d0d0;
    min-width: 700px;
    width: auto !important;
    width: 700px;
}

"""