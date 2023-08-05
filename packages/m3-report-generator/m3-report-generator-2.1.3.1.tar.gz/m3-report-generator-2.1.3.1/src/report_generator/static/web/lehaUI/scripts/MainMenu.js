uiClass({
    name: 'bars.bind.MainMenu',
    type: 'bars.bind.MainMenu',
    base: ui.Control,
    data: {
        cls: 'bottom-toolbar-menu',
        framesLayout: 'body',
        menuItems: [],

        render: function () {
            this.base();

            this.framesLayoutEl = new ui.Element({
                parent: this.framesLayout,
                height: '100%',
                style: { position: 'absolute' }
            });

            _.each(this.menuItems, this.addMenuItem, this);
            this.update.defer(10, this);
        },

        update: function () {
            this.css({ marginLeft: -this.outerWidth() / 2 });

            this.framesLayoutEl.css({ width: this.menuItems.length * 100 + '%' });

            this.goToFrame(ui.HashWatcher.getHash() || this.menuItems[0].Hash, false);

            ui.HashWatcher.on('change', this.goToFrame, this);
        },

        addMenuItem: function (item, index) {
            var item = item || {};
            item.index = index;
            item.el = new ui.Element({
                index: index,
                item: item,
                html: '<span style="background-image: url(\'' + item.Icon + '\');">' + item.Name + '</span>',
                cls: 'item'
            });

            item.el.on('click', function () {
                ui.HashWatcher.setHash(item.Hash);
            });

            this.add(item.el);
        },

        createFrame: function (item) {
            var width = 100 / this.menuItems.length,
                left = item.index * width,
                div = $('<div class="frame-body"/>').appendTo(this.framesLayoutEl.el);

            div.css({
                left: left ? left + '%' : 0,
                width: width + '%'
            });

            return new ui.Iframe({
                url: item.Url,
                parent: div
            });
        },

        goToFrame: function (hash, animate, update) {
            var currentItem;

            _.each(this.menuItems, function (item) {
                if (item.Hash == hash) {
                    currentItem = item;
                    return false;
                }
            });

            if (currentItem) {
                _.each(this.controls, function (c) { c.setActive(false) });
                currentItem.el.setActive(true);

                var data = { left: '-' + currentItem.index * 100 + '%' };

                if (animate !== false) {
                    this.framesLayoutEl.stop().animate(data);
                } else {
                    this.framesLayoutEl.css(data);
                }

                if (update === true && currentItem.el.frame) {
                    currentItem.el.frame.destroy();
                    delete currentItem.el.frame;
                }

                if (!currentItem.el.frame) {
                    currentItem.el.frame = this.createFrame(currentItem);
                }
            }

            this.current = currentItem;
        }
    }
});