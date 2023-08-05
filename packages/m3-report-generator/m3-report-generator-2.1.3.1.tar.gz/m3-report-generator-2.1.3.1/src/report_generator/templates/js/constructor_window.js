
(function(){
    return new Ext.Window({
        title: 'Конструктор',
        maximizable: true,
        maximized: true,

        bodyCfg: {
            tag: 'iframe',
            src: '{{ component.src|safe }}',
            style: {
                border: '0px none'
            }
        }
    });
}());