function(){
    var SimpleTreeGridView = Ext.extend(Ext.ux.maximgb.tg.GridView, {
        // Ext.ux.maximgb.tg.GridView не реализует метод обновления строк
        // поэтому при изменении строки грида игнорируются все css классы
        refreshRow : function(record) {
            var store     = this.ds,
                colCount  = this.cm.getColumnCount(),
                columns   = this.getColumnData(),
                last      = colCount - 1,
                cls       = ['x-grid3-row'],
                rowParams = {
                    tstyle: String.format("width: {0};", this.getTotalWidth())
                },
                colBuffer = [],
                cellTpl   = this.templates.cell,
                rowIndex, row, column, meta, css, i;

            if (Ext.isNumber(record)) {
                rowIndex = record;
                record   = store.getAt(rowIndex);
            } else {
                rowIndex = store.indexOf(record);
            }

            //the record could not be found
            if (!record || rowIndex < 0) {
                return;
            }

            //builds each column in this row
            for (i = 0; i < colCount; i++) {
                column = columns[i];

                if (i == 0) {
                    css = 'x-grid3-cell-first';
                } else {
                    css = (i == last) ? 'x-grid3-cell-last ' : '';
                }

                meta = {
                    id      : column.id,
                    style   : column.style,
                    css     : css,
                    attr    : "",
                    cellAttr: ""
                };
                // Need to set this after, because we pass meta to the renderer
                meta.value = column.renderer.call(column.scope, record.data[column.name], meta, record, rowIndex, i, store);

                if (Ext.isEmpty(meta.value)) {
                    meta.value = ' ';
                }

                if (this.markDirty && record.dirty && typeof record.modified[column.name] != 'undefined') {
                    meta.css += ' x-grid3-dirty-cell';
                }
                // ----- Modification start
                if (column.id == this.grid.master_column_id) {
                    meta.treeui = this.renderCellTreeUI(record, store);
                    cellTpl = this.templates.mastercell;
                }
                else {
                    cellTpl = this.templates.cell;
                }
                // ----- End of modification
                colBuffer[i] = cellTpl.apply(meta);
            }

            row = this.getRow(rowIndex);
            row.className = '';

            if (this.grid.stripeRows && ((rowIndex + 1) % 2 === 0)) {
                cls.push('x-grid3-row-alt');
            }

            if (this.getRowClass) {
                rowParams.cols = colCount;
                cls.push(this.getRowClass(record, rowIndex, rowParams, store));
            }
            // ----- Modification start
            if (!store.isVisibleNode(record)) {
                rowParams.display_style = 'display: none;';
            }
            else {
                rowParams.display_style = '';
            }
            rowParams.level = store.getNodeDepth(record);
            // ----- End of modification
            this.fly(row).addClass(cls).setStyle(rowParams.tstyle);
            rowParams.cells = colBuffer.join("");
            row.innerHTML = this.templates.rowInner.apply(rowParams);

            this.fireEvent('rowupdated', this, rowIndex, record);
        }
    });

    var SimpleTreeGrid = Ext.extend(Ext.ux.maximgb.tg.GridPanel, {
        getView : function()
        {
            if (!this.view) {
                this.view = new SimpleTreeGridView(this.viewConfig);
            }
            return this.view;
        },
    })

    var record = Ext.data.Record.create(
        Ext.util.JSON.decode('{{ component.t_render_record|safe }}')
    );
    var data = Ext.util.JSON.decode('{{ component.t_render_data|safe }}');

    var store = new Ext.ux.maximgb.tg.AdjacencyListStore({
        autoLoad: true,
        reader: new Ext.data.JsonReader({id: '_id'}, record),
        proxy: new Ext.data.MemoryProxy(data)
    });

    var columns = Ext.util.JSON.decode("{{ component.t_render_columns|safe }}")
    var grid = new SimpleTreeGrid({
    {% include 'base-ext-ui.js'%},
        {% if component.top_bar %} tbar: {{ component.t_render_top_bar|safe }}, {% endif %}
        store: store,
        master_column_id: "{{ component.master_column_id|safe }}",
        columns: columns,
        viewConfig: {
            enableRowBody : true
        },
        title: "Array Grid",
        stripeRows: true,
        autoExpandColumn: "{{ component.master_column_id|safe }}",
    }, {
        selModel: new Ext.grid.RowSelectionModel(),
        menus: {}
    })
    return grid;
}()
