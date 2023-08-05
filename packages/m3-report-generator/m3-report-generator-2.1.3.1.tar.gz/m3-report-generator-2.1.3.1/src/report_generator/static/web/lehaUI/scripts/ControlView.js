uiClass({
    name: 'ui.ControlView',
    type: 'view',
    base: ui.Base,
    data: {
        labelPositions: ['left','right','top','bottom'],
        defaultLabelPosition: 'right',
        disabled: false,
        readOnly: false,
        active: false,
        
        init: function(control){
            
            this.base({
                boxes: {},
                control: control,
                parent: control.el,
                cls: control.cls
            });

            _.each(this.viewConfig(), this.setBox, this);
            
            control.on('update', this.update, this);
            
            ui.EventsManager.on('resizeEnd', this.update, this);
        },

        viewConfig: function(){
            return [];
        },

        update: function(){
            this.fire('viewUpdate');
        },

        setActive: function(active){
            var cls = this.cls+'-active';

            if(active === true){
                this.parent.addClass(cls);
            } else {
                this.parent.removeClass(cls);
            }

            this.active = active;
        },

        setDisabled: function(disabled){
            var cls = this.cls+'-disabled';

            this.disabled = disabled;

            if(disabled === true){
                this.parent.addClass(cls);
            } else {
                this.parent.removeClass(cls);
            }
        },

        setReadOnly: function(readOnly){
            this.readOnly = readOnly;
        },

        setBox: function(value, key, p, name){
            if(isString(p)){
                name = p;
                p = this.getBox(p);
            }

            var boxName = isString(value) ? value : value.name,
                name = name ? name + '.' + boxName : boxName,
                cfg = {
                    parent: p || this.parent,
                    cls: this.cls ? this.cls + '-' + boxName : boxName
                };

            if(!isString(value)) {
                if(value.listeners){
                    value.listeners.scope = value.listeners.scope || this;
                }

                cfg = extend(cfg, value);
            }

            var box = new ui.Element(cfg);

            _.each(box.items, function(item, index){
                this.setBox(item, index, box.el, name);
            }, this);

            this.boxes[name] = box;
            this.fire('setBox['+name+']');

            return box;
        },

        getBox: function(value, autoCreate, parent){
            var boxName = isString(value) ? value : value.name,
                boxId = parent ? parent + '.' + boxName : boxName,
                box = this.boxes[boxId];

            if(!box && autoCreate === true){
                var p = parent ? this.getBox(parent) : null;
                box = this.setBox(value, null, p, parent);
            }

            return box;
        },

        removeBox: function(name){
            var box = isString(name) ? this.getBox(name) : name;

            if(box){
                box.destroy();
                delete this.boxes[name];
            }
        },
        
        setLabel: function(text, pos){
            if(text){
                this.setLabelPosition(pos);
                var box = this.getBox('label', true);
                box.setHtml(text);
            } else {
                this.removeBox('label');
                this.setLabelPosition(pos);
            }
        },

        setLabelPosition: function(pos){
            var p = this.labelPositions,
                pos = pos || this.defaultLabelPosition;

            _.each(p, function(i){
                this.parent.removeClass(this.cls+'-'+i);
            },this);

            this.parent.addClass(this.cls+'-'+pos);
        },

        getBody: function(){
            return this.parent;
        },

        getDragZone: function(){
            return this.getBody();
        },

        getDropZone: function(){
            return this.getBody();
        },

        createDragElement: function(){
            return this.type;
        }
    }
});