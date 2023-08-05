/**
 * Crafted by ZIgi
 */

Ext.ns('M3Designer.ide.commands');

/**
 *  В этом файле реализуются основная логика работы с иде. Принцип работы -
 * у каждой вершины в структуре проекта есть определенный тип 'file','ui-class' с которым
 * ассоциируются некоторое количество возможнный действий 'rename', 'ui-designer'. Настройка
 * типов вершин и действий находится в объекте M3Designer.ide.CommandsConfig
 *  Управляет действиями класс диспетчера, в его ответсвенности находится создание объектов команд,
 * передача им управления при соответсвующих действиях пользователя(контекстное меню, клики)
 *  Сама логика находится в классах команд. Они принадлежат неймспейсу M3Designer.commands и должны реализовывать
 *  следующий интерфейс:
 *  {
 *   text: 'Открыть файл', // текстовое название в контекстном меню
 *   iconCls: 'icon-script-lightning', //иконка в контекстном меню
 *   name : 'viewFile', //уникальный идентификатор в конфиге комманд
 *   run: function(item) { //функция обработчик, item - нода дерева
 *       this.controller; // в каждый инстанс пробрасывает объект контроллера ide, для организации обратного взаи-сия
 *  }
 * При добавлении новых команд достаточно реализовать класс, уд-щий этому интерфейсу(он должен быть в неймспейсе
 * commands) и декларативно настроить принадлежность команды к узлам структуры в соответсвующем конфиге
 */


/**
 * @class M3Designer.ide.CommandDispatcher
 * Диспетчер связывает узлы структуры проекта, делегирует действия объектам команд
 */
M3Designer.ide.CommandDispatcher = Ext.extend( Object, {

    /**
     * Инстансы команд
     */
    commandsBuffer : {},

    /**
     * Инстансы контекстных меню
     */
    menuBuffer : {},

    /**
     * @constructor
     * @cfg {M3Designer.ide.Controller} controller
     */
    constructor : function (cfg) {
        Ext.apply(this, cfg);
        M3Designer.ide.CommandDispatcher.superclass.constructor.call(this);
        this.initCommands();
        this.initMenu();
    },

    /**
     * Инстансы команд создаются автоматически - считается что все класс в неймспейсе commands
     * удоволетворяют интерфейсу
     */
    initCommands : function() {
        var i, c, commandsNS = M3Designer.ide.commands;

        for (i in commandsNS) {
            if ( commandsNS.hasOwnProperty(i) && typeof commandsNS[i] === 'function' ) {
                c = new commandsNS[i];
                c.controller = this.controller;
                this.commandsBuffer[c.name] = c;
            }
        }
    },

    /**
     * По типам узлов создаются контекстные меню
     */
    initMenu : function()  {
        var conf = M3Designer.ide.CommandsConfig;

        _(conf).each(function(v,k){
            if (v.hasOwnProperty('contextMenu')) {
                var menuItems = [];

                _(v['contextMenu']).each(function(el) {
                    menuItems.push( this.getMenuConfigObject(el))
                }, this);

                this.menuBuffer[k] = new Ext.menu.Menu({
                    items : menuItems
                });
            }
        }, this);
    },

    /**
     * Формирование конфига объект меню ExtJs
     */
    getMenuConfigObject : function(name) {
        var command;

        //в конфиге может бить или объект конфига или сепаратор
        if (name === '-') {
            return '-';
        }

        if (!this.commandsBuffer.hasOwnProperty(name)) {
            return;
        }

        command = this.commandsBuffer[name];
        // compose принимает список ф-ций и вызывает их поочереди,
        // передавая в качестве аргументов последующей
        // результат выполнения предыдущей.
        // в хэндлере меню айтема передается объект ui,
        // поэтому для обработки его методом run класса команды предварительно
        // извлекаем объекты ноды на которой было вызвано контекстное меню
        return {
            text: command.text,
            iconCls: command.iconCls,
            handler: _.compose(command.run,
                        function(menuItem) {
                            return menuItem.parentMenu.contextNode;
                        } ).bind(command)
        };
    },

    /**
     * Поиск команды отвечающей за двойной щелчок и переданного узла
     */
    getDblClickCommand : function(node) {
        var conf = M3Designer.ide.CommandsConfig,
            buf = this.commandsBuffer, command;

        if (!node.attributes.hasOwnProperty('type') || !conf.hasOwnProperty(node.attributes.type)
            || !conf[node.attributes.type].hasOwnProperty('dblClick')) {
            return;
        }

        command = conf[node.attributes.type].dblClick;

        if (!buf.hasOwnProperty(command)) {
            return;
        }

        return buf[command];
    },

    /**
     * Контекстное меню для переданного узла - каждому пункту соответсвует инстанс комманды
     */
    getContextMenu : function(node) {
        var type = node.attributes.type;

        if (this.menuBuffer.hasOwnProperty(type)) {
            return this.menuBuffer[type];
        }
    },

    /**
     * Возвращает инстанс комманды
     * @param command {String} алиас комманды
     */
    getCommand : function(command) {
        if (this.commandsBuffer.hasOwnProperty(command)) {
            return this.commandsBuffer[command];
        }
        else {
            throw new Error('Command' + command + ' is not defined');
        }
    }
});

/**
 * Настройка соответсвия
 */
M3Designer.ide.CommandsConfig = {
    'file': {
        'dblClick' : 'editFile',
        'contextMenu' : ['editFile','-', 'renameFile', 'deleteFile']
    },
    'projectRoot' : {
        'contextMenu' : ['createFolder', 'createFile']
    },
    'folder' : {
        'contextMenu' : ['createFolder', 'renameFolder', 'deleteFolder',
                        '-', 'createFile']
    },
    'ui-file' : {
        'dblClick' : 'editFile',
        'contextMenu': ['editFile','createUIClass','-','renameFile', 'deleteFile']
    },
    'ui-class' : {
        'dblClick' : 'ui-designer',
        'contextMenu' : ['ui-designer', 'createPanel']
    },
    'ui-function' : {
        'dblClick' : 'ui-designer'
    },
    'readonly-file' : {
        'dblClick' : 'viewFile'
    },
    'readonly-folder' : {
        
    },
    'readonly-ui-file' : {
        'dblClick' : 'viewFile'
    },
    'readonly-ui-class' : {
        //TODO запретить редактирование
        'dblClick' : 'ui-designer'
    },
    'readonly-ui-function' : {
        'dblClick' : 'ui-designer'
    }
};

/**
 * Команды
 */
M3Designer.ide.commands.EditFile = Ext.extend( Object, {
    //TODO сейчас работает по абсолютному пути к файлу -
    //нужно переделать на некий относительный
    text: 'Редактировать файл',
    iconCls: 'icon-script-lightning',
    name : 'editFile',

    run: function(item) {
        var fileObj = {
            'path': item.attributes.path,
            'fileName': item.attributes.text
        };

        if (this.controller.tryActivateTab(fileObj['path'])) {
            //файл уже открыт в какой-то из вкладок
            return;
        }

        M3Designer.Requests.getFile(fileObj,
            this.initCallbackClojure(fileObj['fileName'], fileObj['path'], item.id),
            this);
    },

    initCallbackClojure : function(filename, path, id) {
        //функциональное програмирование ради Высшего Блага
        return function(response) {
            var dataObj = Ext.util.JSON.decode(response.responseText);
            this.controller.openCodeEditor(filename, path, id, dataObj.data.content);
        }
    }
});

M3Designer.ide.commands.ViewFile = Ext.extend( M3Designer.ide.commands.EditFile , {
    text: 'Просмотр файла',
    iconCls: '',
    name: 'viewFile',

    initCallbackClojure: function(filename, path, id) {
        return function(response) {
            var dataObj = Ext.util.JSON.decode(response.responseText);
            this.controller.openCodeEditor(filename, path, id, dataObj.data.content, true);
        }
    }
});

M3Designer.ide.commands.BaseFileSystemCommand = Ext.extend( Object, {
    text: '',
    iconCls: '',
    name:'',
    promptTitle:'',
    promptText:'',
    actionParam:'',
    actionName:'',

    run: function(item) {
        Ext.MessageBox.prompt(this.promptTitle, this.promptText ,
            function(btn, name){
                if (btn == 'ok' && name){
                    var path = item.attributes['path'];
                    var params = {
                        path : path,
                        type: this.actionParam,
                        action : this.actionName,
                        name : name
                    };

                    M3Designer.Requests.manipulation(params, item, name, this.success, this);
                }
            },
            this
        );
    },

    success: function(item, propmt, obj) {
        //Переопределяется в дочерних классах
    }
});

M3Designer.ide.commands.DeleteFile = Ext.extend(M3Designer.ide.commands.BaseFileSystemCommand , {
    text: 'Удалить файл',
    iconCls: 'icon-script-delete',
    name : 'deleteFile',
    promptTitle:'Удалить файл',
    promptText:'Вы действительно хотите удалить файл',
    actionParam:'file',
    actionName:'delete',

    run: function(item) {
        var path = item.attributes['path'];
        var params = {
            path : path,
            type: this.actionParam,
            action : this.actionName
        };
        Ext.Msg.show({
            title: this.promptTitle,
            msg: this.promptText,
            buttons: Ext.Msg.YESNOCANCEL,
            icon: Ext.MessageBox.QUESTION,
            fn: function(btn, text){
                if (btn == 'yes'){
                    M3Designer.Requests.manipulation(params, item, null, function(item){
                        item.remove();
                    });
                }
            }
        });
    }
});

M3Designer.ide.commands.DeleteFolder = Ext.extend(M3Designer.ide.commands.DeleteFile , {
    text: 'Удалить директорию',
    name : 'deleteFolder',
    promptTitle:'Удалить директорию',
    promptText:'Вы действительно хотите удалить директорию',
    actionParam:'folder',
    actionName:'delete'
});


M3Designer.ide.commands.CreateFile = Ext.extend(M3Designer.ide.commands.BaseFileSystemCommand , {
    text: 'Создать файл',
    iconCls: 'icon-script-add',
    name : 'createFile',
    promptTitle:'Новый файл',
    promptText:'Введите имя файла',
    actionParam:'file',
    actionName:'new',

    success:function(item, prompt, obj) {
        var new_node = new Ext.tree.TreeNode({
            text: prompt,
            type:this.actionParam,
            path: obj.data['path'],
            iconCls: this.getIconCls(prompt),
            leaf: this.type === 'file'
        });
        var currentNode = item.type === 'file' ? item.parentNode: item;
        currentNode.appendChild(new_node, function(){
            currentNode.reload();
        });
    },

    getIconCls : function(fileName) {
        return M3Designer.ide.FileHelpers.getFileIcon(fileName);
    }
});

M3Designer.ide.commands.CreateFolder = Ext.extend(M3Designer.ide.commands.CreateFile , {
    text: 'Создать диркеторию',
    iconCls: 'icon-script-add',
    name : 'createFolder',
    promptTitle:'Новая директория',
    promptText:'Введите имя директории',
    actionParam:'folder',
    actionName:'new',

    getIconCls : function() {
        return 'icon-folder';
    }
});



M3Designer.ide.commands.RenameFile = Ext.extend( M3Designer.ide.commands.BaseFileSystemCommand, {
    text: 'Переименовать файл',
    iconCls: 'icon-script-edit',
    name:'renameFile',
    promptTitle:'Переименование файла',
    promptText:'Введите имя файла',
    actionParam:'file',
    actionName:'rename',

    success: function(item, prompt, obj) {
        item.setText(prompt);
    }
});

M3Designer.ide.commands.RenameFolder = Ext.extend( M3Designer.ide.commands.RenameFile , {
    text: 'Переименовать директорию',
    iconCls: 'icon-folder-edit',
    name: 'renameFolder',
    promptTitle: 'Переименование директории',
    promptText: 'Введите имя директории',
    actionParam: 'folder',
    actionName: 'rename'
});

M3Designer.ide.commands.UIDesigner = Ext.extend( Object, {
    text: 'Открыть дизайнер интерфейса',
    iconCls: 'icon-script-lightning',
    name : 'ui-designer',
    controller: undefined,
    run: function(item) {
        var workspace,
            path = item.attributes['path'],
            className = item.attributes['class_name'],
            funcTitle = item.attributes['func_name'] ?
            ' ('+ item.attributes['func_name'] + ')' :
            ' (initialize)',
            func = item.attributes['func_name'],
            id = path + className + funcTitle;

        if (this.controller.tryActivateTab(id)) {
            return;
        }

        workspace = this.controller.createUIDesignerWorkspace(id, item.id,
        path, className, func );

        workspace.on('beforeload', function(json) {
            if (json['not_autogenerated']) {
                this.askToGenerateFunction(item);
                return false;
            }
            else if (json.success) {
               this.controller.appendWorkspace(workspace, className + funcTitle);
               return true;
            }
            else {
                M3Designer.Utils.failureMessage({ "message": json.json });
                return false;
            }
        }, this);

        workspace.loadModel();
        
    },

    askToGenerateFunction : function(item) {
         Ext.Msg.show({
               title:'Функция не определена',
               msg: 'Функция автогенерация не определена в классе ' + item.attributes['class_name'] + '. ' +
                    '<br/> Сгенерировать данную функцию?',
               buttons: Ext.Msg.YESNO,
               icon: Ext.MessageBox.QUESTION,
               fn: function(btn, text){
                    if (btn == 'yes'){
                        M3Designer.Requests.generateInitialize(item);
                    }
               }
         });
    }
});

M3Designer.ide.commands.CreatePanelFunction = Ext.extend( Object , {
    text: 'Создать контейнерную функцию',
    iconCls: 'icon-medal-gold-add',
    name:'createPanel',
    run : function(item) {
        var win = new M3Designer.ide.commands.CreatePanelFunction.SelectTypeWindow({
            node: item});
        win.show();
    }
});

M3Designer.ide.commands.CreatePanelFunction.SelectTypeWindow = Ext.extend( Ext.Window, {
    resizable : false,
    modal : false,
    width : 400,
    initComponent : function() {
        var node = this.node; //
        this.title = 'Создание функции для класса - ' + node.text;
        this.form = this.createForm();
        this.items = [this.form];
        this.buttons = this.createButtons();
        
        M3Designer.ide.commands.CreatePanelFunction.SelectTypeWindow.superclass.initComponent.call(this);
    },

    createForm : function() {
        var store = new Ext.data.ArrayStore({
                    autoDestroy: true,
                    idIndex: 0,
                    fields: [
                        'type',
                        'descr'
                    ]
                    ,data: [
                        ['container', 'Container'],
                        ['panel', 'Panel'],
                        ['formPanel', 'Form panel']
                    ]
        });

        return new Ext.form.FormPanel({
            padding: 10,
            baseCls: 'x-plain',
            labelWidth: 100,
            items:[
                new Ext.form.TextField({
                    fieldLabel: 'Название',
                    id:'func-name',
                    anchor: '100%',
                    allowBlank: false,
                    maskRe: /[A-Za-z\_]+/,
                    name:'name'
                }),
                new Ext.form.ComboBox({
                    fieldLabel: 'Контейнерный класс',
                    anchor: '100%',
                    allowBlank: false,
                    mode:'local',
                    store: store,
                    valueField: 'type',
                    hiddenName: 'type',
                    displayField: 'descr',
                    editable: false,
                    triggerAction: 'all',
                    name:'type'
                })
            ]
        });
    },

    createButtons : function() {
        return [
            new Ext.Button({
                text: 'Создать',
                scope:this,
                handler: function(btn, e) {
                    var funcName = this.form.getForm().findField('func-name').getValue();
                    var funcType = this.form.getForm().findField('type').getValue();
                    M3Designer.Requests.createFunction(funcName, funcType, this.node, this);
                }
            }),
            new Ext.Button({
                text: 'Отмена',
                scope:this,
                handler: function(btn, e) {
                    btn.ownerCt.ownerCt.close();
                }
            })
        ]
    }
});

M3Designer.ide.commands.CreateUIClass = Ext.extend( Object , {
    text: 'Создать класс',
    iconCls: 'icon-cog-add',
    name:'createUIClass',
    run : function(item) {
        Ext.MessageBox.prompt('Создание класса', 'Введите название класса',
            function(btn, text){
                if (btn == 'ok'){
                    M3Designer.Requests.createClass(item, text);
                }
            }
        );
    }
});