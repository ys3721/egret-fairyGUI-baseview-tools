/** This is an automatically generated. Please do not modify it. **/
module network {
    export enum MessageType{
    CG_HANDSHAKE=510,
    GC_HANDSHAKE=511,
    <?py # -*- coding: utf-8 -*- ?>
    <?py for item in MessageTypes: ?>
    /**
    * ${item["comment"]}
    */
    ${item["type"]} = ${item["id"]},
    <?py #endfor ?>
    }
}