
var condField = Ext.getCmp('{{ component.str_item.client_id }}'),
	condParam = Ext.getCmp('{{ component.str_param.client_id }}'),
	cmbCondition = Ext.getCmp('{{ component.cmb_simple_cond.client_id }}'),
    cmbConnector = Ext.getCmp('{{ component.cmb_connector.client_id }}'),
    cmbParamType = Ext.getCmp('{{ component.cmb_param_type.client_id }}'),
    strParam = Ext.getCmp('{{ component.str_param.client_id }}'),
    cmbFieldParam = Ext.getCmp('{{ component.cmb_field_param.client_id }}'),

    valueParam = '{{ component.value_param }}',
    fieldParam = '{{ component.field_param }}',
    constantParam = '{{ component.constant_param }}',

    valueParamText = '{{ component.value_param_str }}',
    fieldParamText = '{{ component.field_param_str }}',
    constantParamText = '{{ component.constant_param_str }}';

win.on('loadData', function(obj){
	condField.setValue(obj['verboseName']);
	condParam.setValue(obj['paramName']);

    var connector = obj['connector'];
    if (connector){
        cmbConnector.setValue(connector);
    }

    var condition = obj['condition'];
    if (condition){
        cmbCondition.setValue(condition)
    }

    // Загружаем данные в комбобокс полей параметров
    loadDataToCmbFieldParam(obj['fields']);

    // Выставление значения в комбобоксе "Тип параметра"
    var paramType = obj['paramType'];
    if (paramType){
        if (paramType == valueParam){
            cmbParamType.setValue(valueParam);
            cmbFieldParam.hide();
            strParam.show();
            strParam.setValue(obj['paramName']);
        } else if (paramType == fieldParam) {
            cmbParamType.setValue(fieldParam);
            cmbFieldParam.show();
            cmbFieldParam.setValue(obj['paramName']);
            strParam.hide();
        } else if (paramType == constantParam) {
            cmbParamType.setValue(constantParam);
            cmbFieldParam.hide();
            strParam.show();
//            strParam.clearValue(true);
        }
    }
});

cmbParamType.on('change', function(cmb, record, indx){
    // В record лежит число
    // В normalParam лежит строка
    // Сравниваю использую ==, чтобы автоматически приводились типы.
    if (record == valueParam){
        strParam.show();
        cmbFieldParam.hide();
    }else if (record == fieldParam) {
        strParam.hide();
        cmbFieldParam.show();
    } else if (record == constantParam) {
        strParam.show();
        strParam.setValue('');
        cmbFieldParam.hide();
    }
});

function selectCondition(){
    // Функция, которая генерирует событие selectData
    // В качестве параметра принимает обьект {param: PARAMETER} для обычных параметров
    // и {field_param: PARAMETER} для параметров-полей.
    var generateSelectDataEvent = function(eventObject){
        // Общие данные для обоих типов параметров
        eventObject['condition']   = cmbCondition.lastSelectionText;
        eventObject['conditionID'] = cmbCondition.getValue();
        eventObject['connector']   = cmbConnector.lastSelectionText;

        win.fireEvent('selectData', eventObject);
        win.close(true);
    };

    // Если данное поле отображено, то пользователь использует обычный параметр.
    if (strParam.isVisible()){
        var paramName = condParam.getValue();
        if (paramName){
            generateSelectDataEvent({
                parameter: condParam.getValue(),
                paramType: cmbParamType.getValue()
            });

        }else{
            Ext.Msg.show({
                title: 'Внимание',
                msg: 'Отсутствует имя параметра',
                buttons: Ext.Msg.OK
            });
        }
    }else{ // В противном случае это поле-параметр
        var selectedValue = cmbFieldParam.getRawValue(),
            store = cmbFieldParam.getStore(),
            selectedRecord = store.find('field', selectedValue),
            entity_type;

        if (selectedRecord){
            entity_type = store.getAt(selectedRecord).data['entity_type'];
            generateSelectDataEvent({field_param: cmbFieldParam.lastSelectionText, entity_type: entity_type});
        }else{
            Ext.Msg.show({
                title: 'Внимание',
                msg: 'Не выбрано поле-параметр',
                buttons: Ext.Msg.OK
            });
        }
    }
}

// Загружаем данные в поле выбора параметра поля.
function loadDataToCmbFieldParam(data){
    var store = cmbFieldParam.getStore(),
        dataCount = data.length,
        record, i;
    for (i = 0; i < dataCount; i++){
        record = new Ext.data.Record();

        record.data['field'] = data[i]['field'];
        record.data['entity_type'] = data[i]['entity_type'];
        record.id = data[i]['id'];

        store.add(record);
    }
}

// Пришлось обработать, т.к. по какой-то причине нельзя было выставить любое, кроме первого, значение
cmbFieldParam.on('select', function(cmb, record){
    cmb.setValue(record.data['field']);
});
