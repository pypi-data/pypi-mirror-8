
var treePermissions = Ext.getCmp('{{ component.tree.client_id }}'),
    form = Ext.getCmp('{{ component.client_id }}'),
    CONTROLLER_TYPE = '{{ component.CONTROLLER_TYPE }}',
    cmbMetaroles = Ext.getCmp('{{ component.field_metarole.client_id }}'),
    role_name = Ext.getCmp('{{ component.field_name.client_id }}'),
    grid = Ext.getCmp('{{ component.grid.client_id }}');
var oldValue;

function getJsonOfStore(store){
    var datar = new Array();
    var records = store.getRange();
    for (var i = 0; i < records.length; i++) {
        datar.push(records[i].data);
    }
    return Ext.util.JSON.encode(datar);
}

form.on('beforesubmit', function beforeSubmit(submit){
    if (grid){
        var store = grid.getStore();
        var res = getJsonOfStore(store);
        submit.params.perms = res;
    }
    return true;
});

function loadPermissionTree(metarole){
    var loader = treePermissions.getLoader();
    loader.baseParams['metarole'] = metarole;

    var rootNode = treePermissions.getRootNode();
    loader.load(rootNode);
    rootNode.expand();
}


/*
Показываем права при редактировании роли
 */
form.on('show', function(){
   if (cmbMetaroles.getValue()){
       loadPermissionTree(cmbMetaroles.getValue());
   }
});

/*
 Запомним текущую метароль для возможности отмены её изменения
 */
cmbMetaroles.on('focus', function(cmp){
    oldValue = cmbMetaroles.getValue();
});

/*
Показываем для каждой метароли свои паки экшены и контроллеры
 */
cmbMetaroles.on('select', function(cmp, record, index){
    if(oldValue) {
        var url = '{{ component.del_all_permission_url }}';
        var result = confirm('Изменение метароли приведет к немедленной утере всех ранее заданных разрешений для роли. Продолжить?');
        if(result) {
            Ext.Ajax.request({
                url: url,
                params: win.actionContextJson,
                success: function(response, opt){
                    smart_eval(response.responseText);
                    loadPermissionTree(record.id);
                },
                failure: function(){
                    cmbMetaroles.setValue(oldValue);
                    loadMask.hide();
                    uiAjaxFailMessage.apply(this, arguments);
                }
            });
        } else {
            cmbMetaroles.setValue(oldValue);
        }
    } else {
        loadPermissionTree(record.id);
    }
    oldValue = cmbMetaroles.getValue();
});

/*
Обработавем удаление метароли
 */
cmbMetaroles.on('change', function(cmp, value, oldValue){
//    console.log(value);
    if (!value){
        loadPermissionTree(value);
    }
});


/**
 * Редактирование права
 */
treePermissions.on('dblclick', function(node, e){

    if (node.attributes['type'] === CONTROLLER_TYPE){
        return;
    }

    var url = '{{ component.edit_permission_url }}';
    assert(url, 'Url is not define');

    var loadMask = new Ext.LoadMask(win.body);
    loadMask.show();
    Ext.Ajax.request({
        url: url
        ,params:  Ext.applyIf({
            'name': node.attributes['name'],
            'type': node.attributes['type'],
            'class_name': node.attributes['class_name'],
            'sub_permissions': node.attributes['sub_permissions'],
            'userrole_name': role_name.getValue(),
            'userrole_metarole': cmbMetaroles.getValue()
        }, win.actionContextJson || {})
        ,success: function(response, opt){
            loadMask.hide();

            var childWin = smart_eval(response.responseText);
            childWin.on('close', function(){
                if (cmbMetaroles.getValue()){
                    loadPermissionTree(cmbMetaroles.getValue());
                }
            });
            childWin.on('closed_ok', function(value){
                if(!win.actionContextJson.userrole_id && childWin.actionContextJson.userrole_id){
                    win.actionContextJson.userrole_id = childWin.actionContextJson.userrole_id;
                }
                childWin.actionContextJson['perms'] = Ext.encode(value);
                Ext.Ajax.request({
                    url: childWin.formUrl,
                    params: childWin.actionContextJson,
                    success: function(response, opt){
                        smart_eval(response.responseText);
                    },
                    failure: function(){
                        loadMask.hide();
                        uiAjaxFailMessage.apply(this, arguments);
                    }
                })
            });
            childWin.fireEvent('loadData', {
                name: node.attributes['name']
            });
//            childWin.on('selectData', function(values){
//
//                // Если проверка не проходит, обработка заканчивается
//                if(!this.checkPriority(data['sectionID'],
//                    values['priorityOutput'])){
//                    return;
//                }
//
//                if (newSection){
//                    sectionModel.addSection(data['sectionID'],
//                        values['typeOutput'],
//                        values['priorityOutput']);
//                } else {
//                    sectionModel.editSection(data['sectionID'],
//                        values['typeOutput'],
//                        values['priorityOutput']);
//                }
//
//            }, this);

        }
        ,failure: function(){
            loadMask.hide();
            uiAjaxFailMessage.apply(this, arguments);
        }
        ,scope: this
    });

});

