uiClass({
    name: 'ui.Base',
    type: 'base',
    data: {
        init: function(cfg){
            extend(this, cfg);

            this.initEvents();
        },

        initEvents: function(){
            this.events = {};
            
            foreach(this.listeners, function (event, name) {
                if(name === 'scope'){return;}
                if (isFunction(event)) {
                    this.on(name, event, this.listeners.scope || this);
                } else {
                    this.on(name, event.fn, event.scope || this.listeners.scope);
                }
            }, this);
        },

        on: function (name, fn, scope) {
            if(!this.events) { this.events = []; }
            if (!this.events[name]) { this.events[name] = []; }

            var eventData = { fn: fn, scope: scope || this, id: ui.guid() };

            this.events[name].push(eventData);

            return eventData;
        },

        un: function(name, event){
            var events = this.events;
            if(isString(name)){
                this.events[name].remove(event);
            } else {
                foreach(events, function(val, key){
                    foreach(events[key], function(data){
                        if(data.scope === name){
                            this.events[key].remove(data);
                        }
                    }, this);
                }, this);
            }
        },

        fire: function (name, args) {
            if(!this.events){
                return;
            }
            
            if (!this.events[name]) { return; }

            var result;

            foreach(this.events[name], function (event) {
                result = delegate(event.fn, event.scope, args)();
                return result;
            }, this);

            return result;
        },

        globalFire: function(name, args){
            this.fire(name, args);

            foreach(this.controls, function(c){
                c.globalFire(name, args);
            });
        },

        destroy: function(){
            this.fire('destroy', this);

            var me = this;

            foreach(this, function(v,k){
                delete this[k];
            }, this);
        }
    }
});