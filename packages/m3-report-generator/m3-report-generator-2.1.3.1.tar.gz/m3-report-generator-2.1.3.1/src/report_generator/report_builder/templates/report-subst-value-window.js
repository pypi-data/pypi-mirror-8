/**
 * Created by PyCharm.
 * User: Игорь
 * Date: 23.01.12
 * Time: 14:11
 * To change this template use File | Settings | File Templates.
 */

var condField = Ext.getCmp('{{ component.str_item.client_id }}'),
    condResult = Ext.getCmp('{{ component.str_result.client_id }}'),
    condition = Ext.getCmp('{{ component.cmb_cond.client_id }}'),
    substValue = Ext.getCmp('{{ component.str_subst.client_id }}');

win.on('loadData', function(obj){
    condField.setValue(obj['name']);

    if (obj['result']){
        condResult.setValue(obj['result']);
    }

    if (obj['subst_value']){
        substValue.setValue(obj['subst_value']);
    }

    if (obj['condition']){
        condition.setValue(obj['condition']);
    }

});

function selectCondition(){
    win.fireEvent('selectData', {
        'condition': condition.lastSelectionText,
        'conditionID': condition.getValue(),
        'result': condResult.getValue(),
        'substValue': substValue.getValue()
    });

    win.close(true);
}