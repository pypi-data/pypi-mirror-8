/* Created by M3 IDE, at 26.10.2011 03:10 */

var frmMain = Ext.getCmp('{{ component.frm_main.client_id }}');

/*
 * Загрузка данных
 */
win.on('loadData', function(data){	
	frmMain.getForm().setValues(data);
});

function onSave(){
	// Генерация события сохранения данных
	if (!frmMain.getForm().isValid()){
	   return;
	}
	
	win.fireEvent('selectData', frmMain.getForm().getValues()); 
	win.close();
}
