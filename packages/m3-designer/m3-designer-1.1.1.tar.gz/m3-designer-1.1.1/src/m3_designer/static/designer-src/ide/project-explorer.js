/**
 * Crafted by ZIgi
 */

Ext.ns('M3Designer.ide');

/**
 * Преднастроенный объект дерева структуры проекта
 */
M3Designer.ide.ProjectExplorer = Ext.extend(Ext.tree.TreePanel, {
    useArrows: true,

    id:'project-view',

    autoScroll: true,

    animate: true,

    containerScroll: true,

    border: false,

    header: false,

    rootText: 'Структура проекта',

    rootVisible:false,

    loader: new Ext.tree.TreeLoader({
        url: M3Designer.UrlMap.get('project-files')
    }),

    initComponent: function() {
        
        this.root = {
            nodeType: 'async',
            text: this.rootText,
            draggable: false,
            type:'projectRoot',
            id: 'source',
            expanded: true
        };

        this.loader = new Ext.tree.TreeLoader({
            url: M3Designer.UrlMap.get('project-files'),
            listeners: {
                'beforeload': function(treeLoader, node) {
                    treeLoader.baseParams['path'] = node.attributes['path'];
                    treeLoader.baseParams['class_name'] = node.attributes['class_name'];
                    treeLoader.baseParams['type'] = node.attributes['type'];
                }
            }
        });

        this.tbar = this.initTopBar();

        M3Designer.ide.ProjectExplorer.superclass.initComponent.call(this);

    },

    initTopBar : function () {
        var result;

        result = new Ext.Toolbar({
            items: [{
                iconCls: 'icon-tree-expand',
                tooltip:'Развернуть узлы',
                handler: this.expandButtonHandler.createDelegate(this)
            },{
                iconCls: 'icon-tree-collapse',
                tooltip:'Свернуть узлы',
                handler: this.collapseButtonHandler.createDelegate(this)
            },{
                iconCls: 'icon-arrow-refresh',
                tooltip:'Обновить структуру проекта',
                handler: this.refreshButtonHandler.createDelegate(this)
            }]
        });

        return result;
    },

    getSelectedNode: function() {
        var selectedNode = this.getSelectionModel().getSelectedNode();
        if (!selectedNode){
            Ext.Msg.show({
                title: 'Информация',
                msg: 'Для выполнения действия необходимо выделить узел дерева',
                buttons: Ext.Msg.OK,
                icon: Ext.Msg.INFO
            });
        }
        return selectedNode;
    },

    expandButtonHandler: function () {
        var selectedNode = this.getSelectedNode();
        if (selectedNode) {
            selectedNode.expand(true);
        }
    },

    collapseButtonHandler: function() {
        var selectedNode = this.getSelectedNode();
        if (selectedNode) {
            selectedNode.collapse(true);
        }
    },

    refreshButtonHandler: function() {
        var loader = this.getLoader();
        var rootNode = this.getRootNode();
        loader.load(rootNode);
        rootNode.expand();
    }

});