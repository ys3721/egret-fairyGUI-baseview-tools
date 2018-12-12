/** This is an automatically generated. Please do not modify it. **/
module ModuleConfig{
    <?py for key in modules: ?>
    export class ${key}{
        public static readonly packageName:string = "${key}";
        <?py for module in modules[key]: ?>
        public static ${module}:framework.ModuleConfigVO;
        <?py #endfor ?>
    }
    <?py #endfor ?>
    export class ModuleConfigBinder{
        public static bindAll():void {
        <?py for key in modules: ?>
        <?py for module in modules[key]: ?>
            ModuleConfig.${key}.${module}= new framework.ModuleConfigVO(${str(modules[key][module]["fullScreen"]).lower()},"${modules[key][module]["ui"]}",
            [
            <?py for packageName in modules[key][module]["packageNames"]: ?>
            ModuleConfig.${packageName}.packageName,
            <?py #endfor ?>
            ]
            );
            <?py if module !="ModalWaiting": ?>
            <?py if modules[key][module]["outsideTouchCancel"]: ?>
            ModuleConfig.${key}.${module}.outsideTouchCancel = true;
            <?py #endif ?>
            fairygui.UIObjectFactory.setPackageItemExtension(ModuleConfig.${key}.${module}.URL, gameview.${modules[key][module]["className"]});
            <?py #endif ?>
        <?py #endfor ?>
        <?py #endfor ?>
        }
    }
}