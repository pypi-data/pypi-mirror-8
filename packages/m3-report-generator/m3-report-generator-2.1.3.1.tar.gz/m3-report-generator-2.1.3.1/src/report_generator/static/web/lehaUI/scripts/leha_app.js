$(function(){
    var lockBtn = $('.lock-button .icon'),
        lockEl = $('.bottom-toolbar'),
        mainFrame = $('.main-frame'),
        locked = false;

    lockBtn.click(function(){
        if(locked){
            lockEl.unbind();
            lockBtn.removeClass('icon-unlocked');
        } else {
            var timer;

            lockEl.bind('mouseenter', function(){
                clearTimeout(timer);
                lockEl.stop().animate({height: 91}, 'fast');
            });
            lockEl.bind('mouseleave', function(){
                timer = setTimeout(function(){
                    lockEl.stop().animate({height: 10}, 'fast');
                }, 500);
            });
            lockBtn.addClass('icon-unlocked');
        }

        mainFrame.css({bottom: locked ? 90 : 14 });

        locked = !locked;
    });

    //Вытаскивает параметр из урла по его названию
    function getParameterByName(name){
        name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
        var regexS = "[\\?&]" + name + "=([^&#]*)";
        var regex = new RegExp(regexS);
        var results = regex.exec(window.location.href);
        if (results === null){
            return "";
        }
        else{
            return decodeURIComponent(results[1].replace(/\+/g, " "));
        }
    }

    var menu = ui.instance({
        type: 'bars.bind.MainMenu',
        parent: '#bottom-toolbar-menu',
        framesLayout: '#frames-layout',
        menuItems: [
            { Name: 'Запросы', Url: 'queries_constructor_ui',
                Hash: 'reports', Icon: 'static/images/processes_red.png' },
            { Name: 'Отчеты', Url: 'reports_constructor_ui',
                Hash: 'print_reports', Icon: 'static/images/processes_orange.png' }
        ]
    });
});