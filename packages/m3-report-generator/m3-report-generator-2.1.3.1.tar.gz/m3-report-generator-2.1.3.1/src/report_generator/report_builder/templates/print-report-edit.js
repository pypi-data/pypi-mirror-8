/**
 * created by prefer, at 04.10.2011 07:10
 * 
 * Окно для создания/редактирования.
 * 
 * Включает в себя экземпляры классов для упрощенной работы (взаимодействие с другими
 * компонентами, создания/редактирование/удаление):
 * allSections - для отображения всех секций в шаблоне. Используется дерево treeTemplateSections
 * sectionModel - для используемых секций. - treeUsedSections
 * queryModel - для используемых запросов. - treeUsedQueries
 * paramModel - для полей с параметрами. - treeQueriesParams
 * matchingModel - для сопоставлений. - treeMatchingFields
 * */

var
	// Основные значения
	strName = Ext.getCmp('{{ component.str_name.client_id }}'),
	templateUploadField = Ext.getCmp('{{ component.fupf_template.client_id }}'),
	pnlMaching = Ext.getCmp('{{ component.pnl_maching.client_id }}'),
	frmMain = Ext.getCmp('{{ component.frm_form.client_id }}'),

	// Вкладка "Запросы"
 	treeQueries = Ext.getCmp('{{ component.tree_all_queries.client_id }}'),
	treeUsedQueries = Ext.getCmp('{{ component.tree_used_queries.client_id }}'),

	// Вкладка "Параметры запроса"
	treeFormParams = Ext.getCmp('{{ component.tree_form_params.client_id }}'),	
	treeQueriesParams = Ext.getCmp('{{ component.tree_queries_params.client_id }}'),
	
	// Вкладка "Порядок секций"
	treeTemplateSections = Ext.getCmp('{{ component.tree_template_sections.client_id }}'),
	treeUsedSections = Ext.getCmp('{{ component.tree_used_sections.client_id }}'),	
	
	// Вкладка "Сопоставление секций"
	treeMatchingFields = Ext.getCmp('{{ component.tree_maching_fields.client_id }}'),

    treeSubQueries = Ext.getCmp('{{ component.tree_query.client_id }}'),

    // ID
    hdnId = Ext.getCmp('{{ component.hdn_id.client_id }}'),

    gridQuery  = Ext.getCmp('{{ component.grd_query.client_id }}'),

    reportKeyField = Ext.getCmp('{{ component.report_key_field.client_id }}'),

    // Окно открыто в режиме редактирования
    editMode = Ext.decode('{{ component.is_edit|lower }}'),

    panel = component;

/**
 * При изменении шаблона происходит удаление всех секций, использованных секций и
 * сопоставлений
 */
templateUploadField.on('beforechange', function(cmp, value){
	if (!value) {
		Ext.Msg.show({
			title:'Внимание',
		    msg: 'Будут удалены все секции шаблона и выбранные значения',
		    buttons: Ext.Msg.YESNO,
		    fn: function(buttonId, text, opt){
		    	if (buttonId==='yes'){
		    		allSections.removeAll();
		    		sectionModel.removeAll();
		    		matchingModel.removeAll();
		    		
		    		templateUploadField.clearFeild();
		    	}		   		
		    },
		    animEl: 'elId',
		    icon: Ext.MessageBox.QUESTION
		});
		return false;
	}
	return true;
});

// Переопределяем поведение при нажатии кнопки загрузки
templateUploadField.clickDownload = function() {
    var url = '{{ component.params.download_url }}',
        file_name = templateUploadField.getFileName(),
        report_id = hdnId.getValue();

    assert(url, 'Url for template download undefined');

    var params = [];

    params.push('file_name=' + file_name);
    params.push('report_id=' + report_id);

    open(url + "?" + params.join("&"));
};

/**
 * Класс, для работы с всеми имеющимися секциями в шаблоне
 */
var allSections = new function(){

	// Список всех секций в шаблоне
	var _jsonNodes = [];	
	
	return {
		/**
		 * Добавление всех возможных секции
		 * */
		addNodes: function(nodes){
			_jsonNodes = nodes;
			
			var rootNode = treeTemplateSections.getRootNode();							
			rootNode.removeAll();
			for (var i=0, nodesCount=nodes.length; i<nodesCount; i++) {
			
				var nodeTemplateParams = new Ext.tree.TreeNode(nodes[i]);
			   
			    rootNode.getOwnerTree().getLoader().doPreload(nodeTemplateParams);                
			    if(nodeTemplateParams){
			        rootNode.appendChild(nodeTemplateParams);
			    }	
			}
			rootNode.loaded = true;
			
		},
		/**
		 * Возврат всех секций в виде json объекта
		 */ 
		getNodes: function(){
			return _jsonNodes;
		},
		/**
		 * Получение одной секции в виде json-объекта
		 */ 
		getSectionNode: function(idSection){
			for (var i= 0, len=_jsonNodes.length; i<len; i++){
				// Поиск по наименованию, т.к. он является идентификатором и не повторяется				
				if (_jsonNodes[i]['template_field'] === idSection){
					return _jsonNodes[i];
				}
			}
		},
		/**
		 * Удаление всех секций
		 */
		removeAll: function(){
			treeTemplateSections.getRootNode().removeAll();
		}
	}
};

/**
 * Класс, для используемых секции в отчете
 */
var sectionModel = new function(){

	// Используемые секции
	// Пример формата: {idSection: {template_field:u"..", children:[{"Параметры секции"}]} }
	var _sections = {};	
	
	return {
		/**
		 * Добавление секции
		 * @param idSection: Идентификатор секции
		 * @param typeOutput: Тип вывода секции (Фиксированный, Горизонтальный, Вертикальный)
		 */
		addSection: function(idSection, typeOutput, priorityOutput, target){

            if (!target){
                target = treeUsedSections.getRootNode();
            }

			var section = allSections.getSectionNode(idSection),
                nodeTemplateParams,
                tagInfo;

			section = Ext.apply(section, {'type_output': typeOutput,
			     'priority_output': priorityOutput, 'section': idSection});

			_sections[idSection] = section;

			nodeTemplateParams = new Ext.tree.TreeNode(section);

			nodeTemplateParams.expanded = false;
            target.getOwnerTree().getLoader().doPreload(nodeTemplateParams);
            // Убираем тэги. Т.к. они не должны отображаться.
            nodeTemplateParams.childNodes = [];
		    if(nodeTemplateParams){
                target.appendChild(nodeTemplateParams);
		    }

            target.loaded = true;

            tagInfo = this.getTagInfo(section);
			nodeTemplateParams.setTooltip(String.format('<b>Тип вывода: </b>{0}</br><b>Приоритет вывода: </b>{1}</br><b>Тэги: </b></br>{2}',
                                    typeOutput, priorityOutput, tagInfo));
		},

        loadSectionsTree: function(reportSections){

            for (var i = 0, count=reportSections.length; i < count; i++){

                var section  = { 'section': reportSections[i], 'visit': false },
                    queue = [section];

                var node = allSections.getSectionNode(reportSections[i]['section']);
                Ext.applyIf(node, reportSections[i]);
                _sections[node['section']] = node;
                node = new Ext.tree.TreeNode(node);

                var treeQueue = [node];
                treeUsedSections.getRootNode().appendChild(node);

                var sectionTree = node;
                while (queue.length){
                    section = queue.shift();
                    node = treeQueue.shift();

                    if (!section['visit']){
                        section['visit'] = true;

                        var tagInfo = this.getTagInfo(node.attributes);
                        node.setTooltip(String.format('<b>Тип вывода: </b>{0}</br><b>Приоритет вывода: </b>{1}</br><b>Тэги: </b></br>{2}',
                            section['section']['type_output'], section['section']['priority_output'], tagInfo));

                        var subSections = section['section'].sub_sections;
                        for (var j = 0, len=subSections.length; j < len; j++){
                            var sub_section = { 'section': subSections[j], 'visit': false};
                            queue.push(sub_section);

                            var childNode = allSections.getSectionNode(subSections[j]['section']);
                            Ext.applyIf(childNode, subSections[j]);
                            _sections[childNode['section']] = childNode;
                            childNode = new Ext.tree.TreeNode(childNode);
                            node.appendChild(childNode);
                            treeQueue.push(childNode);
                       }
                    }
                }
            }

            treeUsedSections.getRootNode().loaded = true;
        },

        /**
         * Подготавливаем строку со списком тэгов для tooltip.
         * @param section - секция шаблона.
         */
        getTagInfo: function(section){

            var fieldInfo = [];
            if (section.children) {
                for (var i = 0, len=section.children.length; i < len; i++){
                    fieldInfo.push(' - ' + section.children[i].template_field);
                }
            }


            return fieldInfo.join('</br>');
        },
		/**
		 * Добавляет секцию (открывает промежуточное окно с параметрами) 
		 * из дерева всех секций
		 * @param node: Узел дерева со всеми секциями
		 */
		openWindowFromNode: function(data, newSection){
			
            var url = '{{ component.params.type_output_url }}';
            assert(url, 'Url for child window is not define');
        
            var loadMask = new Ext.LoadMask(panel.body);
            loadMask.show();
            Ext.Ajax.request({
                url: url
                ,params:  panel.actionContextJson || {}
                ,success: function(response, opt){
                    loadMask.hide();
                    
                    var childWin = smart_eval(response.responseText);

                    childWin.fireEvent('loadData', data);
                    childWin.on('selectData', function(values){
                        
                    	// Если проверка не проходит, обработка заканчивается
                        if(!this.checkPriority(data['sectionID'],
                            values['priorityOutput'])){
                            return;
                        }

                    	if (newSection){
                    	   sectionModel.addSection(data['sectionID'], 
                    	               values['typeOutput'], 
                    	               values['priorityOutput'],
                                       data['target']);
                    	} else {
                    		sectionModel.editSection(data['sectionID'], 
                                       values['typeOutput'], 
                                       values['priorityOutput']);
                    	}
                                        
                    }, this);
                                
                }
                ,failure: function(){
                    loadMask.hide();
                    uiAjaxFailMessage.apply(this, arguments);
                }
                ,scope: this
            });
		},
		/**
		 * Проверка на то, имеется ли уже секция с таким же приоритетом
		 */
		checkPriority: function(sectionID, priorityOutput){
            var nodes = treeUsedSections.getRootNode().childNodes,
                count = nodes.length;
            for (var i = 0; i < count; i++){
                var queue = [],
                    sctn  = {'section': nodes[i], 'visit': false};
                queue.push(sctn);

                while (queue.length){
                    sctn = queue.shift();

                    if (!sctn['visit']){
                        sctn['visit'] = true;

                        if (sectionID !== sctn['section'].attributes['template_field'] &&
                            sctn['section'].attributes['priority_output'] === priorityOutput){
                            Ext.Msg.show({
                                title: 'Внимание',
                                msg: String.format(
                                    'Уже имеется секция "{0}" c приоритетом {1}',
                                    sctn['section'].attributes['template_field'], // 0
                                    priorityOutput // 1
                                ),
                                buttons: Ext.Msg.OK
                            });
                            return false;
                        }

                        var childs = sctn['section'].childNodes;
                        for (var j = 0, len=childs.length; j < len; j++){
                            var subSctn = {'section': childs[j], 'visit': false};
                            queue.push(subSctn);
                        }
                    }
                }
            }
            return true;
		},
		
		/**
		 * Редактирование поля 
		 */
		editSection: function(sectionID, typeOutput, priorityOutput){
           if(!this.checkPriority(sectionID, priorityOutput)){
                return;
            }
			
			var selectedNode = treeUsedSections.getSelectionModel().getSelectedNode();			
			selectedNode.setTooltip(String.format('Тип вывода: {0}</br>Приоритет вывода: {1}',typeOutput, priorityOutput), sectionID);
			
			selectedNode.attributes['template_field'] = sectionID;
			selectedNode.attributes['type_output'] = typeOutput;
			selectedNode.attributes['priority_output'] = priorityOutput;		
		},
		
		/**
		 * Возвращает порядок вывода секций 
		 * TODO: добавить атрибут следования секций и выводить порядок по 
		 * атриубуту
         * TODO: Необходимо переделать данный метод для деревьев секций.
		 */
		getOrderSections: function(){ 
			var res = [], 
				selectedNode = treeUsedSections.getRootNode(),
			    nodes = selectedNode.childNodes;
				
			for (var i= 0, count=nodes.length; i<count; i++){
				res.push(nodes[i].attributes['template_field']);
			}
			return res;
		},
		/**
		 * Получение одной секции в виде json-объекта
		 * @param idSection: Идентификатор секции
		 */
		getSectionNode: function(idSection){
			return _sections[idSection];		
		},
		getSections: function(idSection){
            return _sections;        
        },
		/**
		 * Удаление всех имеющихся секций в отчете
		 */
		removeAll: function(){
			_sections = {};
			treeUsedSections.getRootNode().removeAll();
		},
        remove: function(node){
            var sectionName,
                templateField;
            for (var obj in _sections){
                templateField = _sections[obj]['template_field'];
                if (templateField == node.attributes['template_field']){
                    sectionName = templateField;
                    break;
                }
            }

            // Удаление из дерева сопоставлений
            matchingModel.removeForSectionTree(sectionName);
            // Удаление из дерева секций
            delete _sections[sectionName];
            node.remove();
        }
	}
};

/**
 * Обработчик на редактировании секции
 */
function onEditSection(){
    var selectedNode = treeUsedSections.getSelectionModel().getSelectedNode();
    if (selectedNode){
        sectionModel.openWindowFromNode({
            'sectionID':selectedNode.attributes.template_field,
            'typeOutput':selectedNode.attributes.type_output,
            'priorityOutput':selectedNode.attributes.priority_output
        }, false);
    }
}

/**
 * Обработчик на удаление секции
 */
function onDeleteSection(){
    var selectedNode = treeUsedSections.getSelectionModel().getSelectedNode();
    var messageObject = {
        title: 'Внимание',
        buttons: Ext.Msg.YESNO,
        icon: Ext.MessageBox.INFO,
        fn: function(btn){
            if (btn == 'yes'){
                sectionModel.remove(selectedNode);
            }
        }
    };

    // Флаг, который показывает, является ли секция сопоставлена с полем запроса.
    var isMatching = false;
    if (treeMatchingFields.getRootNode().findChild('template_field', selectedNode.attributes['template_field'])){
        isMatching = true;
    }

    // Если сопоставлена, то сообщаем пользователю.
    if (isMatching){
        var messages = [];
        messages.push('Данная секция имеет связи!');
        messages.push('Согласны продолжить?');
        Ext.Msg.show(Ext.apply(messageObject, {msg: messages.join('<br/>')}));
    }else{
        sectionModel.remove(selectedNode);
    }
}

/**
 * Проверка на возможность добавления секций 
 */
treeUsedSections.on('nodedragover', function(o){
    /**
     * Проверка на существование запроса в отчете
     * @param queryID: Идентификатор секции
     */
    function checkRepeatNode(sectionID){        
        return sectionModel.getSectionNode(sectionID) === undefined;
    }
    
    return o.dropNode.getOwnerTree() === treeTemplateSections &&
        //treeUsedSections.getRootNode() === o.target &&
        checkRepeatNode(o.dropNode.attributes.template_field);

});

/**
 * Действия, производимые при добавлении d&d секции в дерево используемых секций
 */
treeUsedSections.on('beforenodedrop', function(o){
    sectionModel.openWindowFromNode({
        'sectionID':o.dropNode.attributes.template_field,
        'target': o.target
    }, true);

    return false;
});

/**
 * Ajax запрос для отправки темплэйта, распарсивание и получение его параметров
 */
templateUploadField.on('fileselected', function(){
		
	var url = '{{ component.params.template_load_url }}';
	assert(url, 'Url for template load not define');
	
	var loadMask = new Ext.LoadMask(panel.body);
	loadMask.show();
			
	frmMain.getForm().submit({
		clientValidation: false,
		url: url,
		success: function(form, action){
			loadMask.hide();

			var nodes = action.result['sections'];
						
			// Добавление имеющихся секций в соответвующую модель
			allSections.addNodes(nodes);
		},
		failure: function(){
			loadMask.hide();
			uiAjaxFailMessage.apply(this, arguments);
		}
	});
});

/**
 * Класс модели для объектов запросов 
 */
var queryModel = new function(){

	// Список запросов с параметрами
	var _paramNodes = [];
	
	// Список запросов с select полями
	var _selectNodes = [];
	
	return {
		/**
		 * Добавление запроса
		 * Вызывается при добавлении запросов в отчет, генерируется ajax запрос
		 * для получения select-полей и параметров для данного запроса
		 * @param queryID: Идентификатор запроса
		 * */
	    add: function(queryID){

			var url = '{{ component.params.query_data_url }}';
			assert(url, 'Url for child window is not define');

			var loadMask = new Ext.LoadMask(panel.body);
			loadMask.show();
			Ext.Ajax.request({
				url: url,
                scope: this,
                params: {
					'query_id': queryID
				},
                success: function(response, opt){

					loadMask.hide();
					var obj = Ext.decode(response.responseText);
					if (!obj.success) {
						Ext.Msg.alert('Ошибка', obj.message);
						return;
					}

					this.loadSelectNodes(obj.data.selectNodes);
					this.loadParamsNodes(obj.data.paramsNodes);
				},
                failure: function(){
					loadMask.hide();
	        		uiAjaxFailMessage.apply(this, arguments);
				}
			});
		},
		/**
		 * Загрузка запросов для селекта в дерево treeUsedQueries во вкладке 
		 * Сопоставление секций дерево "Запросы/словари отчета"
		 */
		loadSelectNodes: function(node){

			var rootNodeSelectedQuery = treeUsedQueries.getRootNode(),
				selectedNode = new Ext.tree.TreeNode(node);
				
			selectedNode.expanded = false;

			rootNodeSelectedQuery.getOwnerTree().getLoader().doPreload(selectedNode);

            // Убираем SELECT поля. Т.к. они не должны отображаться.
            // Здесь будет метод, который учитывает SELECT поле это или подзапрос.
            selectedNode.childNodes = [];
            //

		    if(selectedNode){
		        rootNodeSelectedQuery.appendChild(selectedNode);
		    }
			rootNodeSelectedQuery.loaded = true;

			_selectNodes.push(node);

            var fieldInfo = this.addToolTip(node);
            selectedNode.setTooltip(String.format('<b>Поля запроса: </b></br>{0}',fieldInfo));

		},

        /**
         * Добавление tooltip к записи запроса.
         */
        addToolTip: function(node){

            // Формируем список SELECT полей запроса.
            var fieldInfo = [];
            for (var i = 0, len=node.children.length; i < len; i++){
                fieldInfo.push(' - ' + node.children[i].name);
            }

            return fieldInfo.join('</br>');
        },

		/**
		 * Загрузка запросов для параметров в дерево treeQueriesParams во вкладке
		 * Параметры формы
		 */
		loadParamsNodes: function(nodes){

			var rootNodeParams = treeQueriesParams.getRootNode(),
				nodeParams = new Ext.tree.TreeNode(nodes);
		   
		    rootNodeParams.getOwnerTree().getLoader().doPreload(nodeParams);                
		    if(nodeParams){
		        rootNodeParams.appendChild(nodeParams);
		    }				    
			rootNodeParams.loaded = true;				
		    //--
			_paramNodes.push(nodes);
		},
		
		/**
		 * Удаление запроса
		 * */
		remove:function(node){
            var queryID = node.attributes['query_id'],
                i, len;

            // Индекс, удаляемого из массива элемента
            var ind = -1;
            for (i = 0, len=_selectNodes.length; i < len; i++){
                 if (queryID === _selectNodes[i]['query_id']){
                     ind = i;
                 }
            }

            // Удаление из дерева параметров запроса
            var rmvNode = treeQueriesParams.getRootNode().findChild('id', queryID);
            if (rmvNode){
                rmvNode.remove();
            }
            //

            // Удаление из дерева параметров формы
            paramModel.removeForQueryTree(queryID);

            // Удаление из грида подстановки значений
            var queryStore = gridQuery.getStore(),
                queryRange = queryStore.getRange();
            for (i = 0, len=queryRange.length; i < len; i++){
                if (node.findChild('query_id', queryRange[i].data['fieldID'])){
                    queryStore.remove(queryRange[i]);
                }
            }
            //

            // Удаление из дерева подстановки значений
            substitutionValueModel.removeForQueryTree(queryID);
            //

            // Удаление из дерева сопоставлений
            matchingModel.removeForQueryTree(queryID);
            //

            // Удаление из дерева запросов
            if (ind !== -1){
                _selectNodes.splice(ind, 1);
            }

            node.remove();
		},
		/**
		 * Возвращение данных селект запроса по id запроса 
		 */
		getQueryForSelect: function(id){
			for (var i= 0, count=_selectNodes.length; i<count; i++){
				// Поиск по наименованию, т.к. он является идентификатором и не повторяется				
				if (_selectNodes[i]['query_id'] === id){
					return _selectNodes[i];
				}			
			}
		},
		/**
		 * Возвращение всех имеющихся id запросов
		 */
		getQueries: function(){
			var res = [];
			for (var i= 0, count=_selectNodes.length; i<count; i++){
                res.push(_selectNodes[i]['query_id']);
            }
            return res;
		}
	}
};

/**
 * Обновляет имеющиеся запросы
 * TODO: не прибинден к кнопке обновления. Этой кнопки нет.
 */
function refreshQueries(){
	var rootNode = treeQueries.getRootNode();
	treeQueries.getLoader().load(rootNode);
	rootNode.expand();
}

/**
 * Хэндлер добавления запроса
 */
function onAddQuery(){
	var node = treeQueries.getSelectionModel().getSelectedNode();	
	if (node) {		
		addQuery(node);		
	}
}

/**
 * Добавление запроса в отчет 
 */
function addQuery(node){
	if (!node.isLeaf()) {
		// Родительские узлы не интересуют 
		return;
	} 	
	queryModel.add(node.id);
}

/**
 * 
 */
function onDeleteQuery(){
	var selectedNode = treeUsedQueries.getSelectionModel().getSelectedNode(),
        messageObject = {
            title: 'Внимание',
            buttons: Ext.Msg.YESNO,
            icon: Ext.MessageBox.INFO,
            fn: function(btn){
                if (btn == 'yes'){
                    queryModel.remove(selectedNode);
                }
            }
        },
        isMatching = false;

    if (treeMatchingFields.getRootNode().findChild('query_id', selectedNode.attributes['query_id']) ||
         treeQueriesParams.getRootNode().findChild('id', selectedNode.attributes['query_id'])){
        isMatching = true;
    }

    if (isMatching){
        var messages = [];
        messages.push('Данное поле имеет связи!');
        messages.push('Согласны продолжить?');
        Ext.Msg.show(Ext.apply(messageObject, {msg: messages.join('<br/>')}));
    }
    else{
        queryModel.remove(selectedNode);
    }
}

function loadToTreeFormParams(treeNodes){
    for (var i=0; i<treeNodes.length; i++){
        var rootNode = treeFormParams.getRootNode(),
        // Добавление корневого узла как поля
            node = new Ext.tree.TreeNode(treeNodes[i]);

        rootNode.getOwnerTree().getLoader().doPreload(node);
        if(node){
            rootNode.appendChild(node);
        }
        rootNode.loaded = true;
    }
}

/**
 * Класс-модель, обеспечивающая работу действий во вкладке Сопоставление секций
 */
var paramModel = new function(){
	
	// Объект для запросов, привязанных к параметрам
	// key - id запроса
	// value - Список параметров 
	var _queriesParams = {};
	
	// Объект для полей, привязанных к параметрам
	// key - идентификатор поля (либо node.id, либо другой идентификатор, однозначно
	// определяющий поле)
	// value - Объект для поля, включающий parameters - список прибинденных параметров 
	var _fieldsParams = {};

	return {
		/**
		 * Установка данных. Используется при первоначальной установки значений.
		 */
		setData: function(treeNodes, queriesParams, fieldParams){
			loadToTreeFormParams(treeNodes);

			_queriesParams = queriesParams;
			_fieldsParams = fieldParams;
		},
		
		/**
		 * Добавление поля к отчету
		 * */
		add: function(node, o){
    		var queryID = node.parentNode.id,
				fieldName = node.attributes['field'],
                paramName = node.attributes['name'],
		        nodeID = this.addNode(o, paramName, queryID);

		    // Добавление в список параметров в запросе		    
			this.addQueryParam(queryID, paramName);

			// Добавление в список полей в запросе
			_fieldsParams[nodeID] = Ext.apply(o, {'params': []});
			this.addFieldParam(nodeID, paramName, queryID);
		},
		/**
		 * Добавление параметра к существующему полю
		 */
		addNode: function(obj, paramName, queryID){
			var rootNodeSelectFields = treeFormParams.getRootNode();						
			// Добавление корневого узла как поля
			var nodeSelect = new Ext.tree.TreeNode(Ext.apply({
				'expanded': true,
				'name': obj['fieldName'], // Название полей могут отличаться
				'iconCls': 'icon-folder-table'
			}, obj));
						
			// Добавление выбранного параметра
			nodeSelect.appendChild(new Ext.tree.TreeNode({
				'name': paramName,
				'query_id': queryID,
				'iconCls': 'icon-table-gear'
			}));
		    
		    
		    if(nodeSelect){
		        rootNodeSelectFields.appendChild(nodeSelect);
		    }
		    rootNodeSelectFields.loaded = true;
		    
		    return nodeSelect.id;
		},
		/**
		 * Добавление параметра в объект запросов
		 */
		addQueryParam: function(queryID, paramID){
			if (_queriesParams[queryID] instanceof Array){
		    	_queriesParams[queryID].push( paramID );
		    } else {
		    	_queriesParams[queryID] = [paramID];
		    }		
		},
		/**
		 * Добавление параметра в объект полей
		 */
		addFieldParam: function(nodeID, paramID, fieldID){
		    _fieldsParams[nodeID]['params'].push({name: paramID, query_id:fieldID});
		},
	    /**
	     * Возвращение параметров для запросов
	     */
		getQueriesParams: function(){
			var res = [],
				o;
			for (o in _queriesParams){
				res.push({
					'query_id': o,
					'params':_queriesParams[o] 
				});
			}
			return res;
		},
		/**
		 * Возвращает все параметры со всеми полями
		 */
		getFieldsParams: function(){
			var res = [],
				o;
			for (o in _fieldsParams){
				res.push( _fieldsParams[o] );
			}
			return res;
		},

		/**
		 * Возвращает параметры по id запроса
		 */
		getParamsByQuery: function(queryID){			
			for (var o in _queriesParams){
				if (o === queryID){
					return _queriesParams[o];
				}                
            }
            return [];
		},
		/**
		 * Добавляет поле с одним параметром
		 */
		addParameter: function(queryID, fieldID, paramID){
			this.addQueryParam(queryID, paramID);
			this.addFieldParam(fieldID, paramID);
		},
		/**
		 * Открывает окно с редактированием атрибутов поля
		 * newField == true - новое окно
		 * newField == false - в режиме редактирования
		 */
		openParamWindow: function (node, newField){
            var url = '{{ component.params.condition_url }}';
            assert(url, 'Url for child window is not define');

            var loadMask = new Ext.LoadMask(panel.body);
            loadMask.show();
            Ext.Ajax.request({
                url: url
                ,params: {}
                ,success: function(response, opt){
                    loadMask.hide();
                    var childWin = smart_eval(response.responseText),
                    // Обработчик события 'selectData'
                        selectDataHandler;
                    if (newField) {
                        selectDataHandler = function(o){
                            paramModel.add(node, o);
                            node.remove();
                        };
                        childWin.fireEvent('loadData', {
                            param: node.attributes['param']
                        });
                        childWin.on('selectData', selectDataHandler);
                    } else {
                        // Обьект, который мы передаем в событие 'loadData'
                        var eventObj = _fieldsParams[node.id];
                        selectDataHandler = function(o){
                            node.setText(o['name']);
                            _fieldsParams[node.id] = Ext.applyIf(o, _fieldsParams[node.id]);
                        };
                        childWin.fireEvent('loadData', eventObj);
                        childWin.on('selectData', selectDataHandler);
                    }
                }
                ,failure: function(){
                    loadMask.hide();
                    uiAjaxFailMessage.apply(this, arguments);
                }
            });
        },
        /**
         * Удаляет поле на форме из отчета
         */
        deleteField: function(node){
        	Ext.Msg.show({
                title:'Внимание',
                msg: 'Вы действительно хотите удалить поле?',
                buttons: Ext.Msg.YESNO,
                fn: function(buttonId, text, opt){
                    if (buttonId==='yes'){
                    	// Определение имеющихся запросов и параметров для поля
                    	var queries = {},
                    	    params,
                            childNodes,
                            i, j;

                    	for (var queryID in _queriesParams){
                    		params = [];
                    		var queryParams = _queriesParams[queryID]; 
                    		for (j=queryParams.length-1; j>=0; j--){
                    			childNodes = node.childNodes;
                    			for (i=0; i<childNodes.length; i++){

                                    if (queryParams[j] === childNodes[i].attributes['name']){
                                        params.push(childNodes[i].attributes);
                                        queryParams.splice(j, 1);
                                        break;
                                    }
                    			}                      	    
                        	}
                        	
                        	if (!queryParams.length){                        		
                        		delete _queriesParams[queryID];
                        	}
                        	
                        	queries[queryID] = params;
                        }

                        // Нахождение существующих узлов и добавление параметров в
                        // дерево treeQueriesParams (всех запросов и параметров)
                        childNodes = treeQueriesParams.getRootNode().childNodes;
                        var treeParams,
                            count = childNodes.length,
                            childCount;

                        for (i=0; i<count; i++){
                        	treeParams = queries[childNodes[i].id];
                        	if (treeParams){
                        		for (j=0, childCount=treeParams.length; j<childCount; j++){
                                    delete treeParams[j]['field_id'];
                                    childNodes[i].appendChild(new Ext.tree.TreeNode(treeParams[j]));
                                    childNodes[i].expand();
                        		}
                        	}
                        }
                                                
                        delete _fieldsParams[node.id];
                        node.remove();
                        
                    }               
                },
                animEl: 'elId',
                icon: Ext.MessageBox.QUESTION
            });
        },

        removeForQueryTree: function(queryID, queryNodes){
            delete _queriesParams[queryID];

            var i, len, obj;

            for (obj in _fieldsParams){
                for (i = 0, len=_fieldsParams[obj].params.length; i < len; i++){
                    if (_fieldsParams[obj].params[i].query_id == queryID){
                        delete _fieldsParams[obj].params[i];
                        delete _fieldsParams[obj].children[i];
                    }
                }
            }

            // Удаление из дерева "Выбранные запросы и их параметры"
            var nodes = treeFormParams.getRootNode().childNodes;
            len   = nodes.length;
            for (i = len - 1; i >= 0; i--){

                var rmvNode = nodes[i].findChild('query_id', queryID);

                if (rmvNode){
                    rmvNode.remove();
                }

                if (!nodes[i].childNodes.length){
                    nodes[i].remove();
                    break;
                }
            }
        }
	}
};

/**
 * Определение, куда можно кидать параметры на дерево имеющихся параметров
 */
treeFormParams.on('nodedragover', function(o){
	if (o.dropNode.getOwnerTree() === treeFormParams){
		return false;
	} else if ( o.target instanceof Ext.tree.TreeNode && 
		treeFormParams.getRootNode().id === o.target.id && o.dropNode.isLeaf()){ 
		// Если кидается узел в пустое пространство дерева			
		return false;	
	} else if (o.dropNode.childNodes.length === 0 &&
		treeFormParams.getRootNode().id === o.target.parentNode.id){
		// Если кидается узел на имеющиеся поле			
		return true;
	}
	
	return false;		
});

/**
 * Позволяет работать только с дочерними узлами дерева всех параметров, т.е.
 * непосредственно с параметрами, а не с запросами.
 */
treeFormParams.on('beforenodedrop', function(o){
	if ( o.target instanceof Ext.tree.TreeNode &&
		treeFormParams.getRootNode().id === o.target.id){
		//paramModel.openParamWindow(o.dropNode, true);
		return false;
	} else if (o.dropNode.isLeaf() && o.target instanceof Ext.tree.TreeNode && 
		treeFormParams.getRootNode().id === o.target.parentNode.id){
			
		var queryID = o.dropNode.parentNode.attributes['id'],
		fieldID = o.target.id,
		paramID = o.dropNode.attributes['name'];
		
		paramModel.addParameter(queryID, fieldID, paramID);
	
		return true;
	}
});


/**
 * Проверка на возможность добавления запросов
 */
treeUsedQueries.on('nodedragover', function(o){
    /**
     * Проверка на существование запроса в отчете
     * @param queryID: Идентификатор запроса
     */

    function checkRepeatNode(queryID){
        return queryModel.getQueryForSelect(queryID) === undefined;
    }
    return o.dropNode.getOwnerTree() === treeQueries &&
        treeUsedQueries.getRootNode() === o.target &&
        checkRepeatNode(o.dropNode.id);

});

/**
 * Действия при добавлении запросов
 */
treeUsedQueries.on('beforenodedrop', function(o){

    queryModel.add(o.dropNode.id);

    return false;
});

/**
 * Хэндлер добавления запроса
 */
function onAddParam(){
	var node = treeQueriesParams.getSelectionModel().getSelectedNode();

    // Второе условие означает, что можно добавлять параметры, но не сам запрос.
	if (node && node.parentNode !== treeQueriesParams.getRootNode()) {
		paramModel.openParamWindow(node, true);
	}
}

/**
 * Хэндлер добавления параметров для проброса
 */
function onForwardParam(){
    paramModel.openParamWindow(null, true);
}

/**
 * Хэндлер редактирования запроса
 */
function onEditParam(){
	var node = treeFormParams.getSelectionModel().getSelectedNode();
    if (node && node.parentNode === treeFormParams.getRootNode()) {
        paramModel.openParamWindow(node, false);
    }
}

/**
 * Хэндлер удаления запроса
 */
function onDeleteParam(){
	var node = treeFormParams.getSelectionModel().getSelectedNode();
    if (node && node.parentNode === treeFormParams.getRootNode()) {
        if (node.childNodes.length){
            paramModel.deleteField(node);
        }
    }
}
/**
 * Класс аналог matchingModel. Отвечает за добавление запросов и их параметров во
 * вкладку подстановка значений.
 */
var substitutionValueModel = new function(){
    var _sections = {};
    return {
        getMatchingNode: function(sectionID, queryID){
            var childNodes = treeSubQueries.getRootNode().childNodes;
            for (var i = 0, count=childNodes.length; i < count; i++){
                if (childNodes[i].attributes['query_id'] === queryID &&
                    childNodes[i].attributes['template_field'] === sectionID){
                    return childNodes[i];
                }
            }
        },
        addParameterIfMatchingExists: function(sectionID, queryID, params){
            var hasMatching = false,
                queries = _sections[sectionID];

            if (queries){

                for (var i = 0, queriesCount=queries.length; i < queriesCount; i++){

                    if (queries[i]['query_id'] === queryID){

                        hasMatching = true;

                        var hasParams = queries[i]['params'].slice();

                        for (var j = 0, paramsCount=params.length; j < paramsCount; j++){
                            var found = false;

                            for (var k = 0, hasParamsCount=hasParams.length; k < hasParamsCount; k++){

                                if (hasParams[k]['query_id'] === params[j]['query_od'] &&
                                    hasParams[k]['template_field'] === params[j]['template_field']){
                                    found = false;
                                    break;
                                }
                            }

                            if (!found){
                                queries[i]['params'].push({
                                    'name': params[j]['name'],
                                    'query_id': params[j]['query_id'],
                                    'template_field': params[j]['template_field']
                                });

                                var subQueryNode = this.getMatchingNode(sectionID, queryID);
                                if (!subQueryNode) {
                                    continue;
                                }

                                subQueryNode.appendChild(new Ext.tree.TreeNode({
                                    'name': params[j]['name'],
                                    'query_id': params[j]['query_id'],
                                    'template_field': params[j]['template_field']
                                }));
                            }
                        }
                    }
                }
            }
            return hasMatching;
        },

        _getMatchingFields: function(node){
            var res = [];
            if (node) {
                for (var i= 0, count=node.length; i<count; i++){
                    res.push({
                        'name': node[i]['name'],
                        'query_id': node[i]['query_id'],
                        'template_field': node[i]['template_field']
                    });
                }
            }
            return res;
        },

        add: function(node){
            if (!node) {
                return;
            }
            var sectionID = node['template_field'],
                queryID =  node['query_id'],
                params = this._getMatchingFields( node['children'] );

            if (this.addParameterIfMatchingExists(sectionID, queryID, params)){
                return;
            }

            var s = _sections[sectionID];
            var o = {
                'query_id': queryID,
                'params': params
            };

            if (s){
                s.push(o);
            } else {
                s = [o];
            }

            _sections[sectionID] = s;

            var rootSubQuery = treeSubQueries.getRootNode();
            var subQueryNode = new Ext.tree.TreeNode(node);

            rootSubQuery.getOwnerTree().getLoader().doPreload(subQueryNode);
            if(subQueryNode){
                rootSubQuery.appendChild(subQueryNode);
            }

            rootSubQuery.loaded = true;
        },

        remove: function(sectionID, queryID, queryFieldID, templateField){

            var sectionData = _sections[sectionID];
            for (var i=sectionData.length-1;  i>=0; i--){

                var query=sectionData[i]['query_id'];

                if (query === queryID){
                    var params=sectionData[i]['params'];
                    for (var j=params.length-1; j>=0; j--){

                        var field=params[j]['query_id'],
                            template=params[j]['template_field'];

                        if (queryFieldID === field && templateField === template){
                            params.splice(j, 1); // Удаляем элемент сопоставления
                            break;
                        }
                    }
                    // Если сопоставлений больше нет - удаляем и запрос
                    if (!params.length){
                        sectionData.splice(i, 1);
                    }
                    break;
                }
            }
        },

        removeForQueryTree: function(queryID){

            for (var obj in _sections){
                 for (var i = 0; i < _sections[obj].length; i++){
                      if (_sections[obj][i]['query_id'] == queryID){
                          _sections[obj].splice(i, 1);
                      }
                 }
            }

            var rmvNodes = treeSubQueries.getRootNode().findChild('query_id', queryID);
            if (rmvNodes){
                rmvNodes.remove();
            }
        }
    }
};

/**
 * Класс-модель, отвечабщая за сопоставление параметров внутри секций с данными 
 * имеющихся в отчете select-полей
 */
var matchingModel = new function(){
    /**Объект "секция"
     *   {sectionID: { // sectionID - идентификатор секции
     *      query_id: queryID, // идентификатор запроса
     *      params: [ {
     *          query_field: "Название поля в запросе",
     *          query_field_id: "Идентификатор поля в запросе",
     *          template_field: "Идентификатор-название параметра в секции"
     *      },.. ]   
     *   }}
     * 
     */
	var _sections = {};	

	return {
		/**
		 * Возвращает узел дерева treeMatchingFields сопоставления уровня
		 * секций и запросов  
		 */
		getMatchingNode: function(sectionID, queryID){
			var childNodes = treeMatchingFields.getRootNode().childNodes;
			for (var i=0; i<childNodes.length; i++){
				if (childNodes[i].attributes['query_field_id'] === queryID &&
				    childNodes[i].attributes['template_field'] === sectionID){
					return childNodes[i];
				}
			}
		},
		/**
		 * Проверяет и добавляет параметры если их нет. Возвращает true, если параметры были
		 * добавлены и сопоставления есть.
		 */
		addParameterIfMatchingExists: function(sectionID, queryID, params){
			
			// Сопоставлена ли секция с запросом
			var hasMatching = false;
              
            var queries = _sections[sectionID];

            if (queries){
                // Получаем все запросы секции

                for (var i=0; i<queries.length; i++ ){
                    
                    // Получаем запрос
                    if (queries[i]['query_id'] === queryID){
                        hasMatching = true;
                        
                        // Получаем все параметры, которые уже есть
                        var hasParams = queries[i]['params'].slice();
                        var found;
                        
                        for (var z=0; z<params.length; z++){
                            found = false;
                            for (var j=0; j<hasParams.length; j++){ 
                                // Если данный параметр уже есть, вставлять его не нужно
                                if (hasParams[j]['query_id'] === params[z]['query_id'] &&
                                    hasParams[j]['template_field'] === params[z]['template_field'] ){
                                    
                                    found = true;
                                    break;
                                }
                            }

                            if (!found){
                                    // Добавляем сопоставления, если нет в списке
                                    queries[i]['params'].push({
                                        'name': params[z]['name'],
                                        'query_id': params[z]['query_id'],
                                        'template_field': params[z]['template_field']
                                });
                                
                                // Нужно добавить параметры и как узлы:
                                var matchingNode = this.getMatchingNode(sectionID, queryID);
                                if (!matchingNode) {
                                    continue;
                                }
                                assert(matchingNode, 'Не найден узел сопоставлений');
                                
                                matchingNode.appendChild(new Ext.tree.TreeNode({
                                   'name': params[z]['name'],
                                   'query_id': params[z]['query_id'],
                                   'template_field': params[z]['template_field']
                                }));
                                
                            }
                        }
                    }
               }
            }
            return hasMatching;
		},
		
		/**
		 * Добавление согласованной секции 
		 */		
		add: function(node){

            var sectionID = node['template_field'], // Добавляемая в сопоставления секция
			    queryID =  node['query_id'], // Добавляемый в сопоставления запрос
			    params = this._getMatchingFields( node['children'] ); // Параметры сопоставления]

			if (this.addParameterIfMatchingExists(sectionID, queryID, params)){
				return;
			}
			
			var s = _sections[sectionID];		
			var o = {
				'query_id': queryID,
				'params': params
			};

			if (s){
				s.push(o);
			} else {
				s = [o];
			}

			_sections[sectionID] = s;
			
        	var rootMatchingQuery = treeMatchingFields.getRootNode();
			var matchingNode = new Ext.tree.TreeNode(node);

		    rootMatchingQuery.getOwnerTree().getLoader().doPreload(matchingNode);
		    if(matchingNode){
		        rootMatchingQuery.appendChild(matchingNode);
		    }

			rootMatchingQuery.loaded = true;
		},

		/**
		 * Возвращает список сопоставленных полей запроса с параметрами секции
		 * @param nodes: список дочерних узлов для дерева treeMatchingFields
		 */
		_getMatchingFields: function(node){
			var res = [];
            if (node) {
                for (var i=0; i<node.length; i++){
                    res.push({
                        'name': node[i]['name'],
                        'query_id': node[i]['query_id'],
                        'template_field': node[i]['template_field']
                    });
                }
            }
			return res;
		},
		/**
		 * Возвращение всех запросов по id секции
		 * @param sectionID: Идентификатор секции
		 */
		getQueries: function(sectionID){
			return _sections[sectionID];
		},
		/**
		 * Удаление всех узлов сопоставлений
		 */
		removeAll: function(){
			_sections = {};
			treeMatchingFields.getRootNode().removeAll();
		},
		/**
		 * Удаление конкретного сопоставления
		 */
		remove: function(sectionID, queryID, queryFieldID, templateField){

			var sectionData = _sections[sectionID];			
			for (var i=sectionData.length-1;  i>=0; i--){			
				
				var query=sectionData[i]['query_id'];
				
				if (query === queryID){
					var params=sectionData[i]['params'];
					for (var j=params.length-1; j>=0; j--){
						
						var field=params[j]['query_id'],
						  template=params[j]['template_field'];
							
						if (queryFieldID === field && templateField === template){
							params.splice(j, 1); // Удаляем элемент сопоставления
							break;
						}
					}
					// Если сопоставлений больше нет - удаляем и запрос
					if (!params.length){						
						sectionData.splice(i, 1);
					}
					break;
				}
			}
		},
        /**
         * Вызывается для удаления из дерева "Cопоставление запросов и секций в отчете"
         * при удалении из дерева "Cекции отчета".
         * @param sectionID
         * @param templateField
         * @param isLeaf является ли удаляемый из дерева узел листом
         */
        removeForSectionTree: function(sectionID){
            var sectionData = _sections[sectionID];
            if (sectionData){

                delete _sections[sectionID];

                // Находим и удаляем запись, с данной секцией, из дерева совоставлений.
                var rmvNode = treeMatchingFields.getRootNode().findChild('template_field', sectionID);
                if (rmvNode){
                    rmvNode.remove();
                }
            }
        },

        removeForQueryTree: function(queryID){

            // Индекс удаляемого элемента.
            var deleteIndex,
                ind;
            for (var obj in _sections){
                 ind = -1;
                 for (var i = 0; i < _sections[obj].length; i++){
                      if (_sections[obj][i]['query_id'] == queryID){
                          ind = i;
                          break;
                      }
                 }
                 if (ind != -1){
                     _sections[obj].splice(ind, 1);
                 }
            }

            var rmvNode = treeMatchingFields.getRootNode().findChild('query_id', queryID);
            if (rmvNode){
                rmvNode.remove();
            }
        }
	}
};

/**
 * Устанавливает сопоставления между полями в запросе и полями в шаблоне
 */
function onMatchFields(){

	var selectedQueryRow = treeUsedQueries.getSelectionModel().getSelectedNode(),
		selectedTemplateRow =  treeUsedSections.getSelectionModel().getSelectedNode();
		
	if (!selectedQueryRow || !selectedTemplateRow || 
		selectedQueryRow.parentNode != treeUsedQueries.getRootNode()){
			return;
	}

	var query = queryModel.getQueryForSelect(selectedQueryRow.attributes.query_id);
	var section = sectionModel.getSectionNode(selectedTemplateRow.attributes['template_field']);

	var loadMask = new Ext.LoadMask(panel.body);
    loadMask.show();
    
    // Показ окна для сопоставления полей между полями запроса и параметрами секции
	Ext.Ajax.request({
        url: '{{component.params.matching_url}}'
        ,params: panel.actionContextJson || {}
        ,success: function(response){
            loadMask.hide();
            var childWin = smart_eval(response.responseText);

            childWin.fireEvent('loadData', query, section);
            childWin.on('selectData', function(cfgNode){
            	matchingModel.add(cfgNode);
            });
            childWin.on('selectDataForSubstitution', function(cfgNode){
                substitutionValueModel.add(cfgNode);
            });
		}
		,failure: function(){
        	loadMask.hide();
            uiAjaxFailMessage.apply(this, arguments);
        }
	});	
}

/**
 * Убрать сопоставление для полей запроса и параметров секции
 */
function onUnMatchFields(){
	var selNode = treeMatchingFields.getSelectionModel().getSelectedNode();
//        children = treeSubQueries.getRootNode().childNodes[0].attributes.children,
    var subTreeNodes = selNode.parentNode.childNodes,
        subTreeNode = new Ext.tree.TreeNode,
        i;
//    if (!children) {
//        return;
//    }
    var len = subTreeNodes.length,
        tree_len = treeSubQueries.getRootNode().childNodes.length;

    if (!selNode) {
        return;
    }



    for (i = 0; i < len; i++){
        if ((subTreeNodes[i].attributes['name'] == selNode.attributes['name'])
            && (subTreeNodes[i].attributes['query_id']==selNode.attributes['query_id'])
            && (subTreeNodes[i].attributes['template_field']==selNode.attributes['template_field'])){
            subTreeNode = subTreeNodes[i];
            break;
        }
    }

	if (selNode){
		
		var queryID = null,
			sectionID = null,
			queryFieldID = null,
			templateField = null;
		
		if (selNode.isLeaf()){ // Сопоставленные элементы секций и запросов
			var parent = selNode.parentNode;
            var subParent = subTreeNode.parentNode;

            var range = gridQuery.getStore().getRange();

            for (i = 0, len = range.length; i < len; i++){
                if ((range[i].data['name'] == selNode.attributes['name'])
                && (range[i].data['query_id'] == selNode.attributes['query_id'])){
                    gridQuery.getStore().remove( range[i] );
                }
            }
			
			queryID = parent.attributes['query_id'];
			sectionID = parent.attributes['template_field'];
			queryFieldID = selNode.attributes['query_id'];
			templateField = selNode.attributes['template_field'];
			
			matchingModel.remove(sectionID, queryID, queryFieldID, templateField);
            substitutionValueModel.remove(sectionID, queryID, queryFieldID, templateField);
									
			if (parent.childNodes.length === 1){ // Остался единственный элемент, удаляем так же родителя
				parent.remove();
                subParent.remove();
			} else {
				selNode.remove();
                subTreeNode.remove();
			}
			
		} else { // Сопоставленные секции и запросы
			
			queryID = selNode.attributes['query_id'];
			sectionID = selNode.attributes['template_field'];
			
			var childNodes = selNode.childNodes,
                childsCount = childNodes.length,
				node;

			for (i=0; i<childsCount; i++){
				node = childNodes[i];
					
				queryFieldID = node.attributes['query_id'];
				templateField = node.attributes['template_field'];
				
				matchingModel.remove(sectionID, queryID, queryFieldID, templateField);
                substitutionValueModel.remove(sectionID, queryID, queryFieldID, templateField);
			}
			selNode.remove();
            subTreeNode.remove();
		}
	}
}

/**
 * Возвращает список сопоставленных секций и запросов
 * Использует алгоритм обхода дерева в ширину.
 */
function getMatchingFields(){

    var res=[],

        nodes = treeUsedSections.getRootNode().childNodes,
        count = nodes.length;

    for (var i = 0; i < count; i++){

        // Очередь для работы с деревьями
        var queue = [],
            sec = { 'section': nodes[i], 'visit': false },
            sectionID = sec['section'].attributes['section'];

        var query = null,
            queryID = null,
            queryName = "";
        var q1 = matchingModel.getQueries(sectionID);
        if (q1) {
            query = q1[0];
            queryID = query.query_id;
            if (queryID){
                queryName = queryModel.getQueryForSelect(queryID).name;
            }
        }

        queue.push(sec);

        // Компоненты дерева секций, которые будут переданы на сервер для сохранения
        var toServerTreeNode = {
                'section': sectionID,
                'type_output': sec['section'].attributes['type_output'],
                'priority_output': sec['section'].attributes['priority_output'],
                // TODO для каждой секции один запрос.
                'query': query,
                'name': queryName,
                'query_id': queryID,
                'sub_sections': []},
            toServerQueue = [];
        toServerQueue.push(toServerTreeNode);

        // Вершина дерева запросов
        var toServerTree = toServerTreeNode;
        while (queue.length){
            
            sec = queue.shift();
            toServerTreeNode = toServerQueue.shift();
            
            if (!sec['visit']){
                sec['visit'] = true;

                var childs = sec['section'].childNodes;
                for (var j = 0; j < childs.length; j++){
                    var sub_sec = { 'section': childs[j], 'visit': false };
                    queue.push(sub_sec);

                    sectionID = sub_sec['section'].attributes['section'];
                    query = matchingModel.getQueries(sectionID)[0];
                    queryID = query.query_id;
                    queryName = queryModel.getQueryForSelect(queryID).name;

                    var toServerTreeChildNode = {
                        'section': sectionID,
                        'type_output': sub_sec['section'].attributes['type_output'],
                        'priority_output': sub_sec['section'].attributes['priority_output'],
                        'query': query,
                        'name': queryName,
                        'query_id': queryID,
                        'sub_sections': []
                    };
                    toServerTreeNode['sub_sections'].push(toServerTreeChildNode);
                    toServerQueue.push(toServerTreeChildNode);
                }
            }
        }
        res.push(toServerTree);
    }
    
	return res;
}

/**
 * Возвращает список используемых запросов в отчете 
 */
function getQueries(){

	var res = [],
	    queries = queryModel.getQueries(),
	    params = paramModel.getFieldsParams();
	
	for (var i=0; i<queries.length; i++){
	   res.push({
	       'query_id': queries[i],
	       'params': paramModel.getParamsByQuery(queries[i])
	   });
	}	
	return res;	      
}

function getSubstitutionValueObject()
{
    var res = [],
        range = gridQuery.getStore().getRange();
    for (var i = 0; i < range.length; i++)
    {
        res.push(range[i].data);
    }
    return res;
}

/**
 * Функция валидации, возвращает true, если все нормально. Возвращает false 
 * если есть проблемы
 */
function validate(){
	/**
	 * Все запросы, добавленные в дерево "Запросы/словари отчета" должны быть
     * также в дереве "Сопоставление запросов и секций в отчете.
	 * @return {Boolean} Результат проверки
	 */
	function checkQueries(){

        var allUserQueriesUsed = true,

        // Запросы, которые используются в отчете.
            userQueries = treeUsedQueries.getRootNode().childNodes,
            i, len = userQueries.length;

        for (i = 0; i < len; i++){
            if (!treeMatchingFields.getRootNode().findChild('query_id', userQueries[i].attributes['query_id'])){
                allUserQueriesUsed = false;
                break;
            }
        }

        return allUserQueriesUsed;
	}
    function checkParams(){
        var childNodes = treeQueriesParams.getRootNode().childNodes;        
        for (var i=0; i<childNodes.length; i++){
            if (childNodes[i].childNodes.length > 0 ){
                return false;
            }
        }
        return true;
    }

    function checkSections(){

        // Пробегаем по дереву секций и для каждого узла проверяем его наличие в дереве сопоставлений с запросами
        // Для пробега используем алгоритм обхода дерева в ширину
        var sections = treeUsedSections.getRootNode().childNodes,
            count    = sections.length,
            // Все ли секции сопоставлены.
            allSectionMatching = true;
        for (var i = 0; i < count; i++){

            // Формируем узел для прогулки по дереву секций
            // 'section' - здесь храним информацию о секции
            // 'visit' - флаг, который указывает посещали ли мы узел
            var node = { 'section': sections[i], 'visit': false },
                // Очередь для прогулки по дереву
                queue = [node];

            while (queue.length){

                node = queue.shift();

                if (!node['visit']){
                    node['visit'] = true;

                    // Здесь проверяем наличие секции в дереве сопоставлений
                    if (!treeMatchingFields.getRootNode().findChild('template_field', node['section'].attributes['template_field'])){
                        allSectionMatching = false;
                        break;
                    }

                    for (var j = 0; j < node['section'].childNodes.length; j++){
                        var childNode = {'section': node['section'].childNodes[j], 'visit': false};
                        queue.push(childNode);
                    }
                }

            }

            if (!allSectionMatching){
                break;
            }

        }

        return allSectionMatching;
    }

    function checkMatchingFields(){

        var nodes = treeMatchingFields.getRootNode().childNodes,
            count = nodes.length;

        // Флаг, который показывает, что одной секции соответствует один запрос
        var oneSectionOneQuery = true;
        for (var i = 0; i < count; i++){
            var section = nodes[i].attributes['template_field'];

            for (var j = i + 1; j < count; j++){
                if (section === nodes[j].attributes['template_field']){
                    oneSectionOneQuery = false;
                    break;
                }
            }

            if (!oneSectionOneQuery){
                break;
            }

        }

        return oneSectionOneQuery;
    }
	
	var basicForm = frmMain.getForm(),
	   result = true,
	   messages = [],
	
	   messageObject = {
            title:'Внимание',            
            buttons: Ext.Msg.OK,
            animEl: 'elId',
            icon: Ext.MessageBox.INFO
        };
	
    if (!basicForm.isValid()){
    	result = false;
    	messages.push('Не все обязательные поля заполнены');                
    }
    if (!checkMatchingFields()){
        result = false;
        messages.push('В отчете присутствуют секции, которые сопоставлены с несколькими запросами');
    }
    if (!checkQueries()){
        result = false;
        messages.push('Не все запросы сопоставлены с секциями');
    }
    if (!checkParams()){
        result = false;
        messages.push('Не все параметры соотносены с полями на форме');
    }
//    if (!checkSections()){
//        result = false;
//        messages.push('Не все секции сопоставлены с запросами');
//    }
    
	if (!result){		
		Ext.Msg.show( Ext.apply(messageObject, {msg: messages.join('<br/>')}) );
	}
    
    return result;
}

function checkSubValue(){
    var range = gridQuery.getStore().getRange();
    for (var i = 0; i < range.length; i++){
        if ((range[i].data['condition'] != 'eq' && range[i].data['condition'] != 'ne')
            && (range[i].data['result'].toLowerCase() == 'false' || range[i].data['result'].toLowerCase() == 'true')){
            Ext.Msg.show({
                title: 'Ошибка в подстановке значений',
                msg: 'Результаты TRUE и FALSE не могут сочитаться с условиями(<=, >=, <, >)',
                buttons: Ext.Msg.OK
            });
            return false;
        }
    }
    return true;
}

/**
 * Обработчик на сохранение отчета
 */
function onSave(){

    if (!checkSubValue()){
       return;
    }

	if (!validate()){
        return;
    }

	var loadMask = new Ext.LoadMask(panel.body);
	loadMask.show();

	frmMain.getForm().submit({
		params: {
			// Поля для построения формы с параметрами
			'form_params': Ext.encode(paramModel.getFieldsParams()),
			
			// Используемые запросы и их параметры
			'queries_params': Ext.encode(getQueries()),
			
			// Используемые секции шаблона с сопоставленными полями
			'sections':  Ext.encode(getMatchingFields()),

            // Значения подстановки для параметра
            'subs_values': Ext.encode(getSubstitutionValueObject())
		},
		success: function(form, action){
            panel.setTitle(strName.getValue());
            // Если объект был новым и успешно сохранился, то проставляем ему
            // айди
            var responseText = action.response.responseText;
            if(responseText.substring(0,1) == '{'){
                // это у нас json объект
                var responseData = Ext.util.JSON.decode(responseText);
                if (typeof responseData.id !== 'undefined'){
                    hdnId.setValue(responseData.id);
                }
            }
            loadMask.hide();
		},
		failure: function(){
			loadMask.hide();
			uiAjaxFailMessage.apply(this, arguments);
		}			
	});
}

gridQuery.on('afterrender', function(){
    var fieldsDropTargetEl = gridQuery.getView().scroller.dom;
    var selectFieldsDropTarget = new Ext.dd.DropTarget(fieldsDropTargetEl, {
        ddGroup    : 'TreeDD',
        notifyDrop : function(ddSource, e, data){
            openSubstitutionValueWindow(data.node.attributes, false);
        }
    });
});

function addSubstitutionValue(){
    var node = treeSubQueries.getSelectionModel().getSelectedNode();
    if (node){
        openSubstitutionValueWindow(node.attributes, false);
    }
}

function delSubstitutionValue(){
    deleteField(gridQuery);
}

function onEditSubstitutionValue(){
    var record = gridQuery.getSelectionModel().getSelected(),
        obj = {};

    obj['name'] = record.data['verboseName'];
    obj['id'] = record.id;

    Ext.apply(obj, record.data);

    openSubstitutionValueWindow(obj, true);
}

function openSubstitutionValueWindow(rec, edit){

    var loadMask = new Ext.LoadMask(panel.body);
    loadMask.show();

    Ext.Ajax.request({
        url: '{{ component.params.subst_url }}',
        params: panel.actionContextJson || {},
        success: function(response){

            var fieldName = rec['name'],
                queryID = rec['query_id'],
                result, subst_value, condition;

            loadMask.hide();
            var childWin = smart_eval(response.responseText);
            if (edit){
                result = rec['result'];
                subst_value = rec['subst_value'];
                condition = rec['condition'];
            }

            childWin.fireEvent('loadData', {
                'name': fieldName,
                'result': result,
                'subst_value': subst_value,
                'condition': condition
            });

            childWin.on('selectData', function(obj){
                var store = gridQuery.getStore(),
                    record;

                if (edit){
                    record = store.getById(rec['id']);
                } else {
                    record = new Ext.data.Record();
                }

                record.id = obj['result'] + obj['conditionID'] + obj['substValue'];
                record.data['verboseName'] = fieldName;
                record.data['condition'] = obj['conditionID'];
                record.data['result'] = obj['result'];
                record.data['subst_value'] = obj['substValue'];
                record.data['expression'] = String.format('{0} {1} {2} {3} {4} {5}',
                    'Если ',
                    fieldName, obj['condition'], obj['result'], ', то заменяем на',
                    obj['substValue']);
                record.data['query_id'] = queryID;

                if (edit){
                    record.commit();
                }else{
                    store.add(record);
                }

            });
        },
        failure: function(){
            loadMask.hide();
            uiAjaxFailMessage.apply(this, arguments)
        }

    });
}

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

/*
 * Обход дерева и выполнение действия на узле
 */
var actionOnTree = function(element, subElementKey, action){

    var node = {'element': element, 'visit': false},
        queue = [node];

    while (queue.length){

        node = queue.shift();

        if (!node['visit']){
            node['visit'] = true;

            action(node['element']);

            var subElements = node['element'][subElementKey],
                childNode;
            for (var j= 0, len=subElements.length; j < len; j++){
                childNode = {'element': subElements[j], 'visit': false};
                queue.push(childNode);
            }
        }
    }
};

// Устанавливаем hot-key ctrl+shift+m. При нажатие поле текст ключа становится активным (в том случае, если это
// редактирование, т.к. при создании нового отчета оно активно всегда).
var map = new Ext.KeyMap(document, {
    key: "m",
    ctrl: true,
    shift: true,
    fn: function(){
        if (editMode) {
            reportKeyField.setReadOnly(!reportKeyField.readOnly);
        }
    }
});


// Вставка значений в режиме редактирования
if (editMode) {

	var i = 0,
        templateName = '{{ component.template_name }}';

    //TODO можно написать регулярное выражение
    //Для решения проблемы с C:\fakepath\имя_шаблона
    templateUploadField.setValue(templateName.replace('&quot;', '').replace('&quot;', ''));

	// Вставка всех секций
	var sections = Ext.decode('{{ component.sections_all|safe }}');	
	allSections.addNodes(sections);
	
	// Вставка выведенных секций
	var reportSections = Ext.decode('{{ component.sections_report|safe }}');
    sectionModel.loadSectionsTree(reportSections);


	var paramsData = Ext.decode('{{ component.all_params|safe }}');
	for (i=0; i<paramsData.length; i++){
		queryModel.loadParamsNodes(paramsData[i]);
	}

	var selectData  = Ext.decode('{{ component.select_data|safe }}');
    for (i=0; i<selectData.length; i++){
        queryModel.loadSelectNodes(selectData[i]);
    }

	var matchingFields = Ext.decode('{{ component.matching_fields|safe }}');
	for (i=0; i<matchingFields.length; i++){
		matchingModel.add(matchingFields[i]);
        substitutionValueModel.add(matchingFields[i]);
	}

    var substitutionValueGrid = Ext.decode('{{ component.subs_values|safe }}');
	for (i = 0; i < substitutionValueGrid.length; i++){
        var record = new Ext.data.Record();
        Ext.apply(record.data, substitutionValueGrid[i]);
        gridQuery.getStore().add(record);
    }

	var formFields = Ext.decode('{{ component.form_fields|safe }}');
	var queryParams = Ext.decode('{{ component.model_query_params|safe }}');
	var formParams = Ext.decode('{{ component.model_form_params|safe }}');
	paramModel.setData(formFields, queryParams, formParams);

    // При редактировании делаем поле ключ отчета недоступным для записи.
    // Его можно активировать комбинацией клавиш ctrl+shift+m.
    reportKeyField.setReadOnly(true);
}

