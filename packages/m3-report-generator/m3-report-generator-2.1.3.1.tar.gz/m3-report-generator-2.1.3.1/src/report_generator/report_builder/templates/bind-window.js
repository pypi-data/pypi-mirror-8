/**
 * Created by PyCharm.
 * User: Игорь
 * Date: 22.03.12
 * Time: 14:21
 * To change this template use File | Settings | File Templates.
 */

var cmbParentFields = Ext.getCmp('{{ component.cmb_parent_fields.client_id }}'),
    cmbChildFields  = Ext.getCmp('{{ component.cmb_child_fields.client_id }}');

win.on('loadData', function(o){
    cmbParentFields.getStore().loadData(o.parent_query);
    cmbChildFields.getStore().loadData(o.child_query);
});

function bindQueries(){

    var parent_field = cmbParentFields.getValue(),
        child_field = cmbChildFields.getValue();

    // Пользователь не выбрал поля для связывания запросов.
    if (!parent_field || !child_field){
        Ext.Msg.show({
            title: 'Внимание',
            msg: 'Выберите поля для связи запросов',
            buttons: Ext.Msg.OK
        });
        return;
    }

    // Выбранные поля для связи запросов
    var choicesFields = {
        'parent_field': cmbParentFields.getValue(),
        'child_field': cmbChildFields.getValue()
    };

    win.fireEvent('selectData', choicesFields);
    win.close();
}