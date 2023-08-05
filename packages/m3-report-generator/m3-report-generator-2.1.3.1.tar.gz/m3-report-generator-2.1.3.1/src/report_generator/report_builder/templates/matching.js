/*Created by M3 IDE, at 19.10.2011 05:10*/

var treeQuery = Ext.getCmp('{{ component.tree_query.client_id }}'),
	treeSection = Ext.getCmp('{{ component.tree_section.client_id }}'),
	grdMatching = Ext.getCmp('{{ component.grd_matching.client_id }}');

/**
 * Класс, облегчающий работу для сопоставлений
 */
var matchingModel = new function(){

	// Имеющиеся запросы
	var _query = {};
	
	// Узел запроса
	var _queryNode = null;
	
	// Имеющиеся секции
	var _section = {};
	
	// Узел секции 
	var _sectionNode = null;
	
	return {
		/**
		 *  Добавление запросов и секций
		 */
		add: function(query, section) {

            _query = query;
			_section = section;

			// Добавление узла в дерево выбранных секций
			var rootNodeQuery = treeQuery.getRootNode();	
			var queryNode = new Ext.tree.TreeNode(query);
		   
		    rootNodeQuery.getOwnerTree().getLoader().doPreload(queryNode);                
		    if(queryNode){
		        rootNodeQuery.appendChild(queryNode);
		    }				    
			rootNodeQuery.loaded = true;
			
			_queryNode = queryNode;
			
			// Добавление узла в дерево выбранных секций
			var rootNodeSection = treeSection.getRootNode();	
			var sectionNode = new Ext.tree.TreeNode(section);
		   
		    rootNodeSection.getOwnerTree().getLoader().doPreload(sectionNode);                
		    if(sectionNode){
		        rootNodeSection.appendChild(sectionNode);
		    }				    
			sectionNode.loaded = true;	
			
			_sectionNode = sectionNode;
		},
		/**
		 * Возвращает узел дерева для запроса сопоставления
		 */
		geQueryNode: function(){
			return _queryNode;
		},
		/**
		 * Возвращает узел дерева для секции сопоставления
		 */
		getSectionNode: function(){
            return _sectionNode;
        },
        /**
         * Возвращает запрос
         */
		getQuery: function(){
			return _query;
		}
		/**
		 * Возвращает секцию
		 */
		,getSection: function(){
			return _section;
		}
	}
};

/**
 * Обработчик кнопки "Выбрать"
 */
function onSelect(){

	var children = [],
		range = grdMatching.getStore().getRange(),
		query = matchingModel.getQuery(),
		section = matchingModel.getSection();

	for (var i=0; i<range.length; i++){
		range[i].data['leaf'] = true;
		children.push(range[i].data);
	}

	if (!children.length){
		return;
	}

	win.fireEvent('selectData', {
		'name': query['name'],
		'query_id': query['query_id'],
		'template_field': section['template_field'],
		'children': children,
		'expanded': true
	});

    win.fireEvent('selectDataForSubstitution', {
       'name': query['name'],
       'query_id': query['query_id'],
       'template_field': section['template_field'],
       'children': children,
       'expanded': true
    });

	win.close();
}


win.on('loadData', matchingModel.add);

/**
 * Проставляет сопоставления на поля
 */
function onMatchingFields(){

	var selectedQueryItemNode = treeQuery.getSelectionModel().getSelectedNode(),
		selectedTemplateNode =  treeSection.getSelectionModel().getSelectedNode();
		
	// Можно выбрать только конечные узлы для сопоставления	
	if (selectedTemplateNode && !selectedTemplateNode.childNodes.length && selectedQueryItemNode
		&& !selectedQueryItemNode.childNodes.length) {

		var record = new Ext.data.Record();
		record.data['name'] = selectedQueryItemNode.attributes['name'];
		record.data['query_id'] = selectedQueryItemNode.attributes['query_id'];
		record.data['template_field'] = selectedTemplateNode.attributes['template_field'];

		grdMatching.getStore().add(record);
		
		selectedTemplateNode.remove();
		selectedQueryItemNode.remove();
	}
}

/**
 * Отменяет сопоставление
 */
function unMatchingFields(){

    var record = grdMatching.getSelectionModel().getSelected();

    if (record){

        // Для запросов восстанавливаем узел
        var queryNode = matchingModel.geQueryNode();
        queryNode.appendChild( new Ext.tree.TreeNode({
            'name': record.get('name'),
            'query_id': record.get('query_id'),
            'iconCls': 'icon-table-link'
        }) );
        queryNode.expand();
        
        
        // Для секций восстанавливаем узел
        var sectionNode = matchingModel.getSectionNode();
        sectionNode.appendChild( new Ext.tree.TreeNode({
            'template_field': record.get('template_field'),
            'iconCls':'icon-brick-link'
        }) ); 
        sectionNode.expand();
    
        grdMatching.getStore().remove(record);
    }
}