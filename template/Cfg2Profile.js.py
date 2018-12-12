/** This is an automatically generated. Please do not modify it. **/
module ProfileData {
export class Cfg2Profile {
<?py for moduName in moduNames: ?>
    private _${moduName}:ProfileData.${moduName};
    public get ${moduName[0].lower()+moduName[1:]}(): ProfileData.${moduName}{
        if(!this._${moduName}){
            this._${moduName} = new ProfileData.${moduName}();
            this._${moduName}.loadJson("${moduName}_json");
        }
        return this._${moduName};
    }
<?py #endfor ?>
}
}