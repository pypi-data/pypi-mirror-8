/**
 * Created by PyCharm.
 * User: prefer
 * Date: 08.04.12
 * Time: 15:05
 * To change this template use File | Settings | File Templates.
 */

var strName = Ext.getCmp('{{component.str_name.client_id}}');

win.on('loadData', function(data){
    strName.setValue(data['name']);
});
