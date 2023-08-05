uiClass({
    name: 'ui.Element',
    type: 'element',
    base: ui.Base,
    data: {
        tag: 'div',
        cls: null,
        html: null,
        parent: null,
        style: null,
        width:null,
        minWidth:null,
        maxWidth:null,
        height:null,
        minHeight:null,
        maxHeight:null,
        fit: false,
        maskText: 'Загрузка...',

        init: function (cfg) {
            cfg = cfg || {};

            this.addJqueryMethods(cfg);
            this.base(cfg);
            
            if (cfg.el) {
                this.rendered = true;
                this.parent = $(cfg.el).parent();
            }
            
            this.el = $(cfg.el ? cfg.el : '<' + this.tag + '/>');

            if (this.autoRender !== false && this.parent) {
                this.doRender();
            }
        },

        showMask: function(text, parent){
            text = text || this.maskText;
            parent = parent || this.el;
            this.hideMask();

            this.mask = new ui.Element({
                cls: 'ui-modal',
                parent: parent,
                html: '<div class="ui-loading-msg">'+text+'</div>'
            });
        },

        hideMask: function(){
            if(this.mask && this.mask.rendered){
                this.mask.destroy();
            }
        },

        slideDown: function(speed){
            var isIE = $.browser.msie && $.browser.version == "7.0";

            if(isIE){
                this.show();
            } else {
                this.el.slideDown(speed);
            }
        },

        slideUp: function(speed){
            var isIE = $.browser.msie && $.browser.version == "7.0";

            if (isIE) {
                this.hide();
            } else {
                this.el.slideUp(speed);
            }
        },

        doRender: function(){
            this.setParent(this.parent);

            if(!this.rendered){
                this.fire('renderStart', this);
                this.render();
                this.rendered = true;
                this.setWidth(this.width);
                this.setHeight(this.height);
                this.fire('renderEnd', this);
            }
            
            if(this.checkParent()){
                this.el.appendTo(this.parent);
                this.globalFire('update');
            }
        },

        checkParent: function(){
            var p = this.el.parent().length > 0 ? this.el.parent()[0] : this.el.parent(),
                tp = this.parent && this.parent.length > 0 ? this.parent[0] : this.parent;

            return p !== tp;
        },

        render: function(){
            var me = this;

            if(this.domAttributes){
                _.each(this.domAttributes, function(val, key){
                    this.attr(key, val);
                }, this);
            }

            this.addClass(this.cls);
            this.initDragAndDrop();

            if(this.extraCls){
                this.addClass(this.extraCls)
            }

            if(!isEmpty(this.html)) { this.setHtml(this.html); }
            if(this.style){ this.css(this.style); }

            _.each(ui.global.jqueryEvents, function(name){
                this.el.bind(name, function(){
                    var args = [me].concat(ui.toArray(arguments));
                    me.fire(name, args);
                });
            },this);

            if(this.fit){
                this.addClass('ui-fit');
            }

            this.setTop(this.top);
            this.setBottom(this.bottom);
            this.setLeft(this.left);
            this.setRight(this.right);
        },

        initDragAndDrop: function(){
            
        },

        addJqueryMethods: function(cfg){
            var me = this;

            _.each(ui.global.jqueryMethods, function(method){
                var m = method;

                if(isString(method)){
                    m = {
                        name: method,
                        jName: method
                    };
                }

                cfg[m.name] = function(){
                    if(!me.el){ return; }
                    var result = me.el[m.jName].apply(me.el, arguments);
                    if(m.fire){ me.fire(m.name, me); }
                    return result;
                }
            }, this);
        },

        setParent: function (parent) {
            if(!parent) { return; }

            if(isString(parent)){
                parent = $(parent);
            } else if(isControl(parent)){
                parent = parent.getBody().el;
            } else if(parent instanceof ui.Element){
                parent = parent.el;
            }

            this.parent = parent;
        },

        setHtml: function(html){
            this.el.html(html);
        },

        getHtml: function(){
            return this.el.html();
        },

        getDom: function(){
            if(this.rendered){
                return this.el[0];
            }

            return null;
        },

        setWidth: function(w){
            if(!this.el){
                return;
            }
            
            if(!isString(w)){
                if(this.minWidth !== null && w < this.minWidth){
                    w = this.minWidth;
                }
                if(this.maxWidth !== null && w > this.maxWidth){
                    w = this.maxWidth;
                }
            }

            this.el.width(w);
        },

        setHeight: function(h){
            if(!this.el){
                return;
            }

            if(!isString(h)){
                if(this.minHeight !== null && h < this.minHeight){
                    h = this.minHeight;
                }
                if(this.maxHeight !== null && h > this.maxHeight){
                    h = this.maxHeight;
                }
            }

            this.el.height(h);
        },

        setTop: function(top){
            if(!isEmpty(top)){
                this.css({position:'absolute'});
                this.css({top:top});
            }
        },

        setBottom: function(bottom){
            if(!isEmpty(bottom)){
                this.css({position:'absolute'});
                this.css({bottom:bottom});
            }
        },

        setLeft: function(left){
            if(!isEmpty(left)){
                this.css({position:'absolute'});
                this.css({left:left});
            }
        },

        setRight: function(right){
            if(!isEmpty(right)){
                this.css({position:'absolute'});
                this.css({right:right});
            }
        },

        show: function(){
            this.doRender();
            this.el.show();
            this.fire('show');
        },

        hide: function(){
            this.el.hide();
            this.fire('hide');
        },

        toggle: function(){
            if(this.el.css('display') == 'none'){
                this.show();
            } else {
                this.hide();
            }
        },

        appendTo: function(el){
            this.setParent(el);
            this.doRender();
            this.fire('domUpdate', this);
        },

        destroy: function(){
            if(this.el){
                this.el.remove();
            }
            
            this.base();
        },

        setActive: function(active){
            var cls = this.cls+'-active';

            if(active === true){
                this.addClass(cls);
            } else {
                this.removeClass(cls);
            }

            this.active = active;
        }
    }
});