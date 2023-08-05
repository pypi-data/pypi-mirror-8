uiClass({
    name: 'ui.Control',
    type: 'control',
    base: ui.Element,
    data: {
        viewType: ui.ControlView,
        cls: 'control',
        disabled: false,
        readOnly: false,

        init: function(cfg){
            cfg = cfg || {};

            extend(cfg, {
                controls: []
            });
            
            this.base(cfg);
        },

        render: function(){
            this.base();

            if(isString(this.editableDataRef) && isEmpty(this.value)){
                var owner = this.getEditableDataOwner(),
                    ref = this.editableDataRef;

                if(owner){
                    var updateRefValue = function(){
                        var names = ref.split('.'),
                            data = owner.editableData,
                            val = undefined;

                        if(!isEmpty(data)){
                            names.each(function(name, index){
                                if(isEmpty(data)){
                                    return false;
                                }

                                data = data[name];

                                if(names.length == index + 1){
                                    val = data;
                                }
                            });
                        }

                        var setValue = function(){
                            if(this.setValue){
                                this.setValue(val, true);
                            }

                            this.fire('updateEditableDataRef', [val, this]);
                        }.delegate(this);

                        if(this.rendered){
                            setValue.defer(20);
                        } else {
                            this.on('renderEnd', function(){
                                setValue.defer(20);
                            });
                        }
                    };

                    owner.on('syncEditableData', updateRefValue, this);
                    this.on('renderEnd', updateRefValue, this);
                }
            }

            this.renderView();

            if(isArrayHasElements(this.items)){
                this.items.each(function(item){
                    this.add(item);
                },this);
            }

            this.setDisabled(this.disabled);
            this.setReadOnly(this.readOnly);

            if(this.dropZone){
                ui.DragAndDropManager.addDropZone(this, this.dropZone);
            }

            if(this.dropZones){
                ui.DragAndDropManager.addDraggable(this, this.dropZones);
            }
        },

        syncEditableData: function(data, update){
            if(update !== true){
                this.editableData = data;
            } else {
                this.editableData = extend(this.editableData, data);
            }

            this.fire('syncEditableData', this.editableData);
        },

        removeAllControls: function(){
            var i = this.controls.length - 1;
            while(i >= 0){
                this.controls[i].destroy();
                i--;
            }
        },

        buildDropValue: function(control, e, dropValue){
            var parent,
                parentIndex,
                index = 0;

            if(dropValue.owner && dropValue.owner !== this){
                dropValue.owner.controls.remove(dropValue);
            }

            dropValue.owner = this;

            if(this.controls.contains(dropValue) === false){
                this.add(dropValue);
            }

            index = this.controls.contains(dropValue);

            if(e){
                this.controls.each(function(c, i){
                    if(c.el[0] === e.target || c.el.find(e.target).length > 0){
                        parent = c;
                        parentIndex = i;
                        return false;
                    }
                }, this);
            }

            if(parent && parent.el[0] !== dropValue.el[0]){
                parent.before(dropValue.el);

                if(this.controls[parentIndex] !== dropValue){
                    this.controls.remove(dropValue);

                    if(index < parentIndex){
                        parentIndex--;
                    }

                    this.controls.splice(parentIndex, 0, dropValue);
                }
            } else if(!parent) {
                this.getBody().append(dropValue.el);
                this.controls.remove(dropValue);
                this.controls.push(dropValue);
            }
        },

        onDrop: function(control, e){
            var value = control;

            if(!(control instanceof ui.DropValue) && this.controls.contains(control) === false){
                value = new ui.DropValue({
                    text: control.text,
                    dropZones: control.dropZones
                });

                this.add(value);

                value.getBody().setHtml(control.text);
            }

            this.buildDropValue(control, e, control);
        },

        renderView: function(){
            if(isString(this.viewType)){
                this.viewType = ui.getType(this.viewType);
            }
            
            this.view = new this.viewType(this);
        },

        createDragElement: function(){
            return this.view.createDragElement();
        },

        viewUpdate: function(){
            if(this.view instanceof ui.ControlView){
                this.view.update();
            }
        },

        getBody: function(){
            if(this.view){
                return this.view.getBody();
            }
        },

        getDragZone: function(){
            return this.view.getDragZone();
        },

        getDropZone: function(){
            return this.view.getDropZone();
        },

        setDisabled: function(disabled){
            this.view.setDisabled(disabled);
            this.disabled = disabled;
        },

        setReadOnly: function(readOnly){
            this.view.setReadOnly(readOnly);
            this.readOnly = readOnly;
        },

        setIcon: function(iconCls){
            this.iconCls = iconCls;
            this.view.setIcon(iconCls);
        },

        setLabel: function(text, pos){
            this.view.setLabel(text, pos);
        },

        setLabelPosition: function(pos){
            this.view.setLabelPosition(pos);
        },

        setHtml: function(html){
            var body = this.getBody();

            if(body instanceof ui.Element){
                body.setHtml(html);
            } else {
                body.html(html);
            }
        },

        show: function(){
            this.base();
            this.globalFire('update');
        },

        add: function(item, parent, autoRender){
            var control;

            parent = parent || this.getBody();

            if(isString(item)){
                if(item == 'clear'){
                    control = ui.instance({ type: item });
                } else if(item == '-'){
                    control = ui.instance({ type: 'seporater' });
                }
            } else {
                control = ui.instance(item, this.defaults, ui.Element);
            }

            if(control){
                control.owner = this;

                this.buildReference(item.ref, control);
                this.bindEditableData(control);
                this.controls.push(control);
                this.fire('addControl', control);

                control.on('destroy', function(){ this.controls.remove(control); }, this);

                if(autoRender !== false && control.autoRender !== false){
                    control.appendTo(parent);
                }
                else {
                    control.setParent(parent);
                }
            }
            
            return control;
        },

        renderToolbar: function(items, getBody, cls){
            if(isArrayHasElements(items)){
                var body = isFunction(getBody) ? getBody() : getBody,
                    tCfg = {
                        type: 'element',
                        cls: cls,
                        parent: body
                    },
                    tool = ui.instance({ style: { 'float':'left' } }, tCfg),
                    center = false;

                items.each(function(item){
                    if(item == '->'){
                        tool = ui.instance({ style: { 'float':'right' } }, tCfg);
                    } else if(item == '<->'){
                        tool.destroy();
                        tool = ui.instance({ style: { 'float':'left' } }, tCfg);
                        center = true;
                    } else {
                        item = isString(item) ? item : ui.instance(item, { type:'btn' });
                        this.add(item, tool);
                    }
                }, this);

                if(center){
                    var centerFn = function(){
                        tool.css({
                            width: tool.outerWidth(),
                            'float':'none',
                            marginLeft: 'auto',
                            marginRight: 'auto'
                        });
                    }.defer(50);
                }
            }
        },

        bindEditableData: function(control){
            if(control.editableDataRef){
                var owner = control.getEditableDataOwner();

                if(owner){
                    control.on('change', function(value, oldValue){
                        namespace(
                            control.editableDataRef,
                            value,
                            owner.editableData);

                        owner.fire('editableDataChange', [value, oldValue, control.editableDataRef]);
                    });
                }
            }
        },

        getEditableDataOwner: function(){
            var owner = this.owner;

            if(!owner || owner.editableData){
                return owner;
            }

            while(owner = owner.owner){
                if(owner.editableData){
                    return owner;
                }
            }
        },

        buildReference: function(ref, control){
            if(isEmpty(ref)){
                return;
            }

            var names = ref.split('./');

            if(names.length > 1){
                var owner = control,
                    i = 1;

                while(owner = owner.owner){
                    if(!owner){
                        return;
                    }

                    if(i == names.length){
                        owner[names[i-1]] = control;
                        return;
                    }

                    i++;
                }

            } else {
                this[ref] = control;
            }
        },

        hasDom: function(dom){
            if(this.getDom() === dom){
                return true;
            }

            var hasDom = false,
                els = ui.toArray(this.find('*'));

            els.each(function(el){
                if(el === dom){
                    hasDom = true;
                    return false;
                }
            });

            return hasDom;
        },

        remove: function(item){
            if(isControl(item)){
                this.controls.remove(item);
                item.destroy();
            }
        },

        destroy: function(){
            if(this.rendered){
                /*this.controls.each(function(control){
                    control.destroy();
                });*/

                this.view.destroy();
            }
            
            this.base();
        }
    }
});
