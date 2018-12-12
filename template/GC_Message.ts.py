/** This is an automatically generated. Please do not modify it. **/
module network {
<?py for listfunction in listField: ?>
<?py if listfunction["index"]==0: ?>
export interface ${listfunction["type"]}VO{  
    <?py for item in listfunction["fields"]: ?>
        /**
        * ${item["comment"]} 
        */
        <?py if item["type"]=="Long" or item["type"]=="Int" or item["type"]=="Float" or item["type"]=="Short" or item["type"]=="Byte": ?>
        <?py if item["islist"]: ?>
        ${item["name"]}:number[];
        <?py else: ?>
        ${item["name"]}:number;
        <?py #endif ?>
        <?py elif item["type"]=="String": ?>
        <?py if item["islist"]: ?>
        ${item["name"]}:string[];
        <?py else: ?>
        ${item["name"]}:string;
        <?py #endif ?>
        <?py elif item["type"]=="Boolean": ?>
        <?py if item["islist"]: ?>
        ${item["name"]}:boolean[];
        <?py else: ?>
        ${item["name"]}:boolean;
        <?py #endif ?>
        <?py elif item["islist"]: ?>
        ${item["name"]}:Array<${item["type"]}VO>;
        <?py else: ?>
        ${item["name"]}:${item["type"]}VO;
        <?py #endif ?>
    <?py #endfor ?>
}
<?py #endif ?>
<?py #endfor ?>
export interface ${messageName}VO extends MessageVO{
<?py for item in fields: ?>
    /**
    * ${item["comment"]}
    */
    <?py if item["type"]=="Long" or item["type"]=="Int" or item["type"]=="Float"  or item["type"]=="Short" or item["type"]=="Byte": ?>
    <?py if item["islist"]: ?>
    ${item["name"]}:number[];
    <?py else: ?>
    ${item["name"]}:number;
    <?py #endif ?>
    <?py elif item["type"]=="String": ?>
    <?py if item["islist"]: ?>
    ${item["name"]}:string[];
    <?py else: ?>
    ${item["name"]}:string;
    <?py #endif ?>
    <?py elif item["type"]=="Boolean": ?>
    <?py if item["islist"]: ?>
    ${item["name"]}:boolean[];
    <?py else: ?>
    ${item["name"]}:boolean;
    <?py #endif ?>
    <?py elif item["islist"]: ?>
    ${item["name"]}:Array<${item["type"]}VO>;
    <?py else: ?>
    ${item["name"]}:${item["type"]}VO;
    <?py #endif ?>
<?py #endfor?>
}
      
export class ${messageName} implements IMessageRead {
    <?py for listfunction in listField: ?>
    <?py if listfunction["islist"]: ?>
    private read${listfunction["type"]}(message):Array<${listfunction["type"]}VO>{
        let count = message.readShort()
        let list:${listfunction["type"]}VO[]=[];
        for (var i=0;i<count;i++){
    <?py else: ?>
     private read${listfunction["type"]}(message):${listfunction["type"]}VO{
    <?py #endif ?>
        
            <?py if listfunction["ismacro"]: ?>
            let dataTable = MessageMacro.read${listfunction["type"]}(message);
            <?py else: ?>
            let dataTable:any = {};
            <?py #endif ?>
            <?py for item in listfunction["fields"]: ?>
            <?py if item["islist"]: ?>
            <?py if item["type"]=="Long" or item["type"] == "String" or item["type"]=="Int" or item["type"]=="Float"  or item["type"]=="Short" or item["type"]=="Byte": ?>
            dataTable.${item["name"]}=[];
            for (let i=message.readShort();i>0;i--){
                dataTable.${item["name"]}.push(message.read${item["type"]}());
            }
            <?py else: ?>
            dataTable.${item["name"]} = this.read${item["type"]}(message);
            <?py #endif ?>
            <?py elif item["ismacro"]: ?>
            dataTable.${item["name"]} = MessageMacro.read${item["type"]}(message,true);
            <?py else: ?>
            dataTable.${item["name"]} = message.read${item["type"]}();
            <?py #endif ?>
            <?py #endfor ?>
    <?py if listfunction["islist"]: ?>
            list.push(dataTable);
        }
        return list;
    <?py else: ?>
        return dataTable;
    <?py #endif ?>
    }
<?py #endfor ?>  
//  ${comment}
    public read(message:BaseMessage):MessageVO{
        let dataTable:any = {};
        dataTable.messageType = MessageType.${MessageType};
<?py for item in fields: ?>
    <?py if item["islist"]: ?>
        <?py if item["type"]=="Long" or item["type"]=="Boolean" or item["type"] == "String" or item["type"]=="Int" or item["type"]=="Float"  or item["type"]=="Short" or item["type"]=="Byte": ?>
        dataTable.${item["name"]}=[];
        for (let i=message.readShort();i>0;i--){
            dataTable.${item["name"]}.push(message.read${item["type"]}());
        }
        <?py else: ?>
        dataTable.${item["name"]} = this.read${item["type"]}(message);
        <?py #endif ?>
    <?py elif item["ismacro"]: ?>
        dataTable.${item["name"]} = MessageMacro.read${item["type"]}(message);
        <?py for sitem in item["fields"]: ?>
        dataTable.${item["name"]}.${sitem["name"]} = message.read${sitem["type"]}();
        <?py #endfor ?>
    <?py else: ?>
        <?py if item["type"]=="Long" or item["type"]=="Boolean" or item["type"] == "String" or item["type"]=="Int" or item["type"]=="Float"  or item["type"]=="Short" or item["type"]=="Byte": ?>
        dataTable.${item["name"]} = message.read${item["type"]}();
        <?py else: ?>
        dataTable.${item["name"]} = this.read${item["type"]}(message);
        <?py #endif ?>
    <?py #endif ?>
<?py #endfor ?>
        return dataTable;
    }
}
}