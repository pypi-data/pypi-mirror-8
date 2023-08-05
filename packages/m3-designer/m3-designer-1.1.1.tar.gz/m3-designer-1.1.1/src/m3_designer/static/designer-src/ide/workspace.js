﻿/**
 * Crafted by ZIgi
 */

Ext.ns('M3Designer.ide');

/**
 * @class M3Designer.ide.DesignerWorkspace
 * Это вкладка в рабочей области дизайнера. Фактически те панели и деревья
 * с которыми потом работают настоящие классы, плюс окружение по иницируещее загрузку и сохарение кода.
 * Так как это код не самого дизайнера, и писали его разные люди левой пяткой,
 * то тут всё грязно и страшно. Если кто желает прибраться - вэлком
 */
M3Designer.ide.DesignerWorkspace = Ext.extend(Ext.Panel, {
    layout: 'border',
    closable: true,
    //TODO убраться в коде
    initComponent: function () {
        M3Designer.ide.DesignerWorkspace.superclass.initComponent.call(this);
        var designPanel = new Ext.Panel({
            layout: 'fit',
            region: 'center',
            ddGroup: 'designerDDGroup'
        });

        var componentTree = new Ext.tree.TreePanel({
            root: new Ext.tree.TreeNode({
                text: 'foo',
                id: 'root',
                expanded: true
            }),
            useArrows: true,
            flex: 1,
            enableDD: true,
            ddGroup: 'designerDDGroup',
            animate: false,
            rootVisible: false,
            title: 'Дерево компонентов',
            autoScroll: true,
            contextMenu: new Ext.menu.Menu({
                items: [{
                    text: 'Удалить',
                    iconCls: 'delete_item',
                    handler: onTreeNodeDeleteClick
                }]
            }),
            listeners: {
                contextmenu: function (node, e) {
                    node.select();
                    var c = node.getOwnerTree().contextMenu;
                    c.contextNode = node;
                    c.showAt(e.getXY());
                }
            },
            keys : [{
                key : Ext.EventObject.DELETE,
                    fn : onTreeNodeDeleteClick,
                    scope : this
            }]
        });

        var toolbox = new Ext.tree.TreePanel({
            root: new Ext.tree.TreeNode({
                text: 'foo',
                id: 'root'
            }),
            flex: 1,
            useArrows: true,
            ddGroup: 'designerDDGroup',
            enableDD: true,
            animate: false,
            autoScroll: true,
            rootVisible: false,
            title: 'Инструменты'
        });

        var application = new M3Designer.controller.AppController({
            tree: componentTree,
            designPanel: designPanel,
            toolbox: toolbox
        });

        this.application = application;

        var storage = new M3Designer.ServerStorage({
            id: 0,
            loadUrl: this.dataUrl,
            saveUrl: this.saveUrl,
            pathFile: this.path,
            className: this.className,
            funcName: this.funcName,
            previewUrl: this.previewUrl,
            uploadCodeUrl: this.uploadCodeUrl,
            maskEl: Ext.getBody()
        });
        this.storage = storage;

        var eastWrapper = new Ext.Panel({
            region: 'east',
            width: 250,
            split: true,
            layout: 'vbox',
            layoutConfig: {
                align: 'stretch'
            },
            items: [componentTree, toolbox]
        });

        this.add([designPanel, eastWrapper]);
        this.addButton({
            text: 'Сохранить',
            iconCls: 'icon-disk',
            handler: function () {
                storage.saveModel(application.getTransferObject());
            }
        });
        this.addButton({
            text: 'Просмотр кода',
            iconCls: 'icon-page-white-put',
            handler: function () {
                storage.previewCode(application.getTransferObject());
            }
        });

        storage.on('load', this.onSuccessLoad.createDelegate(this));

        storage.on('save', function (jsonObj) {
            if (jsonObj.success) {
                application.changedState(false);
                this.onChange();
                M3Designer.Utils.successMessage();
            } else {
                M3Designer.Utils.failureMessage({ "message": 'Ошибка при сохранении файла\n'+jsonObj.json });
            }

        },this);

        storage.on('preview', function (jsonObj) {
            if (jsonObj.success) {
                var previewWindow = new M3Designer.code.PyCodeWindow();
                previewWindow.on('loadcode', storage.uploadCode.createDelegate(storage));
                previewWindow.show(jsonObj.json);
            } else {
                M3Designer.Utils.failureMessage({ "message": jsonObj.json });
            }
        }, this);

        storage.on('loadcode', this.uploadCode.createDelegate(this));

        /**
         * Хендлер на удаление узла из дерева компанентов
         */
        function onTreeNodeDeleteClick(item) {
            var selectedNode = componentTree.getSelectionModel().selNode;
            var childNodesMessage = selectedNode.hasChildNodes() ? '</br>'+selectedNode.text+' Имеет дочерние узлы, они так же будут удалены.' : '';
            Ext.Msg.confirm('Удаление', 'Вы действительно хотите удалить '+selectedNode.text+'?'+ childNodesMessage,
                function(btn, text){
                    if (btn == 'yes'){
                        var accordion = Ext.getCmp('accordion-view');
                        if (accordion) accordion.fireEvent('clear');
                        application.onComponentTreeNodeDeleteClick(selectedNode);
                    }
                }
            )
        }
    },
    onSave: function () {
        this.storage.saveModel(this.application.getTransferObject());
    },
    loadModel: function () {
        this.storage.loadModel();
    },
    onSuccessLoad: function (jsonObj) {
        if (jsonObj.success) {
            if (this.fireEvent('beforeload', jsonObj)) {
                this.application.init(jsonObj.json);
            }
        } else {
            M3Designer.Utils.failureMessage({ "message": jsonObj.json });
        }
    },
    uploadCode: function (jsonObj) {
        if (jsonObj.success) {
            this.application.reloadModel(jsonObj.data)
        } else {
            M3Designer.Utils.failureMessage({ "message": jsonObj.json });
        }
    },
    onChange: function () {
        var newTitle = '*' + this.orginalTitle;
        if ((this.title !== newTitle) && this.application.changedState()) {
            this.orginalTitle = this.title;
            this.setTitle('*' + this.orginalTitle);
        } else if (!this.application.changedState()) {
            window.onbeforeunload = undefined;
            this.setTitle(this.orginalTitle || this.title);
        }
    }
});