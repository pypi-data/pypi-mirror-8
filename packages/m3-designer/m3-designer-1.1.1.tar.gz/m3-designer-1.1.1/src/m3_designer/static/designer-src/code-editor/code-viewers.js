/**
 * Crafted by ZIgi
 * В модуле находяться классы для отображения текстов исходных кодов.
 */

Ext.ns("M3Designer.code");

/**
 * @class M3Designer.code.PyCodeWindow
 * Окно предварительного просмтора кода питона, генерируемого дизайнером. Возникает по кнопке
 * предварительный просмотр кода
 */
M3Designer.code.PyCodeWindow = Ext.extend(Ext.Window, {
    title: 'Просмотр кода',
    width: 600,
    height: 500,
    layout: 'fit',
    maximizable: true,
    initComponent: function () {
        M3Designer.code.PyCodeWindow.superclass.initComponent.call(this);
        this.addEvents('loadcode');
    },
    show: function (code) {
        this.codeEditor = new Ext.m3.CodeEditor({
            sourceCode: code,
            autoScroll: true
        });

        this.add(this.codeEditor);
        this.addButton({
            text: 'Загрузить код в форму',
            iconCls: 'icon-page-white-get',
            handler: function () {
                this.fireEvent('loadcode', this.codeEditor.codeMirrorEditor.getValue());
            },
            scope: this
        });
        M3Designer.edit.PropertyWindow.superclass.show.call(this);
    }
});

/**
 * @class M3Designer.code.ExtendedCodeEditor
 * Редактор исходных кодов. Используется при двойном щелчке по файлу в дереве проекта
 */
M3Designer.code.ExtendedCodeEditor = Ext.extend(Ext.m3.CodeEditor, {
    autoScroll: true,
    border: true,
    buttonAlign: 'left',
    readOnly:false,
    initComponent: function () {
        this.theme = Ext.util.Cookies.get('m3editor-theme') || 'default';

        Ext.applyIf(this, {
            closable: true,
            buttons: [
                //Комбо бокс выбора темы оформления codeEditor'а
                {
                    xtype: 'combo',
                    fieldLabel: 'Theme',
                    hiddenName: 'theme',
                    mode : 'local',
                    store: new Ext.data.SimpleStore({
                        data: [
                            [1, 'default'],
                            [2, 'neat'],
                            [3, 'night'],
                            [4, 'elegant']
                        ],
                        id: 0,
                        fields: ['value', 'text']
                    }),
                    value: this.theme,
                    valueField: 'value',
                    displayField: 'text',
                    triggerAction: 'all',
                    editable: false,
                    listeners:{
                        'select':{
                                scope: this,
                                fn: function(combo, record, index){
                                    this.codeMirrorEditor.setOption("theme", record.data.text);
                                    this.theme = record.data.text;
                                    Ext.util.Cookies.set('m3editor-theme',record.data.text,
                                            new Date(9999,9,9,9,9,9,9) );
                                }
                        }
                    }
                },
                //Spacer отделяет комбо бокс от кнопок
                {
                    xtype: 'tbfill'
                },
                new Ext.Button({
                    text: 'Сохранить',
                    handler: this.onSave.createDelegate(this),
                    iconCls: 'icon-script-save',
                    hidden : this.readOnly
                }), new Ext.Button({
                    text: 'Обновить',
                    handler: this.onUpdate.createDelegate(this),
                    iconCls: 'icon-script-go',
                    hidden: this.readOnly
                }), new Ext.Button({
                    text: 'Закрыть',
                    handler: this.onClose.createDelegate(this),
                    iconCls: 'icon-cancel'
                })
            ]
        });
        //Хендлер на изменение кода
        this.on('contentchanged', function () {
            this.onChange();
        });
        //Хендлер на перехватывает keydown, если это ctrl+s то зажигается событие сохранить(save)
        this.on("editorkeyevent", function(i, e){
            if (e.ctrlKey && (e.keyCode == 83) && e.type == "keydown") {
                this.fireEvent('save');
                e.stop();
            }
        }, this);
        M3Designer.code.ExtendedCodeEditor.superclass.initComponent.call(this, arguments);
    },
    onClose: function () {
        //Вероятно можно будет оптимизировать, т.к. дублирует поведение beforeclose у tabpanel (выше)
        //Если есть именения в коде, выводим сообщения [ showMessage ]
        var textArea = this.getTextArea();
        if (this.contentChanged) {
            var scope = this;
            M3Designer.Utils.showMessage(function (buttonId) {
                if (buttonId === 'yes') {
                    scope.onSave();
                    scope.fireEvent('close', scope);
                } else if (buttonId === 'no') {
                    scope.fireEvent('close', scope);
                }
            });
        } else {
            this.fireEvent('close', this);
        }
    },
    onChange: function () {
        var newTitle = '*' + this.orginalTitle;
        if ((this.title !== newTitle) && this.contentChanged) {
            this.orginalTitle = this.title;
            this.setTitle('*' + this.orginalTitle);
        } else if (!this.contentChanged) {
            window.onbeforeunload = undefined;
            this.setTitle(this.orginalTitle || this.title);
        }
    },
    onSave: function () {
        this.fireEvent('save');
    },
    onUpdate: function () {
        this.fireEvent('update');
    },

    plugins:[new M3Designer.code.CodeAssistPlugin()]
});