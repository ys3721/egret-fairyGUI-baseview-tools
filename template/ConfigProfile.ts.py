<?py # -*- coding: utf-8 -*- ?>
module ProfileData {
export interface ${moduName}VO{
    key:number;
    <?py for item in propertys: ?>
/**
 * ${item["info"].replace("\n","\n*")}
 */
        <?py if item["type"] =="int" or "Float"==item["type"] or "long" ==item["type"]  or item["type"] =="float": ?>
    ${item["key"]}:number;
        <?py elif item["type"] =="string": ?>
    ${item["key"]}:string;
        <?py elif item["type"] =="array": ?>
    ${item["key"]}:Array<any>;
        <?py else: ?>
    ${item["key"]}:any;
        <?py #endif ?>
    <?py #endfor ?>
}
export class ${moduName} extends Cfg2ProfileBase{
protected loadData():void{
    this.loadJson("${moduName}");
}
public getAllData():${moduName}VO[]{
  return super.getAllData();
}
protected convertTable(key):${moduName}VO{
    let rowdata = this.cfgData[key];
    if (rowdata){
        let vo:any = {};
        vo.key = key;
    <?py for item in propertys: ?>
        <?py if item["luaindex"] ==0: ?>
        vo.${item["key"]}=key;
        <?py else: ?>
            <?py if item["type"] =="int" or "long" ==item["type"] or item["type"] =="float": ?>
        vo.${item["key"]}=rowdata[${item["luaindex"]-1}];
            <?py elif item["type"] =="string" : ?>
                    <?py if item["lang"] ==1 : ?>
        vo.${item["key"]}=Lang.getLang(rowdata[${item["luaindex"]-1}]) ;
                    <?py else: ?>
        vo.${item["key"]}=rowdata[${item["luaindex"]-1}];
                    <?py #endif ?>
            <?py else: ?>
        vo.${item["key"]}=rowdata[${item["luaindex"]-1}];
            <?py #endif ?>
        <?py #endif ?>
    <?py #endfor ?>
        return vo;
    }
    else{
        return null;
    }
}


//获取整行数据
public getRowData(beanId:number):${moduName}VO{
    return this.convertTable(beanId);
}
<?py for item in propertys: ?>
/**
 * ${item["info"].replace("\n","\n*")}
 */
<?py if item["type"] =="int" or "long" ==item["type"] or item["type"] =="float": ?>
public get${item["name"]}(beanId:number):number{
<?py elif item["type"] =="array": ?>
public get${item["name"]}(beanId:number):Array<any>{
<?py elif item["type"] =="string": ?>
public get${item["name"]}(beanId:number):string{
<?py else: ?>
public get${item["name"]}(beanId:number):any{
<?py #endif ?>
    <?py if item["luaindex"] ==0: ?>
    return beanId
    <?py else: ?>
    let rowdata:Array<any> = this.cfgData[beanId];
    if (rowdata){
        <?py if item["type"] =="string" : ?>
            <?py if item["lang"] ==1 : ?>
        return Lang.getLang(rowdata[${item["luaindex"]-1}]);
            <?py else: ?>
        return rowdata[${item["luaindex"]-1}];
            <?py #endif ?>
        <?py else: ?>
        return rowdata[${item["luaindex"]-1}];
        <?py #endif ?>
    } 
    <?py if item["type"] =="string" : ?>
    return "";
    <?py elif item["type"] =="array": ?>
    return null;
    <?py else: ?>
    return 0;
    <?py #endif ?>
    <?py #endif ?>
}
<?py #endfor ?>
}
}