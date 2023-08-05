/**
 * Crafted by ZIgi
 */

Ext.ns('M3Designer.ide');

/**
 * @class M3Designer.ide.Controller
 * Класс управляющий виджектами интерфейса и обрабатывающий действия пользователя.
 * Вся логика действий в проекте делегируется объекту класса CommandDispatcher(см command.js) Здесь находится
 * только взаимодействие с интерфейсом(создание и обработчики)
 */
M3Designer.ide.Controller = Ext.extend(Object, {

    /**
     * {M3Designer.ide.CommandDispatcher} объект обрабатывающий действия ide
     */
    dispatcher : undefined,

    /**
     * @constructor
     * @cfg {Ext.tree.TreePanel} explorerTree Дерево со структурой проекта
     * @cfg {Ext.Panel} propertyPanel Панелька со свойствами быстого редактирования - используется
     * в дизайнере UI
     * @cfg {Ext.TabPanel} tabPanel Панель с вкладками
     */
    constructor : function(cfg) {
        M3Designer.ide.Controller.superclass.constructor.call(this);
        Ext.apply(this, cfg);
        this.init();
    },

    init : function() {
        this.explorerTree.on('dblclick', this.explorerDblClickHandler, this);
        this.explorerTree.on('contextmenu', this.explorerContextMenuHandler, this);

        this.dispatcher = new M3Designer.ide.CommandDispatcher({
            controller:this
        });

        //Перехват ctrl+S для сохранения данных
        Ext.fly(document).on('keydown', this.documentKeyDownHandler, this);

        this.tabPanel.on('tabchange', this.tabChangeHandler, this);
    },

    /**
     * Двойной щелчок по вершине структуры проекта
     */
    explorerDblClickHandler:function(node,e) {
        var command = this.dispatcher.getDblClickCommand(node);
        if (command) {
            command.run(node, this);
        }
    },

    /**
     * Контекстное меню на вершине структуры
     */
    explorerContextMenuHandler : function(node, e) {
        var menu;

        node.select();
        menu = this.dispatcher.getContextMenu(node);
        if (menu) {
            menu.contextNode = node;
            menu.showAt(e.getXY());
        }
    },

    /**
     * Попытка активировать таб с переданным id
     * @return {Ext.Panel} Объект таба или undefined
     */
    tryActivateTab : function(tabId) {
        var tab = this.tabPanel.getItem(tabId);
        if(tab){
            this.tabPanel.setActiveTab(tab);
            return tab;
        }
        else {
            return undefined;
        }
    },

    /**
     * Создает вкладку с редактором кода и добавляет ее в табпанель
     */
    openCodeEditor:function(fileName, filePath, nodeId, fileContent, readOnly) {
        var type = M3Designer.ide.FileHelpers.getFileType(fileName);
        var isReadOnly = readOnly === undefined ? false : readOnly;

        var codeEditor = new M3Designer.code.ExtendedCodeEditor({
            id: filePath,
            treeNodeId: nodeId, // нода в дереве "струкрура проекта"
            silent: true, // Признак обработки ивентов
            sourceCode: fileContent,
            parser: type,
            readOnly: isReadOnly
        });

        codeEditor.setTitle(fileName);
        this.tabPanel.add( codeEditor );
        this.tabPanel.activate(codeEditor);
        codeEditor.silent = false;

        this.initCodeEditorHandlers(codeEditor, filePath);
    },

    /**
     * Создать вкладку с дизайнером UI и возвращает объект вкладки
     * @return {M3Designer.ide.DesignerWorkspace}
     */
    createUIDesignerWorkspace : function(id, nodeId, path, className, func) {
        return new M3Designer.ide.DesignerWorkspace({
            id: id,
            treeNodeId: nodeId,
            silent: true,
            dataUrl: M3Designer.UrlMap.get('data'),
            saveUrl: M3Designer.UrlMap.get('save'),
            path:path,
            className:className,
            funcName:func,
            previewUrl: M3Designer.UrlMap.get('preview'),
            uploadCodeUrl: M3Designer.UrlMap.get('upload-code')
        });
    },

    /**
     * Добавляет панекль дизайнера UI к табам
     * @param {M3Designer.ide.DesignerWorkspace} workspace
     * @param {String} tabTitle
     */
    appendWorkspace : function (workspace, tabTitle) {
        workspace.setTitle(tabTitle);
        this.tabPanel.add(workspace);

        //очень важная строчка, нужно таб активируется чтобы
        //дизайнер отрендерился в дом, если этого не сделать
        //получим ошибку при попытке доступа к элементам дома
        //при инициализации дизайнера
        this.tabPanel.activate(workspace);

        workspace.application.on('contentchanged', function() {
            this.onChange();
        }, workspace);


        workspace.on('beforeclose',
            _(this.initTabCloseHandler).bind(this, workspace,
                _(function(){return workspace.application.changedState}).bind(workspace)));

        workspace.on('close', function(tab){
            if (tab) {
               this.tabPanel.remove(tab);
               window.onbeforeunload = undefined;
            }
        }, this);

        this.tabPanel.on('tabchange', function(panel, newTab) {
            workspace.application.removeHighlight();
            //Грязный хак
            var accordion = Ext.getCmp('accordion-view');
            if (accordion) accordion.fireEvent('clear');
        });
    },

    /**
     * Функция слушает событие изменение контента елемента.
     * @param element
     * @param changed
     */
    initWorkSpaceCloseHandler : function(element, changed){
        //Хендлер на событие перед закрытием
        element.on({
            // Хендлер на событие перед закрытием
            'contentchanged':{
                fn: function(){
                    // Дефолтное значение или аргумент
                    var changedBool = changed === undefined ? element.contentChanged : changed;
                    if (changedBool === undefined){
                        changedBool = true;
                    }
                    if (changedBool){
                        window.onbeforeunload = function(){
                            return 'Вы закрываете вкладку, в которой имеются изменения.'
                        }
                    }else{
                        //Очищаем хендлер срабатывающий перед закрытием вкладки окна браузера
                        window.onbeforeunload = undefined;
                    }
                }
            },
            // Хендлер на событие перед закрытием
            'beforeclose':{
                fn : _(this.initTabCloseHandler).bind(this,element)
            }
        });
    },

    /**
     * Добавляет обработчики на таб
     */
    initTabCloseHandler : function(element, changed){
        var changedBool = element.contentChanged != undefined ? element.contentChanged : changed;
        var userTakeChoice = true;
        if (changedBool){
            var scope = element;
            M3Designer.Utils.showMessage(function(buttonId){
                if (buttonId==='yes') {
                    scope.onSave();
                    scope.fireEvent('close', scope);
                }
                else if (buttonId==='no') {
                    scope.fireEvent('close', scope);
                }
                else if (buttonId==='cancel') {
                    userTakeChoice = !userTakeChoice;
                }
                userTakeChoice = !userTakeChoice;
            });
        }else {
            userTakeChoice = !userTakeChoice;
        }
        return !userTakeChoice;
    },

    /**
     * Добавляет обработчики к табу с редактором кода
     */
    initCodeEditorHandlers : function(codeEditor, path){
        this.initWorkSpaceCloseHandler(codeEditor);

        /* Хендлер на событие закрытие таба таб панели */
        codeEditor.on('close', function(tab){
            if (tab) {
                window.onbeforeunload = undefined;
                //var tabPanel = Ext.getCmp('tab-panel');
                this.tabPanel.remove(tab);
            }
        }, this);
    
        /* Хендлер на событие сохранения */
        codeEditor.on('save', function(){
            /*Запрос на сохранение изменений */
            M3Designer.Requests.fileSaveContent(codeEditor, path);
        });

        /* Хендлер на событие обновление */
        codeEditor.on('update', function(){
            //Запрос на обновление
            M3Designer.Requests.fileUpdateContent(codeEditor, path);
        });

    },

    /**
     * Обработчик на переключение табов
     */
    tabChangeHandler : function (panel, tab) {
        if (tab.silent){
            return;
        }

        var projectView = Ext.getCmp('project-view');
        var rootNode =  this.explorerTree.getRootNode();
        var tab = rootNode.findChild('id', tab.treeNodeId, true);

        if (tab && !tab.isSelected() ){
            tab.parentNode.ensureVisible(function(){
                tab.parentNode.expand();
                tab.select();
            });
        }

    },

    /**
     * Обработчик нажатия клавиш с клавиатуры. Пока используется только
     * для обработки Ctrl+S(очевидно вызывается сохранение)
     */
    documentKeyDownHandler : function(e ,t, o) {
        if (e.ctrlKey && (e.keyCode == 83)) {// кнопка S
            var tab = this.tabPanel.getActiveTab();
            if (tab && tab.onSave && (typeof(tab.onSave) == 'function')) {
                tab.onSave();
                e.stopEvent();
            }
        }
    },

    /**
     * Поиск ноды в структуре проекта. Поиск найдет только первую попавщуюся вершину при
     * совпадении атрибутов
     * @param attr
     * @param value
     */
    findProjectNode : function(attr, value) {
        return this.explorerTree.getRootNode().findChildBy(function(node){
            if (node.attributes.hasOwnProperty(attr) && node.attributes[attr] === value ) {
                return true;
            }
        }, this, true);
    },

    /**
     * Выполняет комманду для переданной ноды
     * @param node {Ext.tree.TreeNode} нода
     * @param command {String} комманда
     */
    execCommand : function(node, command) {
        var command = this.dispatcher.getCommand(command);
        command.run(node);
    }
});