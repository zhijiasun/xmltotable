# xmltotable
show xml with table

ConfigDataXML由xxInfo.xml和xxData.xml组成。Info.xml定义了表的结构，Data.xm定义了表的内容。
使用jquery的Datatables控件和bootstrrap-treeview在web页面来展示由xml定义的表格内容。
当前问题：
1. 期望django运行时，能够解析好XML，但目前还有几个xml的处理由异常。而且还不确定放在apps.py中是否合适。
2. 能否启用多线程来加快XML的处理
3. 静态文件的问题
4. 前台web页面是否可以针对每一列，加上超链接