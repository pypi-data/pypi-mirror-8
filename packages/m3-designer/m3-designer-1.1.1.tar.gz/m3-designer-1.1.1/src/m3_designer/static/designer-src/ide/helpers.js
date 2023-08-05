/**
 * Crafted by ZIgi
 */

Ext.ns('M3Designer.ide');

/**
 * Функции для обработки информации о файлах
 */
M3Designer.ide.FileHelpers = Ext.apply({}, {

    extConfig: {
        'py': 'python',
        'conf' : 'python',
        'js': 'javascript',
        'css': 'css',
        'html': 'html',
        'sql': 'sql',
        'default': 'text'
    },

    iconConfig: {
        'py': 'icon-page-white-py',
        'js': 'icon-page-white-js',
        'css': 'icon-css',
        'html': 'html',
        'default': 'icon-page-white-text'
    },

    /**
     * Возвращает расширение файла
     * @param fileName {String}
     */
    getFileExt:  function(fileName) {
        var splited = fileName.split('.');
        return splited[splited.length-1];
    },

    /**
     * Тип содержимого файла по его расширению
     * @param fileName {String}
     */
    getFileType : function(fileName) {
        var ext = this.getFileExt(fileName);
        return this.extConfig[ext] ? this.extConfig[ext] : this.extConfig["default"];
    },

    /**
     * CSS класс иконки
     * @param fileName
     */
    getFileIcon : function(fileName) {
        var ext = this.getFileExt(fileName);
        return this.iconConfig[ext] ? this.iconConfig[ext] : this.iconConfig["default"];
    } 
    
});