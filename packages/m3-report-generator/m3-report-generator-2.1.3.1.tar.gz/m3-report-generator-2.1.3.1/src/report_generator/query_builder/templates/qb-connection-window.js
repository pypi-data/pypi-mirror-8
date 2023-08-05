

var treeEntitiesFieldsFirst = Ext.getCmp('{{ component.tree_entities_fields_first.client_id }}');
var treeEntitiesFieldsSecond = Ext.getCmp('{{ component.tree_entities_fields_second.client_id }}');

/**
 * Подписка на событие добавления узлов
 */
win.on('fillNodes', function(childNodes){
	var rootNode;
	var massOfTreeFields = [treeEntitiesFieldsFirst, treeEntitiesFieldsSecond];
	for (var i = 0, len = massOfTreeFields.length; i < len; i++){

		rootNode = massOfTreeFields[i].getRootNode();		
		appendChildNode(rootNode, childNodes);
	}	
});

/**
 * Копирование узлов в узел
 * @param node: Куда будут копироваться узлы
 * @param childNodes: Список узлов, которые будут скопированы
 */
function appendChildNode(node, childNodes){
	var n, childNode, nChild;
	for (var i = 0, len = childNodes.length; i < len; i++){
		childNode = childNodes[i];
        n = new Ext.tree.TreeNode(childNode);
        
        node.getOwnerTree().getLoader().doPreload(n);  
        
        node.appendChild(n);            
	}
}

/**
 * 
 */
function selectLinks(){
	var firstNode = treeEntitiesFieldsFirst.getSelectionModel().getSelectedNode();
	var secondNode = treeEntitiesFieldsSecond.getSelectionModel().getSelectedNode();

	if (!firstNode ||  !secondNode){
		Ext.Msg.show({
	       title:'Выбор связи'
	       ,msg: 'Не все поля выбраны для связи'
	       ,buttons: Ext.Msg.OK
	       ,icon: Ext.MessageBox.WARNING
	    });
	    return;
	}
	
	var firstChkLink = Ext.getCmp('{{ component.chk_link_first.client_id }}');
	var secondChkLink = Ext.getCmp('{{ component.chk_link_second.client_id }}');
    function convertNodeId(node) {
        var List1;
        var nodeId = node.attributes['id_field'];
        if (node.attributes['entity_type'] == 2) {
            List1 = nodeId.split('.');
            nodeId = [List1[0], List1[1], List1[List1.length - 1]].join('.')
        }
        return nodeId;
    }
    var firstNodeId = convertNodeId(firstNode),
        secondNodeId = convertNodeId(secondNode);

	var resObj = {
		'outerFirst': firstChkLink.checked
		,'outerSecond': secondChkLink.checked
		,'relation': String.format('{0}-{1}|{2}-{3}',
			firstNode.attributes['entity_id'],
			firstNodeId,
			secondNode.attributes['entity_id'],
			secondNodeId
		)
		,'value': String.format('{0}.{1} = {2}.{3}',
			firstNode.parentNode.attributes['verbose_field'],
			firstNode.attributes['verbose_field'],
			secondNode.parentNode.attributes['verbose_field'],
			secondNode.attributes['verbose_field']
		)
        ,'leftEntityType': firstNode.attributes['entity_type']
        ,'rightEntityType': secondNode.attributes['entity_type']
    };

	win.fireEvent('selectLinks', resObj);
	win.close();
}
