uiClass({
    name: 'ui.Iframe',
    type: 'iframe',
    base: ui.Element,
    data: {
        cls: 'ui-iframe',
        tag: 'iframe',
        frameborder: 0,

        render: function(){
            this.base();
            this.attr('frameborder', this.frameborder);

            if(this.url){
                this.load(this.url);
            }

            if(this.name){
                this.el.attr('name', this.name);
            }

            this.on('load', this.hideMask, this);
        },

        showMask: function(text, parent){
            this.base(text, parent || this.parent);
        },
        
        load: function(url){
            this.showMask();
            this.attr('src', url);
        },

        getWindow: function(){
            if(this.rendered){
                return this.el[0].contentWindow;
            }
        },

        getDoc: function(){
            if(this.rendered){
                return this.getWindow().document;
            }
        },

        getHead: function(){
            var doc = $(this.getDoc());

            return doc.find('head');
        },

        getBody: function(){
            var doc = $(this.getDoc());

            return doc.find('body');
        },

        addCssFile: function(url){
            this.getHead().append('<link href="'+url+'" rel="stylesheet" type="text/css" />');
        }
    }
});