//UI object.
reportGenerator.UI = function(){

    var that = {},

        spec = reportGenerator.spec.getSpec(),
        buildReportUrl = spec.buildReport;

    //////////////////////////////////////////////////////////////////////////
    //Поля
    //////////////////////////////////////////////////////////////////////////

    //Кнопки
    var contentTabPanel = new Ext.TabPanel({
        id:'tpanel_content',
        xtype: 'tabpanel',
        activeTab: 0,
        items: [{
            title: 'Документация',
            html: '<iframe src="http://m3.bars-open.ru/report_generator/user.html" width="100%" height="100%" style="border: 0px none;"></iframe>',
            silent: true
        }]
        }),
            addButton = new Ext.Button({
                id: 'btn_add',
                text: 'Добавить',
                iconCls: 'icon-application-add'
            }),
            changeButton = new Ext.Button({
                id: 'btn_change',
                text: 'Изменить',
                iconCls: 'icon-application-edit'
            }),
            deleteButton = new Ext.Button({
                id: 'btn_delete',
                text: 'Удалить',
                iconCls: 'icon-application-delete'
            }),
            refreshButton = new Ext.Button({
                id: 'btn_refresh',
                text: 'Обновить',
                iconCls: 'icon-arrow-refresh'
            }),
            buildButton = new Ext.Button({
                id: 'btn_build',
                text: 'Построить отчет',
                iconCls: 'icon-building'
            });

    //Грид с элементами.
    var elementsStore = new Ext.data.JsonStore({
        autoLoad: true,
        autoDestroy: true,
        url: spec.elementsGridDataUrl,
        idProperty: 'id',
        root: 'rows',
        totalProperty: 'total',
        fields: ['name']
    });

    var toolBarBtns = [
            addButton,
            changeButton,
            deleteButton,
            refreshButton
        ],
        addWidth = 0;

    // Если это вкладка отчетов, то добавляем кнопку сформировать отчет
    // и увеличиваем ширину.
    if (buildReportUrl.length){
        toolBarBtns.push(buildButton);
        addWidth += 110;
    }

    var elementsGrid = new Ext.grid.GridPanel({
        id:'grid_elements',
        store: elementsStore,
        colModel: new Ext.grid.ColumnModel({
            defaults: {
                width: 300,
                sortable: true
            },
            columns: [
                {id: 'name', header: 'Название', width: 300+addWidth,
                    sortable: true, dataIndex: 'name'}
            ]
        }),
        items: [{
            xtype: 'toolbar',
            id: 'tlb_elements',
            items: toolBarBtns
        }]
    });

    elementsGrid.on('render', function(){
        var mask = new Ext.LoadMask(elementsGrid.body);

        elementsStore.on('beforeload', function(){
            mask.show();
        });

        elementsStore.on('load', function(){
            mask.hide();
        });

        elementsStore.on('exception', function(){
            mask.hide();
            reportGenerator.util.showBadMessage();
        });
    });
    ////////////////////////////////////
    //Приватные методы
    ////////////////////////////////////

    //Получить выбранный в гриде id
    var getSelectedId = function(grid){
        var selectionModel = grid.getSelectionModel();
        var selectedRow = selectionModel.getSelected();
        return selectedRow.id;
    };

    //Запрашивает получение панели редактирования\создания с сервера.
    var requestPanelFromServer = function(url, id){
        var mask = new Ext.LoadMask(contentTabPanel.body);
        mask.show();
        Ext.Ajax.request({
            url: url,
            params: {id: id},
            success: function(data){
                var panel = smart_eval(data.responseText);

                panel.closable = true;

                var panels = contentTabPanel.items.items;
                for (var i = 0, len=panels.length; i < len; i++){
                    if (panels[i].title === panel.title){
                        contentTabPanel.setActiveTab(panels[i]);
                        mask.hide();
                        return;
                    }
                }

                contentTabPanel.add(panel);
                contentTabPanel.setActiveTab(panel);
                mask.hide();
            },
            failure: function(){
                reportGenerator.util.showBadMessage();
                mask.hide();
            }
        });
    };

    //Удаляет элемент грида с сервера.
    var deleteFromServer = function(deleteUrl, id){
        Ext.Msg.show({
            title: 'Удаление записи',
            msg: 'Вы действительно хотите удалить выбранную запись?',
            icon: Ext.Msg.QUESTION,
            buttons: Ext.Msg.YESNO,
            fn:function(btn, text, opt){
                if (btn == 'yes') {
                    Ext.Ajax.request({
                        url: deleteUrl,
                        params: {id: id},
                        success: function(data){
                            reportGenerator.util.decodeResponse(data, function(){
                                elementsGrid.getStore().load();
                            });
                        },
                        failure: function(){
                            reportGenerator.util.showBadMessage();
                        }
                    });
                }
            }
        });
    };

    //Готовит события кнопок
    var prepareButtonEvents = function(){
        addButton.on('click', function(){
            requestPanelFromServer(spec.newRowUrl,'');
        });

        changeButton.on('click', function() {
            var id = getSelectedId(elementsGrid);
            requestPanelFromServer(spec.editRowUrl, id);
        });

        deleteButton.on('click', function(){
            var id = getSelectedId(elementsGrid);
            deleteFromServer(spec.deleteRowUrl, id);
        });

        refreshButton.on('click', function() {
            elementsGrid.getStore().load();
        });

        if (buildReportUrl.length){
            buildButton.on('click', function(){
                var id = getSelectedId(elementsGrid);
                Ext.Ajax.request({
                    url: spec.buildReport,
                    params: {'id': id},
                    success: function(response){
                        var buildWin = smart_eval(response.responseText);
                    }
                });
            });
        }
    };

    var prepareGridEvents = function(){
        elementsGrid.on('rowdblclick', function(that, rowIndex, e){
            var id = getSelectedId(elementsGrid);
            requestPanelFromServer(spec.editRowUrl, id);
        });
    };

    //Подготавливает viewPort нашего UI
    var makeViewPort = function(){
        new Ext.Viewport({
            layout: 'border',
            id: 'x-desktop',
            renderTo: Ext.getBody(),
            items: [{
                region: 'west',
                xtype: 'panel',
                split: true,
                id: 'panel_elements',
                width: 300 + addWidth,
                layout: 'fit',
                header: false,
                items:[elementsGrid]
            },{
                region: 'center',
                xtype: 'panel',
                layout: 'fit',
                header: false,
                id: 'panel_content',
                items: [contentTabPanel]
            }]
        });
    };

    ////////////////////////////////////
    //Публичные методы
    ////////////////////////////////////

    ////////////////////////////////////
    //Конструктор
    ////////////////////////////////////

    _constructor_ = function(){
        makeViewPort();
        prepareButtonEvents();
        prepareGridEvents();
    };

    _constructor_();

    return that;
};
