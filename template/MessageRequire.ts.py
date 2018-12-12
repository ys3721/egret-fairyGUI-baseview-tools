/** This is an automatically generated. Please do not modify it. **/
module network {
<?py # -*- coding: utf-8 -*- ?>
export class MessageRouting {
    public static classMap={};
    public static init():void{
        <?py for item in MessageTypes: ?>
        MessageRouting.classMap[MessageType.${item["type"]}]=${item["name"]};
        <?py #endfor ?>
    }
    
}
}
