//Application
reportGenerator.app = function(){
    var that = {};

    ////////////////////////////////////
    //Поля
    ////////////////////////////////////
    var UI = {};

    var _startApp = function() {
        UI = reportGenerator.UI();
    };

    that.startApp = function(){
        _startApp();
    };

    return that;
};