/** This is an automatically generated. Please do not modify it. **/
module gameview{
    <?py # -*- coding: utf-8 -*- ?>
    export class ${viewName}Base extends ${superView}{
    <?py for item in components: ?>
    <?py if item["luaClass"]=="": ?>
        <?py if item["type"] =="Button": ?>
        public ${item["name"]}:fairygui.GButton;
        <?py elif item["type"] =="list": ?>
        public ${item["name"]}:fairygui.GList;
        <?py elif item["type"] =="ComboBox": ?>
        public ${item["name"]}:fairygui.GComboBox;
        <?py elif item["type"] =="Slider": ?>
        public ${item["name"]}:fairygui.GSlider;
        <?py elif item["type"] =="image": ?>
        public ${item["name"]}:fairygui.GImage;
        <?py elif item["type"] =="loader": ?>
        public ${item["name"]}:fairygui.GLoader;
        <?py elif item["type"] =="text": ?>
        public ${item["name"]}:fairygui.GTextField;
        <?py elif item["type"] =="input": ?>
        public ${item["name"]}:fairygui.GTextInput;
        <?py elif item["type"] =="richtext": ?>
        public ${item["name"]}:fairygui.GRichTextField;
        <?py elif item["type"] =="graph": ?>
        public ${item["name"]}:fairygui.GGraph;
        <?py elif item["type"] =="movieclip": ?>
        public ${item["name"]}:fairygui.GMovieClip;
        <?py else: ?>
//      public ${item["name"]}:${item["type"]};
        <?py #endif ?>
    <?py else: ?>
        public ${item["name"]}:${item["luaClass"]};
    <?py #endif ?>
    <?py #endfor ?>
    <?py if superView.find("fairygui.G")>-1: ?>
        private signals:Array<any>=[];
        protected onInit():void{
            this.addSlot();
        }
       
        protected addSlot() {

        }
        protected addSlot2Signal(signal:any,slot:Function):void{
            framework.EventManager.addSlot2Signal(signal,slot,this);
        }
        protected removeSlot():void{
            framework.EventManager.removeAllSlot(this);
        }
        public dispose():void{
            this.removeAllEventListener();
            this.removeSlot();
            super.dispose();
        }
    <?py #endif ?>
    <?py content = contentView.strip()=="" and " " or contentView+" , " ?>

        protected constructFromXML(xml: any): void {
            super.constructFromXML(xml);
        <?py if superView.find("fairygui.G")>-1: ?>
            framework.BaseView.constructFromXMLGButton(this);
        <?py #endif ?>
        <?py for item in components: ?>
                <?py if item["touchable"]: ?>
                <?py if item["luaClass"] =="HeroView" or  item["type"] =="Button" or item["type"] =="loader": ?>
            this.${item["name"]}.addEventListener(egret.TouchEvent.TOUCH_TAP,this.${item["name"]}onClick,this);
                <?py elif item["type"] =="list": ?>
            this.${item["name"]}.addEventListener(fairygui.ItemEvent.CLICK,this.${item["name"]}ClickItem,this);
                <?py elif item["type"] =="ComboBox": ?>
            this.${item["name"]}.addEventListener(egret.TouchEvent.TOUCH_TAP,this.${item["name"]}onChanged,this);
                <?py elif item["type"] =="Slider": ?>
            this.${item["name"]}.addEventListener(egret.TouchEvent.TOUCH_TAP,this.${item["name"]}onChanged,this);
                <?py #endif ?>
                <?py #endif ?>
        <?py #endfor ?>
            this.onInit();
        }
        
        public removeAllEventListener():void{
            <?py if superView.find("fairygui.G")<0: ?>
            super.removeAllEventListener();
            <?py #endif ?>
            <?py for item in components: ?>
                <?py if item["touchable"]: ?>
                <?py if item["luaClass"] =="HeroView" or item["type"] =="Button" or item["type"] =="loader": ?>
            this.${item["name"]}.removeEventListener(egret.TouchEvent.TOUCH_TAP,this.${item["name"]}onClick,this);
                <?py elif item["type"] =="list": ?>
            this.${item["name"]}.removeEventListener(fairygui.ItemEvent.CLICK,this.${item["name"]}ClickItem,this);
                <?py elif item["type"] =="ComboBox": ?>
            this.${item["name"]}.removeEventListener(egret.TouchEvent.TOUCH_TAP,this.${item["name"]}onChanged,this);
                <?py elif item["type"] =="Slider": ?>
            this.${item["name"]}.removeEventListener(egret.TouchEvent.TOUCH_TAP,this.${item["name"]}onChanged,this);
                <?py #endif ?>
                <?py #endif ?>
            <?py #endfor ?>
        }
        
        
        <?py for item in components: ?>
        <?py if item["touchable"]: ?>
        <?py if item["luaClass"] =="HeroView" or item["type"] =="Button" or item["type"] =="loader": ?>
        protected ${item["name"]}onClick(event:egret.TouchEvent):void{
            
        }
        <?py elif item["type"] =="list": ?>
        protected ${item["name"]}ClickItem(event: fairygui.ItemEvent):void{
            
        }
        <?py elif item["type"] =="ComboBox": ?>
        protected ${item["name"]}onChanged():void{
            
        }
        <?py elif item["type"] =="Slider": ?>
        protected ${item["name"]}onChanged():void{
            
        }
        <?py #endif ?>
        <?py #endif ?>
    <?py #endfor ?>
    }
}