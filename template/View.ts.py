module gameview{
    <?py # -*- coding: utf-8 -*- ?>
    export class ${viewName} extends ${viewName}Base{
        protected onInit():void{
            super.onInit();
            <?py for item in components: ?>
            <?py if item["defaultItem"]!="" and item["type"]=="list": ?>
            this.${item["name"]}.setVirtual();
            this.${item["name"]}.callbackThisObj= this;
            this.${item["name"]}.itemRenderer=this.${item["name"]}itemRenderer;
            this.${item["name"]}.numItems = 0;
            <?py #endif ?>
            <?py #endfor ?>
        }
        public updateView(args:any=null):void{

        }
//      添加监听
        protected addSlot(){

        }
    <?py for item in components: ?>
        <?py if item["type"] =="Button": ?>
        protected ${item["name"]}onClick():void{
            
        }
        <?py elif item["type"] =="list": ?>
        protected ${item["name"]}ClickItem(event: fairygui.ItemEvent):void{
            
        }
        <?py if item["defaultItem"]!="": ?>
        protected ${item["name"]}itemRenderer(index:number, item:${item["defaultItem"]}):void{
            item.updateView(index);
        }
        <?py #endif ?>
        <?py elif item["type"] =="ComboBox": ?>
        protected ${item["name"]}onChanged():void{
            
        }
        <?py elif item["type"] =="Slider": ?>
        protected ${item["name"]}onChanged():void{
            
        }
        <?py #endif ?>
    <?py #endfor ?>
    }
}