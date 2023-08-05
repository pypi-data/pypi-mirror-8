
var hdnID = Ext.getCmp('{{ component.hdn_id.client_id }}'),
	edtQueryName = Ext.getCmp('{{ component.str_name.client_id }}'),

	treeEntities = Ext.getCmp('{{ component.tree_entities.client_id }}'),
	grdSelectedEntities = Ext.getCmp('{{ component.grd_selected_entities.client_id }}'),
	grdLinks = Ext.getCmp('{{ component.grd_links.client_id }}'),
    joinRemovalChk = Ext.getCmp('{{ component.chb_join_removal.client_id }}'),

	treeAllFields = Ext.getCmp('{{ component.tree_all_fields.client_id }}'),
	grdSelectedFields = Ext.getCmp('{{ component.grd_selected_fields.client_id }}'), 
	distinctChk = Ext.getCmp('{{ component.chk_distinct.client_id }}'),
	limitChk = Ext.getCmp('{{ component.chk_limit.client_id }}'),
	limitCount = Ext.getCmp('{{ component.nmbr_limit_count.client_id }}'),

	treeGroupsFields = Ext.getCmp('{{ component.tree_groups_fields.client_id }}'),
	grdGroupFields = Ext.getCmp('{{ component.grd_group_fields.client_id }}'),
	grdGroupAggrFields = Ext.getCmp('{{ component.grd_gruop_aggr_fields.client_id }}'),

	treeConditionsFields = Ext.getCmp('{{ component.tree_conditions_fields.client_id }}'),
	grdConditionsFields = Ext.getCmp('{{ component.grd_conditions.client_id }}'),

    modelType = parseInt('{{ component.params.model_type }}'),
    queryType = parseInt('{{ component.params.query_type }}'),
    valueParam = '{{ component.value_param }}',
    fieldParam = '{{ component.field_param }}';

    panel = component;

//grdConditionsFields.getView().refresh();

////////////////////////////////////////////////////////////////////////////////
/**
 * Класс модели для сущностей и сразу же создание экземпляра 
 */
var entityModel = new function(){


	var _entities = [],
	    trees = [treeAllFields, treeGroupsFields, treeConditionsFields];

	return {
		/*
		 * Добавляет сущность
		 */
		add: function(models, queries){

			var url = '{{ component.params.entity_items_url }}';
			assert(url, 'Url for child window is not define');

            //NOTE: Здесь вызвать LoadMask ну никак не получится.

			Ext.Ajax.request({
				url: url,
                params: {
					'models': Ext.encode(models),
                    'queries': Ext.encode(queries)
				},
                success: function(response, opt){
					var nodes = Ext.decode(response.responseText),
	                    node, rootNode;
														
					for (var i = 0, treeCount = trees.length; i < treeCount; i++){
						
						rootNode = trees[i].getRootNode();
						rootNode.loaded = true;

						for (var j = 0, nodesCount = nodes.length; j < nodesCount; j++) {

							node = new Ext.tree.TreeNode(nodes[j]);
						   
						    rootNode.getOwnerTree().getLoader().doPreload(node);                
						    if(node){
						        rootNode.appendChild(node);
						    }

					        if (i === 0){ // Заполняем ноды при заполнении одного дерева
                                _entities.push( nodes[j] );
					        }
						}					
					}										
				},
                failure: function(){
					//loadMask.hide();
	                uiAjaxFailMessage.apply(this, arguments);
				}
			});						
		},
		
		/*
		 * Удаляет сущность
		 */
		remove: function (entities){

			var removeInGrid = function(grid, entityField, entityName){
				var store = grid.getStore();
				var records = store.query(entityField, entityName).getRange();
				if (records){
					store.remove(records);	
				}
            };

			// Нужно удалить выбранный массив id сущностей из всех деревьев
			// Пробежаться по всем полям и удалить все поля, которые входят в удаляемую сущность
			var grids = [grdSelectedFields, grdGroupFields, grdGroupAggrFields, grdConditionsFields],
                rootNode,
                entitiesCount = entities.length,
                gridsCount = grids.length,
                treeNodesCount = trees.length, i, j, k;

			for (j = 0; j < entitiesCount; j++) {
				
				// Удаление всех имеющихся узлов 
				for (i=0; i<trees.length; i++){
					rootNode = trees[i].getRootNode();
					
					var node = rootNode.findChild('id', entities[j]);
					node.remove();					
				}
			
				// Удаление записей в гридах, кроме грида связей
				for (k=0; k<gridsCount; k++){
					removeInGrid(grids[k], 'id', entities[j]);	
				}
				
				removeInGrid(grdLinks, 'entityFirst', entities[j]);
				removeInGrid(grdLinks, 'entitySecond', entities[j]);
			}

            for (i = 0; i < entitiesCount; i++){
                for (j = 0; j < _entities.length; j++){
                    if (_entities[j]['id'] == entities[i]){
                        _entities.splice(j, 1);
                        break;
                    }
                }
            }
		},
		
		/*
		 * Возвращает имеющиеся сущности
		 */
		getEntities:function (){			
			return _entities;
		}
	}
}();


////////////////////////////////////////////////////////////////////////////////
// Общие функции
/*
 * Удаление поля в произвольном гриде
 */
function deleteField(grid){
	var sm =  grid.getSelectionModel();
	if (sm instanceof Ext.grid.RowSelectionModel){
		 grid.getStore().remove( sm.getSelections() );
	} else if (sm instanceof Ext.grid.CellSelectionModel) {
		var rec = sm.getSelectedCell();
		if (rec) {
			var currentRecord = grid.getStore().getAt(rec[0]);
			grid.getStore().remove(currentRecord);
		}
	}
}



/**
 * Добавление поля в произвольный грид c полями: 
 * 	dataIndex='fieldName' 
 * 	dataIndex='entityName'
 */
function addField(grid, node, isModel){

    function convertNodeId(node) {
        var List1;
        var nodeId = node.attributes['id_field'];
        List1 = nodeId.split('.');
        console.log(node);
        if (node.attributes['entity_type'] == 2) {
            nodeId = [List1[0], List1[1], node.attributes['verbose_field'] || List1[List1.length - 1]].join('.')
        } else {
//            nodeId = [List[0]]
        }
        return nodeId;
    }

    var record = Ext.data.Record.create([ // creates a subclass of Ext.data.Record
	    {name: 'fieldName', mapping: 'fieldName'},
	    {name: 'entityName', mapping: 'entityName'}
	]);

	var fieldName = node.attributes['verbose_field'];
    var fieldVerboseName = node.attributes['true_verbose_field'];
	var entityId = node.attributes['entity_id'];

	var fieldID = convertNodeId(node);

    var entityType = modelType;
    if (!isModel){
        entityType = queryType;
    }

	var newRecord = new record(
	    {'fieldName': fieldName,
         'fieldVerboseName': fieldVerboseName,
	     'entityId': entityId,
         'entityType': entityType},
	    fieldID
	);

    try{
	    grid.getStore().add(newRecord);
    }catch(e){
        Ext.Msg.show({
            title: 'Внимание. Невозможно добавить поле'
            ,msg: 'Поле с данным идентификатором уже выбранно.'
            ,buttons: Ext.Msg.OK
        })
    }
}

/**
 * D&d из дерева сущностей в произвольный грид. Общий обработчик.
 */
function onAfterRenderGrid(grid){
	var fieldsDropTargetEl = grid.getView().scroller.dom;
	var selectFieldsDropTarget = new Ext.dd.DropTarget(fieldsDropTargetEl, {
	    ddGroup    : 'TreeDD',
	    notifyDrop : function(ddSource, e, data){
            if (data.node.parentNode === ddSource.tree.getRootNode()){
                return false;
            }
            var isModel = true;
            if (data.node.attributes['entity_type'] === queryType){
                isModel = false;
            }
			addField(grid, data.node, isModel);
	    }
	});	
}

/**
 * Обработчик произвольной кнопки добавить
 */
function addFieldBtn(tree, grid){

	var node = tree.getSelectionModel().getSelectedNode(),
        isModel = true;

    // Проверка того, что мы добавляем в поля поле, а не сущность.
    if (node.parentNode === tree.getRootNode()){
        return;
    }

    if (node.attributes['entity_type'] === queryType){
        isModel = false;
    }

	if (node) {
		addField(grid, node, isModel);
	}
}

////////////////////////////////////////////////////////////////////////////////
// Вкладка - Таблица и связи

/*
 * Обновление сущностей
 */
function refreshEntities(){    
	var rootNode = treeEntities.getRootNode();
	treeEntities.getLoader().load(rootNode);
	rootNode.expand();
}

/*
 * Добавление сущности в проект
 */
function onAddEntity(){
    // Может быть выбрана как сущность, так и существующий запрос.
	var node = treeEntities.getSelectionModel().getSelectedNode();

    if (node.id === modelType || node.id === queryType){
        return;
    }

	if (node) {
		addEntity(node);
	}
}

/*
 * Хендлер на кнопку "Добавить сущность"
 */
function addEntity(node){
    var dateNow = Date.now();
    var selectedStore = grdSelectedEntities.getStore(),
		entityId = node.id + "__" + dateNow,
		entityName = node.attributes['title'],
        entityVerboseName = node.attributes['title_verbose'],
        alias = node.id + "__" + dateNow,
        // Флаг. Является ли добавляемая сущность моделью или запросом.
        isModel = true;

    if (node.parentNode.attributes['id'] === queryType){
        isModel = false;
    }
    
    var record = selectedStore.getById(entityId);        
    if (!record && entityId && entityName){

		// Заполняется грид на этой же вкладке - выбранные сущности
		var EntityRecord = Ext.data.Record.create([ // creates a subclass of Ext.data.Record
		    {name: 'title', mapping: 'title'},
            {name: 'title_verbose', mapping: 'title_verbose'}
		]);

        var entityType = modelType;
        if (!isModel){
            entityType = queryType;
        }

		var newEntityRecord = new EntityRecord(
		    {entityId: entityId, entityType: entityType, title: entityName,
             title_verbose: entityVerboseName},
		    entityId 
		);
        selectedStore.add(newEntityRecord);

        var models = [],
            queries = [];

        if (isModel){
            models.push(entityId);
        }else{
            queries.push(entityId);
        }
        entityModel.add(models, queries);
    }else{
        Ext.Msg.show({
            title: 'Внимание. Невозможно добавить сущность'
            ,msg: 'Сущность с данным идентификатором уже выбранна.'
            ,buttons: Ext.Msg.OK
        })
    }
}

/**
 * D&d из дерева сущностей в выбранные сущности
 */
grdSelectedEntities.on('afterrender', function(){
    var selectEntityDropTargetEl = grdSelectedEntities.getView().scroller.dom,
        selectEntityDropTarget = new Ext.dd.DropTarget(selectEntityDropTargetEl, {
        ddGroup: 'TreeDD',
        notifyDrop : function(ddSource, e, data){
            if (data.node.id === modelType || data.node.id === queryType){
                return false;
            }
            addEntity(data.node);
            return true;
        }
    });
});

/**
 * Удаление сущностей
 */
function deleteEntity(){
	var sel = grdSelectedEntities.getSelectionModel().getSelections(),
        grdSelectFieldsRange = grdSelectedFields.getStore().getRange(),
        grdGroupFieldsRange = grdGroupFields.getStore().getRange(),
        grdGroupAggrFieldsRange = grdGroupAggrFields.getStore().getRange(),
        grdConditionsFieldsRange = grdConditionsFields.getStore().getRange(),
        grdLinksRange = grdLinks.getStore().getRange(),

        // Флаг показывающий, используются ли поля сущности.
        found = (
            checkEntityInGrids(grdSelectFieldsRange) ||
            checkEntityInGrids(grdGroupFieldsRange) ||
            checkEntityInGrids(grdGroupAggrFieldsRange) ||
            checkEntityInGrids(grdConditionsFieldsRange)
        ),

        str, i, j,
        selCount = sel.length;

    for (i = 0; i < selCount; i++){
        for (j = 0; j < grdLinksRange.length; j++){
            str = grdLinksRange[j].id.split('|');
            if (str[0].split('-')[0] == sel[i].id){
                found = true;
                break;
            }
            if (str[1].split('-')[0] == sel[i].id){
                found = true;
                break;
            }
        }
    }

    if (!found){
	    var massEntities = [];
	    for (i=0; i<selCount; i++){
		    massEntities.push(sel[i].id); //.split('__')[0]
	    }
	    entityModel.remove(massEntities);
	    grdSelectedEntities.getStore().remove(sel);
    }
    else{
        Ext.Msg.show({
            title: 'Внимание. Невозможно удалить',
            msg: 'Возможно сущность связана с условиями или группировками',
            buttons: Ext.Msg.OK
        });
    }
}

/* Вспомогательная функция для deleteEntity 
   Проверяет наличие полей сущности в гриде.
   Если поле сущности в гриде возвращает true.
 */
function checkEntityInGrids(grd){
    var id_, id2_;
    var sel = grdSelectedEntities.getSelectionModel().getSelections();
    for (var i = 0, selLen = sel.length; i < selLen; i++)
        for (var j = 0, grdLen=grd.length; j < grdLen; j++){
            if (grd[j].data){
                id_ = grd[j].data.id_;
                id2_ = sel[i].data.id_;
            }
            id_ = id_ || grd[j].id;
            id2_ = id2_ || sel[i].id;
            if (id_.split('-')[0].lastIndexOf(id2_, 0) === 0){
                return true;
            }
        }
    return false;
}

/*Выбор связи*/
function selectConnection(){
    var loadMask = new Ext.LoadMask(panel.body);
    loadMask.show();
    
    Ext.Ajax.request({
        url: '{{ component.params.select_connections_url }}'
        ,params: panel.actionContextJson || {}
        ,success: function(response){
            loadMask.hide();
            var childWin = smart_eval(response.responseText);                        
            
            childWin.fireEvent('fillNodes', entityModel.getEntities() );
            
            // Подпись на нажатие "Выбор" и обработка результатов запроса
            childWin.on('selectLinks', function(resObj){
				var record = new Ext.data.Record();
				record.id = resObj['relation'];
				record.data['outerFirst'] = resObj['outerFirst'];
				record.data['outerSecond'] = resObj['outerSecond'];
				record.data['value'] = resObj['value'];
                record.data['leftEntityType'] = resObj['leftEntityType'];
                record.data['rightEntityType'] = resObj['rightEntityType'];

                grdLinks.getStore().add(record);
            });
        }
        ,failure: function(){
        	loadMask.hide();
            uiAjaxFailMessage.apply(this, arguments);
        }
    });
}

/*Удаление связи*/
function deleteConnection(){
	deleteField(grdLinks);
}

/*Связь выше*/
function connectionUp(){
    console.log('Up');
    var selModel = grdLinks.getSelectionModel(),
        selected = selModel.getSelected(),
        range = grdLinks.getStore().getRange(),
        i, rec, canMove = false;
    if (!selected) {
        Ext.Msg.show({
           title:'Не выбрано условие',
           msg: 'Пожалуйста, выберите связь',
           buttons: Ext.Msg.OK,
           icon: Ext.MessageBox.WARNING
        });
    }
    var index = range.indexOf(selected);
    if (index > 0) {
        var buf = grdLinks.getStore().getAt(index);
        grdLinks.getStore().removeAt(index);
        grdLinks.getStore().insert(index - 1, buf);
        canMove = true;
    }
    if (!canMove) {
        Ext.Msg.show({
           title:'Ошибка',
           msg: 'Невозможно переместить связь',
           buttons: Ext.Msg.OK,
           icon: Ext.MessageBox.WARNING
        });
    }
}

/*Связь ниже*/
function connectionDown(){
    console.log('Down');
    var selModel = grdLinks.getSelectionModel(),
        selected = selModel.getSelected(),
        range = grdLinks.getStore().getRange(),
        i, rec, canMove = false;
    if (!selected) {
        Ext.Msg.show({
           title:'Не выбрано условие',
           msg: 'Пожалуйста, выберите связь',
           buttons: Ext.Msg.OK,
           icon: Ext.MessageBox.WARNING
        });
    }
    var index = range.indexOf(selected);
    if (index >= 0 && index < range.length - 1) {
        var buf = grdLinks.getStore().getAt(index);
        grdLinks.getStore().removeAt(index);
        grdLinks.getStore().insert(index + 1, buf);
        canMove = true;
    }
    if (!canMove) {
        Ext.Msg.show({
           title:'Ошибка',
           msg: 'Невозможно переместить связь',
           buttons: Ext.Msg.OK,
           icon: Ext.MessageBox.WARNING
        });
    }
}

////////////////////////////////////////////////////////////////////////////////
// Вкладка - Поля


grdSelectedFields.on('afterrender', function(){
	onAfterRenderGrid(grdSelectedFields);
});

function addSelectField(){
	addFieldBtn(treeAllFields, grdSelectedFields);
}

function deleteSelectField(){
	deleteField(grdSelectedFields);
}

/**
 * Поднимает вверх выбранное поле
 */
function fieldUp(){	
	var rec = grdSelectedFields.getSelectionModel().getSelectedCell();
	if (rec && rec[0] > 0){
		var currentRecord = grdSelectedFields.getStore().getAt(rec[0]);
		
		grdSelectedFields.getStore().remove(currentRecord);		
		grdSelectedFields.getStore().insert(rec[0] - 1, currentRecord);
		
		grdSelectedFields.getSelectionModel().select(rec[0] - 1, rec[1]);
	}	
}

/**
 * Опускает вниз выбранное поле
 */
function fieldDown(){
	var rec = grdSelectedFields.getSelectionModel().getSelectedCell();

	if (rec && rec[0] < grdSelectedFields.getStore().getCount() - 1){
		var currentRecord = grdSelectedFields.getStore().getAt(rec[0]);		
		grdSelectedFields.getStore().remove(currentRecord);		
		grdSelectedFields.getStore().insert(rec[0] + 1, currentRecord);
		
		grdSelectedFields.getSelectionModel().select(rec[0] + 1, rec[1]);
	}
}

////////////////////////////////////////////////////////////////////////////////
// Вкладка - Группировка

grdGroupFields.on('afterrender', function(){
	onAfterRenderGrid(grdGroupFields);
});

grdGroupAggrFields.on('afterrender', function(){
	onAfterRenderGrid(grdGroupAggrFields);
});

function addGroupField(){
//	addFieldBtn(treeGroupsFields, grdGroupFields);
    var tree = treeGroupsFields, grid = grdGroupFields;
    var node = tree.getSelectionModel().getSelectedNode(),
        isModel = true;

    // Проверка того, что мы добавляем в поля поле, а не сущность.
    if (node.parentNode === tree.getRootNode()){
        return;
    }

    if (node.attributes['entity_type'] === queryType){
        isModel = false;
    }

	if (node) {
		addField(grid, node, isModel);
	}
}

function addGroupAggrField(){
	addFieldBtn(treeGroupsFields, grdGroupAggrFields);
}

function deleteGroupField(){	
	deleteField(grdGroupFields);	
}

function deleteGroupAggrField(){	
	deleteField(grdGroupAggrFields);	
}


////////////////////////////////////////////////////////////////////////////////
// Вкладка - Условия

grdConditionsFields.on('afterrender', function(){
//	var fieldsDropTargetEl = grdConditionsFields.getView().scroller.dom;
//    var selectFieldsDropTarget = new Ext.dd.DropTarget(fieldsDropTargetEl, {
//        ddGroup    : 'TreeDD',
//        notifyDrop : function(ddSource, e, data){
//
//            if (data.node.parentNode === ddSource.tree.getRootNode()){
//                return false;
//            }
//
//            var d = {};
//            d = Ext.apply(d, data.node.attributes);
//            d['entity_name'] = data.node.parentNode.attributes['verbose_field'];
//            openConditionWindow(d, false);
//        }
//    });
    grdConditionsFields.getView().refresh();
});

function moveUp(selected, from, to, store) {
    var i, buf = [], buf2 = [], endIndex = null, range = store.getRange();


    for (i = to; i < from; i++) {
        buf.push(range[i]);
    }
    for (i = range.length - 1; i >= 0; i--) {
        rec = range[i];
        if (isMyParent(selected.get('_id'), rec, range)) {
            endIndex = i;
            break;
        }
    }
    if (endIndex === null) {
        endIndex = from
    }
    store.removeAt(to);
    store.insert(to + endIndex - from + 1, buf);
}


function conditionUp(){

    var selModel = grdConditionsFields.getSelectionModel(),
        selected = selModel.getSelected(),
        range = grdConditionsFields.getStore().getRange(),
        i, rec, canMove = false;
    if (!selected) {
        Ext.Msg.show({
           title:'Не выбрано условие',
           msg: 'Пожалуйста, выберите условие',
           buttons: Ext.Msg.OK,
           icon: Ext.MessageBox.WARNING
        });
    }
    var _parent = selected.get('_parent') || null;
    var _id = selected.get('_id');
    //обход снизу
    for (i = range.length - 1; i >= 0; i--){
        rec = range[i];
        if (_parent == rec.get('_parent')) {
            if (_id == rec.get('_id')) {
                canMove = true;
                var from = i;
                continue;
            } else if (canMove) {
                var to = i;
                moveUp(selected, from, to, grdConditionsFields.getStore());
            }
        }
    }
    if (!canMove) {
        Ext.Msg.show({
           title:'Ошибка',
           msg: 'Невозможно переместить условие',
           buttons: Ext.Msg.OK,
           icon: Ext.MessageBox.WARNING
        });
    }
}

function moveDown(selected, from, to, store) {
    var i, buf = [], buf2 = [], endIndex = null, range = store.getRange();

    for (i = from; i < to; i++) {
        buf.push(range[i]);
    }
    var toRecord = range[to];
    for (i = range.length - 1; i >= 0; i--) {
        rec = range[i];
        if (isMyParent(toRecord.get('_id'), rec, range)) {
            endIndex = i;
            break;
        }
    }
//    if (endIndex === null) {
//        endIndex = from
//    }
    store.removeAt(from);
    store.insert(-to + endIndex + from + 1, buf);
}

function conditionDown(){
    var selModel = grdConditionsFields.getSelectionModel(),
        selected = selModel.getSelected(),
        range = grdConditionsFields.getStore().getRange(),
        i, rec, canMove = false;
    if (!selected) {
        Ext.Msg.show({
           title:'Не выбрано условие',
           msg: 'Пожалуйста, выберите условие',
           buttons: Ext.Msg.OK,
           icon: Ext.MessageBox.WARNING
        });
    }
    var _parent = selected.get('_parent') || null;
    var _id = selected.get('_id');
    // обход сверху
    for (i = 0; i <= range.length - 1; i++){
        rec = range[i];
        if (_parent == rec.get('_parent')) {
            if (_id == rec.get('_id')) {
                canMove = true;
                var from = i;
                continue;
            } else if (canMove) {
                var to = i;
                moveDown(selected, from, to, grdConditionsFields.getStore());
            }
        }
    }
    if (!canMove) {
        Ext.Msg.show({
           title:'Ошибка',
           msg: 'Невозможно переместить условие',
           buttons: Ext.Msg.OK,
           icon: Ext.MessageBox.WARNING
        });
    }
}


function getParentNode(_id, range){
    var j, rec_;
    for (j = range.length - 1; j >= 0; j--){
        rec_ = range[j];
        if (rec_.get('_id') == _id){
            return rec_;
        }
    }
    return null;
}

function isMyParent(parent_id, node, range){
    if (node == null) {
        return false;
    }
    var _parent = node.get('_parent');
    if (_parent == null){
        return false;
    }
    if (_parent == parent_id){
        return true;
    }
    return isMyParent(parent_id, getParentNode(node.get('_parent'), range), range);
}



/**
 * Открывает окно для добавления нового условия или редактирования существующего.
 * Флаг isEdit признак редактируемости записи.
 */
function openConditionWindow(rec, isEdit){
    function convertNodeId(rec) {
        var List1;
        var nodeId = rec['id_field'];
        if (rec['entity_type'] == 2) {
            List1 = nodeId.split('.');
            console.log(rec);
            nodeId = [List1[0], List1[1], rec['verbose_field'] || List1[List1.length - 1]].join('.')
        }
        return nodeId;
    }

    function findInsertIndex (record, parentNode) {

        var i, j, store = grdConditionsFields.getStore(),
            range = store.getRange(),
            rec;

        for (i = range.length - 1; i >= 0; i--) {
            rec = range[i];
            if (isMyParent(record.get('_parent'), rec, range)) {
                return i + 1;
            }
        }
        for (i = range.length - 1; i >= 0; i--) {
            rec = range[i];
            if (rec.get('_id') == record.get('_parent')) {
                return i + 1;
            }
        }
        return range.length - 1;
    }

    var loadMask = new Ext.LoadMask(panel.body);
    loadMask.show();
    
    Ext.Ajax.request({
        url: '{{ component.params.condition_url }}'
        ,params: panel.actionContextJson || {}
        ,success: function(response){
            loadMask.hide();
            var childWin = smart_eval(response.responseText);

            var verboseFieldName = rec['verbose_field'],
                trueVerboseFieldName = rec['true_verbose_field'],
                fieldID          =  convertNodeId(rec), //rec['id_field'],
                paramName        = rec['parameter'] || fieldID,
                condition,
                connector,
                paramType;

            if (isEdit){
                connector = rec['connector'];
                condition = rec['condition'];
                paramType = rec['param_type'];
            }

            // Генерируем событие загрузки данных в окно задания условий.
            childWin.fireEvent('loadData', {
            	'verboseName': verboseFieldName,
            	// id параметра, задается здесь, потом везде используется только для
            	// чтения
            	'paramName': paramName,
                'connector': connector,
                'condition': condition,
                'paramType': paramType,
                // Поля, которые могут использоваться в качестве параметров в условиях.
                'fields': getSelectedFields()
            });

            // Обработка события щелчка кнопки выбрать в окне задания условий
            childWin.on('selectData', function(obj){
                var param    = obj['parameter'] || obj['field_param'],
                    conditionID = obj['conditionID'],
                    recordID = String.format('{0}-{1}-{2}', fieldID, conditionID, param),
                    store    = grdConditionsFields.getStore(),
                    record,
                    paramType;

                if (isEdit){
//                    record  = store.getById(rec['id']);
                    record = grdConditionsFields.getSelectionModel().getSelected();
                }else{
                    record  = new Ext.data.Record();
                    record.data['verboseName'] = verboseFieldName;
                }
                if (obj['parameter']){
                    paramType = parseInt(obj['paramType']);

                }else{
                    paramType = parseInt(fieldParam);
                    record.data['second_field_entity_type'] = obj['entity_type'];
                }
                record.data['parameter'] = param;
                record.data['param_type'] = paramType;
			    record.data['condition'] = conditionID;
			    record.data['expression'] = String.format('{0} {1} ${2}',
										verboseFieldName, obj['condition'], param);
                record.data['connector'] = obj['connector'];
                record.data['id_field'] = fieldID;
                record.data['first_field_entity_type'] = rec['entity_type'];
                record.set('id_', recordID);
                var parentNode;
                if (!isEdit){
//                    var cell = grdConditionsFields.getSelectionModel().getSelectedCell();
//                    if (cell) {
//                        curNodeNum = cell[0];
//                        parentNode = grdConditionsFields.getStore().getRange()[curNodeNum];
//                    }
                    parentNode = grdConditionsFields.getSelectionModel().getSelected();
                    record.data['_is_leaf'] = true;
                    if (parentNode) {
                        record.data['_parent'] = parentNode.data['_id'];
                        record.data['_level'] = parentNode.data['_level'] + 1;
                        parentNode.data['_is_leaf'] = false;
                        parentNode.commit();
                    } else {
                        record.data['_level'] = 1; // root
                    }

                }
                if (isEdit){
                    record.commit();
                }else{
                    record.data['_id'] = Date.now();
                    record['id'] = record.data['_id'];
                    if (parentNode) {
//                        store.addToNode(parentNode, record)
                        record.set("_parent", parentNode.id);
//                        store.addSorted(record);
                        var index = findInsertIndex(record, parentNode);
                        store.insert(index, record);
                    } else {
                        store.add(record);
                    }
//                    store.sortData();
                }
                store.expandNode(record);
                grdConditionsFields.getView().refresh();


            });
		}
		,failure: function(){
        	loadMask.hide();
            uiAjaxFailMessage.apply(this, arguments);
        }
	});
}

// Получаем данные для загрузки в комбобокс выбора параметра-поля.
function getSelectedFields(){

    var entities = treeConditionsFields.getRootNode().childNodes,
        entitiesCount = entities.length,
        fieldsCount,
        fields = [],
        field = {},
        res = [],
        i, j;

    for (i = 0; i < entitiesCount; i++){

        fields = entities[i].childNodes;
        fieldsCount = fields.length;

        for (j = 0; j < fieldsCount; j++){
            field = fields[j].attributes;

            res.push({
                id: String.format('{0}', field['id_field']),
                field: String.format('{0}.{1}', field['entity_id'], field['verbose_field']),
                entity_type: field['entity_type']
            });
        }
    }

    return res;
}

function editCondition(){
    // Выбранная для редактирования запись в гриде
//    var numCell = grdConditionsFields.getSelectionModel().getSelectedCell();
//    if (!numCell) return;


    var editRow = grdConditionsFields.getSelectionModel().getSelected();

    if (!editRow){
        return;
    }

    var rec = {};
    rec['verbose_field'] = editRow.data['verboseName'];

    // editRow.data['parameter'] имеет вид entity_name-id_field
    // поэтому использую магические числа.
    rec['id_field']      = editRow.data['id_field'];
    rec['connector']     = editRow.data['connector'];
    rec['condition']     = editRow.data['condition'];
    rec['param_type']    = editRow.data['param_type'];
    rec['parameter']     = editRow.data['parameter'];
    rec['id']            = editRow.id;
    rec['entity_type']   = editRow.data['first_field_entity_type'];

    openConditionWindow(rec, true);
}

function deleteCondition(){

    var grid = grdConditionsFields, rec, view = grid.getView();
//    deleteField(grdConditionsFields);
    var sm =  grid.getSelectionModel();
	if (sm instanceof Ext.grid.RowSelectionModel){
        var selected = sm.getSelected();
        var _parent = selected.get('_parent');
		grid.getStore().remove(selected);
        var range = grid.getStore().getRange(), i, have_children = false;
        if (_parent) {
            for (i = range.length - 1; i >= 0; i--) {
                rec = range[i];
                if (rec.get("_parent") == _parent) {
                    have_children = true;
                }
                if (rec.get('_id') == _parent && !have_children) {
                    rec.data['_is_leaf'] = true;
                    rec.commit();
                    break;
                }
            }
        }
	} else if (sm instanceof Ext.grid.CellSelectionModel) {
		rec = sm.getSelectedCell();
		if (rec) {
			var currentRecord = grid.getStore().getAt(rec[0]);
			grid.getStore().remove(currentRecord);
		}
	}

//    var selModel = grdConditionsFields.getSelectionModel(),
//        params_id = [];
//    for (var i = 0; i < selModel.getSelections().length; i++){
//        params_id[i] = selModel.getSelections()[i].data['id'];
//    }
//    Ext.Ajax.request({
//        url: '{{ component.params.check_and_del_params_url }}'
//        ,params: {'params_id': Ext.encode(params_id),
//                  'query_id': hdnID.getValue(),
//                  'operation': 'check'}
//        ,success: function(response){
//            var resp = Ext.decode(response.responseText);
//            if (resp['reports'].length != 0){
//                var messageObject = {
//                    title: 'Внимание',
//                    buttons: Ext.Msg.YESNO,
//                    icon: Ext.MessageBox.INFO,
//                    fn: function(btn){
//                        if (btn == 'yes'){
//                            Ext.Ajax.request({
//                                url: '{{ component.params.check_and_del_params_url }}'
//
//                                ,params: { 'params_id': Ext.encode(params_id),
//                                           'operation': 'delete',
//                                           'query_id': hdnID.getValue() }
//
//                                ,success: function(response){
//                                    deleteField(grdConditionsFields);
//                                }
//                            });
//                        }
//                    }
//                };
//                var messages = [];
//                messages.push('Параметры будут удалены из следующих отчетов');
//                for (var i = 0; i < resp['reports'].length; i++){
//                    messages.push(resp['reports'][i]);
//                }
//                messages.push('Согласны продолжить?');
//                Ext.Msg.show( Ext.apply(messageObject, {msg: messages.join('<br/>')}) );
//            }
//            else{
//                deleteField(grdConditionsFields);
//            }
//        }
//        ,failure: function(){
//            loadMask.hide();
//            uiAjaxFailMessage.apply(this, arguments);
//        }
//    });
}

/**
 * Обработчик произвольной кнопки добавить
 */

function addCondition(){

	var node = treeConditionsFields.getSelectionModel().getSelectedNode(),
        data = {};

    if (node.parentNode === treeConditionsFields.getRootNode()){
        return;
    }

	if (node) {
        data = Ext.apply(data, node.attributes);
        data['entity_name'] = node.parentNode.attributes['verbose_field'];
        openConditionWindow(data, false);
	}
}

function checkAtLeastOneSelect(){

}

// Валидация при сохранении
function queryValidation(){
    // Проверка на наличие SELECT полей и связей.
    var checkSubQRel = checkSubQueriesRelations();
    var noRelationsEntities = checkSubQRel[0],
        haveAtLeastOneSelect = checkSubQRel[1],
        // Флаг
        normal = true;

    if (noRelationsEntities.length){
        var messageObject = {
            title: 'Внимание',
            buttons: Ext.Msg.OK
        };
        var message = [];
        message.push('Следующие запросы без связи и SELECT полей:');
        for (var i = 0; i < noRelationsEntities.length; i++){
            message.push(noRelationsEntities[i].data.entityId);
        }
        Ext.Msg.show(Ext.apply(messageObject, {msg: message.join('<br/>')}));
        normal = false;
    }
    if (!haveAtLeastOneSelect) {
        Ext.Msg.show({
            title: 'Внимание',
            buttons: Ext.Msg.OK,
            msg: 'Должно быть хотя бы одно выбранное поле (SELECT)'});
        normal = false;
    }

    return normal;
}

// Отправляет запрос на сервер и получает sql-запрос в качестве ответа
function showQueryText(){
    // Валидация запроса
    if (!queryValidation()){
        return;
    }

    var loadMask = new Ext.LoadMask(panel.body);
    loadMask.show();

	Ext.Ajax.request({
		url: '{{component.params.query_text_url }}'
		,params: {
			'objects': Ext.encode( buildParams() )
		}
		,success: function(response){
			loadMask.hide();
            var childWin = smart_eval(response.responseText);
		}
		,failure: function(){
        	loadMask.hide();
            uiAjaxFailMessage.apply(this, arguments);
        }
	});
}

// Сохраняет запрос
function saveQuery(){

    // Валидация запроса
    if (!queryValidation()){
        return;
    }

	var queryName = edtQueryName.getValue();
	if (!queryName) {
		Ext.Msg.show({
		   title:'Внимание',
		   msg: 'Не введено название запроса',
		   buttons: Ext.Msg.OK,
		   animEl: 'elId',
		   icon: Ext.MessageBox.WARNING
		});
		return;
	}
	
	// Получение имени запроса	
	var loadMask = new Ext.LoadMask(panel.body);
    loadMask.show();
    
	Ext.Ajax.request({
		url: '{{ component.params.save_query_url }}'
		,params: {
			'objects': Ext.encode(buildParams()),
            'query_name': queryName,
            'id': hdnID.getValue()
		},
        success: function(response){
            smart_eval(response.responseText);
            panel.setTitle(edtQueryName.getValue());

            //Проставляем новосозданному объекту айди при успешном сохранении.
            var responseText = response.responseText;
            var responseData = Ext.util.JSON.decode(responseText);
            if (typeof responseData.id !== 'undefined'){
                hdnID.setValue(responseData.id);
            }

			loadMask.hide();
		},
        failure: function(){
        	loadMask.hide();
            uiAjaxFailMessage.apply(this, arguments);
        }
	});		
}

/**
 * Функция проверки связи между сущностями
 */
function checkSubQueriesRelations(){
    // Сначало проверяем, имеются ли SELECT поля у данного запроса.
    // Если нет, то проверяем связан ли он с другими запросами.
    var entities = grdSelectedEntities.getStore().getRange(),
        // Список сущностей без SELECT полей и связей с другими сущностями.
        noRelationsEntities = [],
        haveAtLeastOneSelectField = false;
    for (var i = 0, len = entities.length; i < len; i++){
        var haveSelectField = haveQuerySelectField(entities[i].id);
        if (!haveSelectField && !haveQueryRelations(entities[i].id)){
            // Следовательно сущность не имеет SELECT полей и не связана с другими сущностями
            noRelationsEntities.push(entities[i]);
        }
        if (haveSelectField) {
            haveAtLeastOneSelectField = true;
        }
    }
    return [noRelationsEntities, haveAtLeastOneSelectField];
}

/*
 * Функция проверяет им12еется ли у данного подзапроса SELECT поля
 */
function haveQuerySelectField(entityID){

    var haveSelect = false,
        selectedFields = grdSelectedFields.getStore().getRange();

    for (var i = 0, len = selectedFields.length; i < len; i++){
        // Каждая запись в гриде выбранных SELECT полей имеет вид
        // ИмяПриложения.ИмяМодели.ИмяПоля. Мы выдергиваем ИмяПоля и сравниваем
        // c параметров. Если нашлось совпадение, то у сущности есть SELECT поля
        if (selectedFields[i].data.entityId === entityID){
            haveSelect = true;
            break;
        }
    }
    return haveSelect;
}

/*
 * Функция проверяет имеется ли у данного подзапроса связи
 */
function haveQueryRelations(entityID){
    var haveRelation = false,
        relations = grdLinks.getStore().getRange();

    for (var i = 0, len=relations.length; i < len; i++){
        // Идентификатор записи в гриде связей таблиц имеет вид
        // ИмяСущности1-ИмяПоляСвязи1|ИмяСущности2-ИмяПоляСвязи2
        var firstEntityID = relations[i].id.split('|')[0].split('-')[0],
            secondEntityID = relations[i].id.split('|')[1].split('-')[0];

        if ((entityID === firstEntityID && entityID !== secondEntityID) ||
            entityID !== firstEntityID && entityID === secondEntityID){
            haveRelation = true;
            break;
        }
    }

    return haveRelation;
}

// Билдит параметры, для показа запроса и для сохранения запроса
function buildParams(){
	function getElements(grid, exclusionFields){
		exclusionFields = exclusionFields || [];
		var mass = [],
		    range = grid.getStore().getRange();

		for (var i= 0, len=range.length; i<len; i++){
			mass.push(range[i].data);
			
			mass[mass.length-1]['id'] = range[i].id;
			
			for (var j=0; j<exclusionFields.length; j++){
				delete mass[mass.length-1][exclusionFields[j]];				
			}
		}
		return mass;
	}

	// Сущности в запросе
	var entities = getElements(grdSelectedEntities);
	
	// Связи в запросе
	var relations = getElements(grdLinks);
			
	// Поля в выборке
	var selectedFields = getElements(grdSelectedFields);	
	
	// Группируемые и агригируемые поля
	var groupFields = getElements(grdGroupFields);	
	
	var groupAggrFields = getElements(grdGroupAggrFields);	

	// Условия
	var condFields = getElements(grdConditionsFields);

	var limit;
	if (limitChk.checked) {
		limit = limitCount.getValue();
	}

    var canJoinRemove = false;
    if (joinRemovalChk) {
        canJoinRemove = joinRemovalChk.checked;
    }

	return {
		'entities': entities,
		'relations': relations, 
		'selected_fields': selectedFields,
		'group': {
			'group_fields': groupFields,
			'group_aggr_fields': groupAggrFields
		},
		'cond_fields': condFields,
		'distinct': distinctChk.checked,
		'limit': limit || -1,
        'join_removal': canJoinRemove
	}
}


/*
 * Если запрос открыт на редактирование, нужно из имеющихся сущностей 
 * заполнить деревья полей
 */
(function (){
	var models = [],
        queries = [],
		range = grdSelectedEntities.getStore().getRange();

	for (var i= 0, len=range.length; i<len; i++){

        if (range[i].data['entityType'] === modelType || range[i].data['entityType'] === ''){
            models.push(range[i].id);
        }else{
            queries.push(range[i].id);
        }
	}

	if (models || queries) {
		entityModel.add(models, queries);
	}
}());
