/** This is an automatically generated. Please do not modify it. **/
module network {
export class  ${messageName} implements IMessageWrite {
    <?py for item in fields: ?>
    <?py if item["islist"]: ?>
    protected write${item["name"]}(message:BaseMessage,value:any[]):void{
        let len = value.length;
        message.writeShort(len)
        for(let v of value){
            message.write${item["type"]}(v);
        }
    }
    <?py #endif ?>
    <?py #endfor ?>
//  ${comment}
    public write(message:BaseMessage,value:any):void{
        <?py for item in fields: ?>
//       ${item["comment"]}
        <?py if item["islist"]: ?>
        this.write${item["name"]}(message,value["${item["name"]}"]);
        <?py else: ?>
        message.write${item["type"]}(value["${item["name"]}"]);
        <?py #endif ?>
    <?py #endfor ?>
        message.writeString(value && value["extraInfo"] || "");
    }
}
}