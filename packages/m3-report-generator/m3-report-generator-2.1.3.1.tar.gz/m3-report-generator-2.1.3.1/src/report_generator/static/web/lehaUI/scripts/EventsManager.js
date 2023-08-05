uiClass({
    name: 'ui.core.EventsManager',
    base: ui.Base,
    data: {
        init: function () {
            this.base();
            this.initResize();

            var me = this;

            _.each(ui.global.jqueryEvents, function (name) {
                $(document).bind(name, function (e) { me.fire(name, e); });
            });
        },

        initResize: function () {
            var rtime = new Date(1, 1, 2000),
                timeout = false,
                delta = 200,
                fn = function () {
                    if (new Date() - rtime < delta) {
                        setTimeout(fn, delta);
                    } else {
                        timeout = false;
                        this.fire('resizeEnd');
                    }
                }.delegate(this);

            $(window).resize(function() {
                rtime = new Date();
                
                if (timeout === false) {
                    timeout = true;
                    setTimeout(fn, delta);
                }
            });
        },

        on: function (name, fn, scope) {
            var event = this.base(name, fn, scope);

            if(scope instanceof ui.Base){
                scope.on('destroy', function(){
                    this.un(name, event);
                }, this);
            }

            return event;
        }
    }
});
ui.EventsManager = new ui.core.EventsManager();

uiClass({
    name: 'ui.core.DragAndDropManager',
    base: ui.Base,
    data: {
        dragControl: null,
        dropControl: null,
        groups: {},

        add: function (element) {
            element.on('mousedown', function(e){
                ui.selectable(false);
                element.fire('dragStart',[e, element]);
                var moveFn = ui.EventsManager.on('mousemove', function(e){
                    element.fire('drag', [e, element]);
                });

                var upFn = ui.EventsManager.on('mouseup', function(e){
                    element.fire('drop', [e, element]);

                    ui.selectable(true);
                    ui.EventsManager.un('mousemove', moveFn);
                    ui.EventsManager.un('mouseup', upFn);
                });
            });
        },

        addDraggable: function(control, groups){
            var dragZone = control.getDragZone();

            if(isEmpty(groups)){
                groups = ['all'];
            } else if(isString(groups)){
                groups = [groups];
            }

            if(dragZone){
                var event = dragZone.on('mousedown', function(el, e){ this.onDragStart(control, groups, e); }, this);
            }
        },

        addDropZone: function(control, name){
            var dropZone = control.getDropZone();

            if(isEmpty(name)){
                name = 'all';
            }

            if(!this.groups[name]){
                this.groups[name] = [];
            }

            this.groups[name].push(control);

            control.on('destroy', function(){
                this.groups[name].remove(control);
            }, this);
            
            dropZone.on('mouseenter', function(){ this.dropControl = control; }, this);
            dropZone.on('mouseleave', function(){
                if(this.dropControl){
                    this.dropControl.removeClass('ui-hover');
                }
                this.dropControl = null;
            }, this);
        },

        onDragStart: function(control, groups, e){
            var controls = this.getControls(groups),
                dragEl = $('<div style="position:absolute;z-index:99999" />')
                    .append(control.createDragElement())
                    .css({ left: e.clientX + 5, top: e.clientY + 5 });

            this.dragControl = control;

            var moveFn = ui.EventsManager.on('mousemove', function(e){
                if(dragEl.parent().length == 0){
                    dragEl.appendTo('body');
                    _.each(controls, function(c){ c.addClass('ui-has-drop'); });

                    ui.selectable(false);
                }

                dragEl.css({ left: e.clientX + 5, top: e.clientY + 5 });

                if(this.dropControl){
                    this.dropControl.addClass('ui-hover');
                }
            }, this);

            var mouseUpFn = ui.EventsManager.on('mouseup', function(e){
                if(this.dropControl && controls.contains(this.dropControl) !== false){
                    this.dropControl.fire('drop', [control, e]);
                    control.fire('dragdrop', [this.dropControl,e]);

                    dragEl.remove();
                } else {
                    var offset = control.getDragZone().offset();
                    dragEl.animate({ left: offset.left, top: offset.top }, function(){ dragEl.remove(); });
                }

                ui.selectable(true);
                this.dragControl = null;

                _.each(controls, function(c){ c.removeClass('ui-has-drop'); });

                ui.EventsManager.un('mousemove', moveFn);
                ui.EventsManager.un('mouseup', mouseUpFn);
            }, this);
        },

        getControls: function(groups){
            var controls = [];

            _.each(groups, function(g){
                if(this.groups[g]){
                    controls = controls.concat(this.groups[g]);
                }
            }, this);

            return controls;
        }
    }
});
ui.DragAndDropManager = new ui.core.DragAndDropManager();

uiClass({
    name: 'ui.core.HashWatcher',
    base: ui.Base,
    data: {
        watchTime: 100,
        lastHash: false,

        init: function () {
            this.base();
            this.watch();
        },

        getHash: function () {
            var arr = window.location.hash.split("#"),
                hasValue = arr[1];

            if (isEmpty(hasValue)) {
                return false;
            }

            var hashLen = hasValue.indexOf("?");

            if (hashLen > 0) {
                hasValue = hasValue.substring(0, hashLen);
            }

            return hasValue;
        },

        setHash: function (hash) {
            try {
                window.location.hash = hash;
            } catch (e) {
                console.log(e);
            }
        },

        watch: function () {
            var currentHash = this.getHash();

            if (currentHash !== this.lastHash) {
                this.lastHash = currentHash;
                this.fire('change', currentHash);
            }

            this.watch.defer(this.watchTime, this);
        }
    }
});
ui.HashWatcher = new ui.core.HashWatcher();