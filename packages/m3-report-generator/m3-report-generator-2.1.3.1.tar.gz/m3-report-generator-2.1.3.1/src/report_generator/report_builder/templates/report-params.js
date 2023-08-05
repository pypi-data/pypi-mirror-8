
var
    // На сколько увеличивается
    costHeight = 30,

    // Первоначальное положение окна
    winHeight = win.height,

	chkRequired = Ext.getCmp('{{ component.chk_required.client_id }}'),
	chkMultiChoice = Ext.getCmp('{{ component.chk_multi_choice.client_id }}'),


	comboType = Ext.getCmp('{{ component.cmb_type.client_id }}'),
	comboTypeValue = Ext.getCmp('{{ component.cmb_type_value.client_id }}'),

    strDefaultType = Ext.getCmp('{{ component.str_default_type.client_id }}'),

	frmMain = Ext.getCmp('{{ component.frm_main.client_id }}'),

    typeNumber = '{{ component.type_number }}',
    typeString = '{{ component.type_string }}';


/*
 * Загрузка данных
 */
win.on('loadData', function(obj){
	loadTypeValues(obj['type'], true);
	win.on('loadTypeValues', function(){
	   frmMain.getForm().setValues(obj)
	});

});

/*
 * Сохранение формы
 */
function onSave(){
	var typeValue = comboTypeValue.getValue(),
	    dataLength = comboTypeValue.getStore().data.length;

	if (!frmMain.getForm().isValid() || dataLength && !typeValue){
		return;
	}

    // Проверка валидности для поля типа "число"
    if (frmMain.getForm().getValues()['type'] == typeNumber &&
        isNaN(Number(frmMain.getForm().getValues()['defaultType']))){
        Ext.Msg.show({
            title: 'Внимание',
            msg: 'Для числового типа значение по умолчанию должно быть числом',
            buttons: Ext.Msg.OK
        });
        return;
    }

	// Генерация события сохранения данных
	win.fireEvent('selectData', Ext.apply(frmMain.getForm().getValues(), {
		// Иначе подставляется значение "on"
		'multiChoice': chkMultiChoice.checked,
		'required': chkRequired.checked
	}));

	win.close();
}

function loadTypeValues(typeID, isEdit){
	var url = '{{ component.params.type_value_items_url }}';
    assert(url, 'Url is not define');

    comboTypeValue.clearValue();
    comboTypeValue.getStore().removeAll();

    var loadMask = new Ext.LoadMask(win.body);
    loadMask.show();
    Ext.Ajax.request({
        url: url
        ,scope: this
        ,params: {
        'type': typeID
        }
        ,success: function(response, opt){
            loadMask.hide();
            var json = Ext.decode(response.responseText);

            if (json.success) {
                if (json.data.length){
                    win.setHeight(winHeight + costHeight);
                    strDefaultType.setVisible(false);
                    comboTypeValue.setVisible(true);
                    comboTypeValue.markInvalid();
                    comboTypeValue.getStore().loadData(json.data);
                } else {
                    // Устанавливается невидимость бокса выбора значений типов
                    comboTypeValue.setVisible(false);
                    // Если тип поля "строка" или "число", то появляется поле
                    // значение по-умолчанию
                    if (typeID == typeNumber || typeID == typeString){
                        win.setHeight(winHeight + costHeight);
                        strDefaultType.setVisible(true);
                    }else{
                        win.setHeight(winHeight);
                    }
                }
                if (isEdit) {
                    win.fireEvent('loadTypeValues');
                }
            }
        }
        ,failure: function(){
            loadMask.hide();
            uiAjaxFailMessage.apply(this, arguments);
        }
   });
}

comboType.on('select', function(cmb, record, index){
    loadTypeValues(record.id, false);
});

comboTypeValue.on('select', function(cmb, record, index){
    comboTypeValue.clearInvalid();
});
