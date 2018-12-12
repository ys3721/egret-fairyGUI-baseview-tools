/** This is an automatically generated. Please do not modify it. **/
module network {
<?py # -*- coding: utf-8 -*- ?>
    <?py for macro in macros.keys(): ?>
    export interface ${macro}VO{
        <?py for item in macros[macro]: ?>
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
        ${item["name"]}:Boolean[];
        <?py else: ?>
        ${item["name"]}:Boolean;
        <?py #endif ?>
        <?py else: ?>
            <?py if item["islist"]: ?>
        ${item["name"]}:${item["type"]}VO[];
            <?py else: ?>
        ${item["name"]}:${item["type"]}VO;
            <?py #endif ?>
        <?py #endif ?>
        <?py #endfor ?>
    }
    <?py #endfor ?>
    export class MessageMacro {
        <?py for macro in macros.keys(): ?>
        public static read${macro}(message:BaseMessage,extraInfo:boolean=false):${macro}VO{
            let vo:any={};
            <?py for item in macros[macro]: ?>
            <?py if item["name"]=="extraInfo": ?>
            if (extraInfo){
                vo.extraInfo=message.readString();
            }
            <?py elif item["type"]=="Long" or item["type"]=="String" or item["type"]=="Boolean" or item["type"]=="Int" or item["type"]=="Short" or item["type"]=="Byte": ?>
                <?py if item["islist"]: ?>
            vo.${item["name"]}=[];
            for(let i = message.readShort();i>0;i--){
                vo.${item["name"]}.push(message.read${item["type"]}());
            }    
                <?py else: ?>
            vo.${item["name"]}=message.read${item["type"]}();
                <?py #endif ?>
            <?py else: ?>
                <?py if item["islist"]: ?>
            vo.${item["name"]}=[];
            for(let i = message.readShort();i>0;i--){
                vo.${item["name"]}.push(MessageMacro.read${item["type"]}(message,true));
            }    
                <?py else: ?>
            vo.${item["name"]}=MessageMacro.read${item["type"]}(message,true);
                <?py #endif ?>
            <?py #endif ?>
            <?py #endfor ?>
            return vo;
        }
        <?py #endfor ?>
    }
}