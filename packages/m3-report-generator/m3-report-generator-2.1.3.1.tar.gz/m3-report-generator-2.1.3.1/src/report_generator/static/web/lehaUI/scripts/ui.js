var ui = {
    charset: 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
    hex: "0123456789ABCDEF",
    hasSvg: !!document.createElementNS && !!document.createElementNS('http://www.w3.org/2000/svg', 'svg').createSVGRect,
    guids:{},
    types: {},
    theme: {},
    emptyFn: function(){},
    key: {
        Enter: 13,
        Esc: 27
    },

    color: function(color, type){
        var rgb = ui.hexToRgb(color),
            hsb = ui.rgbToHsb(rgb.r, rgb.g, rgb.b);

        if(type=='invert'){
            rgb.r = 255 - rgb.r;
            rgb.g = 255 - rgb.g;
            rgb.b = 255 - rgb.b;
        } else if(type=='lighten') {
            hsb.s -= hsb.s / 100 * 30;
            rgb = ui.hsbToRgb(hsb.h, hsb.s, hsb.b);
        } else if(type=='darken') {
            hsb.b -= hsb.b / 100 * 30;
            rgb = ui.hsbToRgb(hsb.h, hsb.s, hsb.b);
        }

        return ui.rgbToHex(rgb.r, rgb.g, rgb.b);
    },

    hexToRgb: function(hex){
        var color = hex.slice(hex.length - 6, hex.length),
            giveHex = function(val){ return parseInt(val.toUpperCase(),16); };

        return {
            r: giveHex(color.slice(0,2)),
            g: giveHex(color.slice(2,4)),
            b: giveHex(color.slice(4,6))
        }
    },

    rgbToHex: function(r, g, b){
        var toHex = function(num){ return ui.hex.charAt((num >> 4)& 0xf)+ ui.hex.charAt(num & 0xf); }

        return '#' + toHex(r > 255 ? 255 : r) + toHex(g > 255 ? 255 : g) + toHex(b > 255 ? 255 : b);
    },

    hsbToRgb: function(h, s, b){
        var rgb = {};

        h = Math.round(h);
        s = Math.round(s*255/100);
        b = Math.round(b*255/100);

        if(s == 0) {
            rgb.r = rgb.g = rgb.b = b;
        } else {
            var t2 = (255-s)*b/255,
                t3 = (b-t2)*(h%60)/60;

            if(h==360) {
                h = 0;
            }

            if(h<60) {
                rgb = { r: b, g: t2 + t3, b: t2};
            } else if(h<120) {
                rgb.g=b;
                rgb.b=t2;
                rgb.r=b-t3;
            } else if(h<180) {
                rgb.g=b;
                rgb.r=t2;
                rgb.b=t2+t3;
            } else if(h<240) {
                rgb.b=b;
                rgb.r=t2;
                rgb.g=b-t3;
            } else if(h<300) {
                rgb.b=b;
                rgb.g=t2;
                rgb.r=t2+t3;
            }  else if(h<360) {
                rgb.r=b;
                rgb.g=t2;
                rgb.b=b-t3
            } else {
                rgb.r=0;
                rgb.g=0;
                rgb.b=0;
            }
        }
        return {
            r:Math.round(rgb.r),
            g:Math.round(rgb.g),
            b:Math.round(rgb.b)
        };
    },

    rgbToHsb: function(r, g, b){
        var hsb = {
            h: 0,
            s: 0,
            b: 0
        };

        var min = Math.min(r, g, b),
            max = Math.max(r, g, b),
            delta = max - min;

        hsb.b = max;
        hsb.s = max != 0 ? 255 * delta / max : 0;

        if (hsb.s != 0) {
            if (r == max) {
                hsb.h = (g - b) / delta;
            } else if (g == max) {
                hsb.h = 2 + (b - r) / delta;
            } else {
                hsb.h = 4 + (r - g) / delta;
            }
        } else {
            hsb.h = -1;
        }
        
        hsb.h *= 60;

        if (hsb.h < 0) {
            hsb.h += 360;
        }
        hsb.s *= 100/255;
        hsb.b *= 100/255;

        return hsb;
    },

    guid: function(){
        var guid = '',
            i = 0;

        for (i = 0; i < 10; i++) {
            guid += ui.charset.charAt(Math.random() * ui.charset.length);
        }

        if(ui.guids[guid]){
            return ui.guid();
        }

        ui.guids[guid] = 1;

        return guid;
    },

    svg2arr: function (value, scale) {
        var d = value;

        scale = scale || 1;

        d = d.replace(/,/gm, ' ')
            .replace(/([MmZzLlHhVvCcSsQqTtAa])([MmZzLlHhVvCcSsQqTtAa])/gm, '$1 $2')
            .replace(/([MmZzLlHhVvCcSsQqTtAa])([MmZzLlHhVvCcSsQqTtAa])/gm, '$1 $2')
            .replace(/([MmZzLlHhVvCcSsQqTtAa])([^\s])/gm, '$1 $2')
            .replace(/([^\s])([MmZzLlHhVvCcSsQqTtAa])/gm, '$1 $2')
            .replace(/([0-9])([+\-])/gm, '$1 $2')
            .replace(/(\.[0-9]*)(\.)/gm, '$1 $2')
            .replace(/([Aa](\s+[0-9]+){3})\s+([01])\s*([01])/gm, '$1 $3 $4 ');
        
        var parser = new(function (d) {
            this.tokens = d.split(' ');
        })(d);

        return _.map(parser.tokens, function (item) {
            var __ = parseFloat(item);
            
            if (isNaN(__)) {
                return item;
            } else {
                return __ * scale;
            }
        });
    },


    selectable: function(selectable, obj){
        var body = obj ? obj : $('body');

        if($.browser.msie){
            body.unbind('selectstart');

            if(selectable === false){
                body.bind('selectstart', function(){ return false; });
            }
        }
        else if($.browser.opera)
        {
            body.unbind('mousemove');
            
            if(selectable === false){
                body.bind('mousemove', function(e){ e.target.ownerDocument.defaultView.getSelection().removeAllRanges(); });
            }
        }
        else
        {
            if(selectable){
                body.removeClass('ui-unselectable');
            } else {
                body.addClass('ui-unselectable');
            }
        }
    },

    regType: function(name, type){
        this.types[name] = type;
    },

    getType: function(name){
        return this.types[name];
    },

    toJson: function(data){
        return $.toJSON(data);
    },

    toArray: function(obj){
        var arr = [];

        for(var i = 0; i < obj.length; i++){
            arr.push(obj[i]);
        }

        return arr;
    },
    
    tpl: function(tpl, methods){
        return new ui.Template(tpl, methods);
    },

    instance: function(item, defaults, baseType){
        baseType = baseType || ui.Base;
        
        if(item instanceof baseType){
            return item;
        }

        item = extend(extend({}, defaults), item);

        var type = ui.getType(item.type);

        if(isFunction(type)){
            return new type(item);
        }
    },

    ready: function(callback, scope){
        $(callback.delegate(scope));
    },

    getBody: function(){
        if(!ui.body){
            ui.body = ui.instance({
                type: 'element',
                el: 'body'
            });
        }

        return ui.body;
    },

    showMask: function(text){
        var body = ui.getBody();

        if(body){
            body.showMask(text);
        }
    },

    hideMask: function(){
        var body = ui.getBody();

        if(body){
            body.hideMask();
        }
    }
};

ui.common = {
    uiClass: function(cfg){
        var base = isString(cfg.base) ? ui.getType(cfg.base) : cfg.base,
            cls = $.inherit(base || cfg.data, base ? cfg.data : cfg.staticData, cfg.staticData);

        if(isString(cfg.name)){
            ui.common.namespace(cfg.name,cls);
        }

        if(isString(cfg.type)){
            ui.regType(cfg.type, cls);
        }

        return cls;
    },

    clone: function(obj){
        return $.extend(true, {}, obj);
    },

    extend: function(object, extendData, replace) {
        object = object || {};

        for(var k in extendData)
        {
            if(object[k] !== undefined ? replace !== false : true){
                object[k] = extendData[k];
            }
        }

        return object;
    },

    namespace: function(ns, data, scope){
        var names = ns.split('.'),
            obj = scope || window;

        _.each(names, function(name, index){
            if(isEmpty(obj[name])){
                obj[name] = {};
            }

            if(names.length - 1 == index && !isEmpty(data)){
                obj[name] = data;
            }

            obj = obj[name];
        });

        return obj;
    },

    isArray: function (obj) {
        return obj ? (obj instanceof Array || obj instanceof $) : false;
    },

    isArrayHasElements: function (obj) {
        return (this.isArray(obj) && obj.length > 0);
    },

    isString: function (obj) {
        return typeof (obj) == 'string';
    },

    isFunction: function (obj) {
        return typeof (obj) == 'function';
    },

    isNumber: function(obj){
        return typeof (obj) == 'number';
    },

    isControl: function(obj){
        return obj instanceof ui.Control;
    },

    isObject: function(obj){
        return obj instanceof Object;
    },

    isEmpty: function(obj, allowBlank){
        return obj === null || obj === undefined || (!allowBlank ? obj === '' : false);
    },

    delegate: function (fn, scope, args) {
        return fn.delegate(scope, args);
    },

    foreach: function(obj, fn, scope){
        if(isArray(obj)){
            _.each(obj, fn, scope || this);
        } else if(obj){
            for (var i in obj) {
                if (fn.call(scope || this, obj[i], i) === false) {
                    return;
                }
            }
        }
    }
};

ui.common.extend(window, ui.common);

extend(Array.prototype,{
    contains: function (obj) {
        var i = this.length;
        while (i--) {
            if (this[i] === obj) {
                return i;
            }
        }
        return false;
    },
    remove: function (obj) {
        var i = this.length;
        while (i--) {
            if (this[i] === obj) {
                this.splice(i, 1);
                return i;
            }
        }
    },
    min: function(){
        return Math.min.apply(Math, this);
    },
    max: function(){
        return Math.max.apply(Math, this);
    },
    sum: function(){
        var sum = 0;

        for (var i= 0, n= this.length; i<n; i++){
            var val = parseFloat(this[i]);
            if(!isNaN(val)){
                sum += val;
            }
        }

        return sum;
    },
    find: function(ns, value){
        var finded;

        _.each(this, function(item, i){
            var nsVal = ui.toJson(namespace(ns, null, this[i]));

            if(nsVal === ui.toJson(value)){
                finded = item;
                return false;
            }
        }, this);
        
        return finded;
    }
}, false);

extend(Function.prototype,{
    delegate: function(scope, args){
        var fn = this;

        args = isEmpty(args) ? ui.toArray(arguments) : args;

        return function () {
            if (isArray(args)) {
                return fn.apply(scope, args);
            } else {
                return fn.call(scope, args);
            }
        };
    },
    defer: function(time, scope, args){
        var fn = this.delegate(scope, args);

        setTimeout(fn, time);
    }
});

extend(String.prototype, {
    endsWith: function (suffix) {
        return this.indexOf(suffix, this.length - suffix.length) !== -1;
    },
    format: function(callback){
        return this.replace(/\{([^\{|\}]+)\}/g,function(arg,math){ return callback(math); });
    }
}, false);