/**
 * Crafted by ZIgi
 */
Ext.namespace('M3Designer.ui');

/**
 * @constructor
 * Эта реализация паттерна посетитель, которая позволяет используя мощь JS'а
 * организовать полиморфное поведение при обходе древовидной структуры.
 * Кроме того здесь используется JS паттерн module от Дугласа Крокфорда -
 * фактически M3Designer.ui.ModelUIPresentaitionBuilder уже готовый объект в глобальном пространстве имен
 * после прохода интерпретатора
 */
M3Designer.ui.ModelUIPresentaitionBuilder = (function () {
    //Важное замечание номер раз - каждому экстовому компоненту присваевается id = id модели
    //это требуется для того чтобы ставить в соответсвие DOM элементы и экстовые компоненты
    //Важное замечание номер два - у контейнеров следует навешивать cls 'designContainer'
    //он нужен для визуального dd на форму при лукапе по DOM'у
    //Третье важное замечание - у всего что можно подсвечивать вешается класс designComponent
    var mapObject = {
        button: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'button',
                handler:undefined
            });
        },
        label: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'label'
            });
        },
        window: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'panel'
            });
        },
        panel: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'panel'
            });
        },
        container: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'container'
            });
        },
        fieldSet: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'fieldset'
            });
        },
        listView: function (model, cfg) {
            var columns = this.findGridColumns(model);
            var store = this.findStore(model, columns);

            return Ext.apply(cfg, {
                store: store,
                columns: columns,
                xtype: 'listview'
            });
        },
        formPanel: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'form'
            });

        },
        textField: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'textfield',
                readonly: true
            });
        },
        htmlEditor: function (model, cfg) {
            return Ext.apply(cfg, {
                readOnly: true,
                xtype: 'htmleditor'
            });
        },
        textArea: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'textarea',
                readonly: 'true'
            });
        },
        checkBox: function (model, cfg) {
            return Ext.apply(cfg, {
                readOnly: true,
                xtype: 'checkbox'
            });
        },
        numberField: function (model, cfg) {
            return Ext.apply(cfg, {
                readOnly: true,
                xtype: 'numberfield'
            });
        },
        displayField: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'displayfield'
            });
        },
        dateField: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'datefield'
            });
        },
        timeField: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'timefield'
            });
        },
        comboBox: function (model, cfg) {
            var store, i;
            //попробуем найти стор
            for (i = 0; i < model.childNodes.length; i++) {
                if (model.childNodes[i].attributes.type === 'arrayStore') {
                    store = new Ext.data.ArrayStore(
                            Ext.apply({
                                fields: ['id', model.attributes.properties.displayField]
                            },
                            model.childNodes[i].attributes.properties)
                        );
                }
            }
            //или создадим пустой
            if (!store) {
                store = new Ext.data.Store({
                    autoDestroy: true
                });
            }
            return Ext.apply(cfg, {
                store: store,
                mode: 'local',
                xtype: 'combo'
            });
        },
        triggerField: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'trigger'
            });
        },
        dictSelect: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'designer-dict-select'
            });
        },
        multiSelect:function(model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'designer-dict-select'
            });
        },
        fileUploadField: function (model, cfg) {
            //если не задать никаких указаний ширины то поле расплывается
            if (!cfg.width && !cfg.anchor) {
                cfg.width = 150;
            }
            return Ext.apply(cfg, {
                xtype: 'fileuploadfield'
            });
        },
        imageUploadField: function (model, cfg) {
            if (!cfg.width && !cfg.anchor) {
                cfg.width = 150;
            }
            return Ext.apply(cfg, {
                xtype: 'imageuploadfield'
            });
        },
        addressField: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'designer-kladr-companent'
            });
        },
        tabPanel: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'tabpanel',
                deferredRender: false,
                activeTab: model.attributes.activeTabId ? model.attributes.activeTabId : model.attributes.properties.activeTab,
                listeners: {
                    tabchange: function (panel, tab) {
                        var modelId = M3Designer.Utils.parseModelId(panel.id);
                        var tabPanelModel = model.ownerTree.findModelById(modelId);
                        tabPanelModel.attributes.activeTabId = tab.id;
                    }
                }
            });
        },
        treeGrid: function (model, cfg) {
            var children = [];
            var columns = this.findGridColumns(model);

            var recursion = function (m) {
                    var kids = [];
                    var j;
                    for (j = 0; j < m.childNodes.length; j++) {
                        if (m.childNodes[j].attributes.type === 'treeNode') {
                            var nodeCfg = Ext.apply({}, m.childNodes[j].attributes.properties);
                            if (m.childNodes[j].attributes.properties.items) {
                                Ext.apply(nodeCfg, m.childNodes[j].attributes.properties.items);
                            }
                            kids.push(nodeCfg);

                            if (m.childNodes[j].childNodes && m.childNodes[j].childNodes.length > 0) {
                                nodeCfg.children = recursion(m.childNodes[j]);
                            } else {
                                nodeCfg.leaf = true;
                            }
                        }
                    }
                    return kids;
                };
            children = recursion(model);
            //debugger;
            return Ext.apply(cfg, {
                root: new Ext.tree.AsyncTreeNode({
                    text: model.attributes.properties.rootText,
                    children: children
                }),
                rootVisible: false,
                xtype: 'treegrid',
                columns: columns
            });

        },
        objectTree: function(model, cfg) {
            var tree_cfg = this.treeGrid(model, cfg);
            var advcfg = {
                tbar: {
                    xtype: 'toolbar',
                    items: [{
                        xtype: 'button',
                        text: 'Добавить',
                        iconCls: 'add_item'
                    }, {
                        xtype: 'button',
                        text: 'Изменить',
                        iconCls: 'edit_item'
                    }, {
                        xtype: 'button',
                        text: 'Удалить',
                        iconCls: 'delete_item'
                    }, {
                        xtype: 'button',
                        text: 'Обновить',
                        iconCls: 'refresh-icon-16'
                    }]
                },
                bbar: {
                    xtype: 'paging'
                }
            };
            if (!cfg.allowPaging)
                delete advcfg["bbar"];
            return Ext.apply(tree_cfg, advcfg);
        },
        gridPanel: function (model, cfg) {
            var columns = this.findGridColumns(model);
            var store = this.findStore(model, columns);

            return Ext.apply(cfg, {
                xtype: 'grid',
                cls: 'designContainer designComponent',
                store: store,
                colModel: new Ext.grid.ColumnModel({
                    columns: columns
                })
            });
        },
        objectGrid: function (model, cfg) {
            var columns = this.findGridColumns(model);
            var config = {
                xtype: 'grid',
                cls: 'designContainer designComponent',
                store: {
                    xtype: 'arraystore'
                },
                tbar: {
                    xtype: 'toolbar',
                    items: [{
                        xtype: 'button',
                        text: 'Добавить',
                        iconCls: 'add_item'
                    }, {
                        xtype: 'button',
                        text: 'Изменить',
                        iconCls: 'edit_item'
                    }, {
                        xtype: 'button',
                        text: 'Удалить',
                        iconCls: 'delete_item'
                    }, {
                        xtype: 'button',
                        text: 'Обновить',
                        iconCls: 'refresh-icon-16'
                    }]
                },
                bbar: {
                    xtype: 'paging'
                },

                colModel: new Ext.grid.ColumnModel({
                    columns: columns
                })
            }
            if (cfg.allowPaging == false) delete config["bbar"];
            return Ext.apply(cfg, config);

        },
        toolbar: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'toolbar'
            });
        },
        tbfill: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'tbfill'
            });
        },
        tbseparator: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'tbseparator'
            });
        },
        tbspacer: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'tbspacer'
            });
        },
        tbtext: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'tbtext'
            });
        },
        pagingToolbar: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'paging'
            });
        },
        codeEditor: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'uxCodeEditor'
            });
        },
        radio: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'radio'
            });
        },
        radiogroup: function (model, cfg) {
            return Ext.apply(cfg, {
                xtype: 'radiogroup',
                items: this.findRadio(model)
            });
        },

        //================ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ================
        findRadio: function(model){
            var items = [],
                i,
                item;

            for (i = 0; i < model.childNodes.length; i++) {
                item = model.childNodes[i];
                if (item.attributes.type === 'radio') {
                    items.push(Ext.apply({}, item.attributes.properties));
                }
            };

            if (items.length === 0){
                items.push({
                    id: 'fake',
                    xtype: 'radio',
                    label: '',
                    hidden: true
                });
            }
            return items;
        },

        findGridColumns: function (model) {
            var columns = [];
            var i;
            //поиск колонок
            for (i = 0; i < model.childNodes.length; i++) {
                if (model.childNodes[i].attributes.type === 'gridColumn') {
                    var newColumn = Ext.apply({}, model.childNodes[i].attributes.properties);
                    columns.push(newColumn);
                }
            }
            //если нет колонок, создадим фейк
            if (columns.length === 0) {
                columns.push({
                    id: 'fake',
                    header: 'Fake column',
                    dataIndex: 'fake',
                    menuDisabled: true
                });
            }
            return columns;
        },
        findStore: function(model, columns){
            // Ищем Store во вложенных компонентах. Если нет нашли, то возвращаем заглушку.
            var store, i;

            //попробуем найти стор
            for (i = 0; i < model.childNodes.length; i++) {
                if (model.childNodes[i].attributes.type === 'arrayStore') {
                    //Добавляем филды для array сторе для правильного рендеринга
                    var fieldsIndexes = ['id'];
                    for (var x = 0; x<columns.length; x++){
                        fieldsIndexes.push(columns[x].dataIndex);
                    };
                    store = new Ext.data.ArrayStore(
                        Ext.apply({
                                fields: fieldsIndexes
                                },
                                model.childNodes[i].attributes.properties
                        )
                    );
                }
            }
            //или создадим пустой
            if (!store) {
                store = new Ext.data.Store({
                    autoDestroy: true
                });
            }
            return store;
        }
    };

    return {
        /**
         * Возвращает конфиг подготовленый для создания экстового компонента что будет нарисован на экране
         */
        build: function (model) {
            var cfg = Ext.apply({}, model.attributes.properties);
            Ext.destroyMembers(cfg, 'disabled');
            cfg.id = M3Designer.Utils.parseDomId(model.id);
            if (M3Designer.Types.isTypeContainer(model.attributes.type)) {
                cfg.cls = 'designContainer designComponent';
                cfg.items = [];
            } else {
                cfg.cls = 'designComponent';
            }
            if (mapObject.hasOwnProperty(model.attributes.type)) {
                return mapObject[model.attributes.type](model, cfg);
            }
        }
    };
}());