reportGenerator.util = function(){
    var that = {};

    that.showBadMessage = function(){
        Ext.Msg.show({
            title:'Внимание',
            msg:'Не удалось соединиться с сервером!',
            buttons: Ext.Msg.OK,
            fn: Ext.emptyFn,
            animEl: 'elId',
            icon: Ext.MessageBox.WARNING
        });
    };

    //Если с сервера пришел OperationResult
    that.decodeResponse = function(response, successFunction){
        var o = Ext.decode(response.responseText);
        if (o.success) {
            successFunction();
        } else {
            Ext.Msg.show({
                title: 'Ошибка',
                msg: o.message,
                buttons: Ext.Msg.OK,
                fn: Ext.emptyFn(),
                animEl: 'elId',
                icon: Ext.MessageBox.ERROR
            });
        }
    };

    return that;
}();
