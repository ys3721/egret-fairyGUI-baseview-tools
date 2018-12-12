<?py # -*- coding: utf-8 -*- ?>
[
<?py if len(data)>0: ?>
    [
    <?py splitechar="" 
        for item in data: ?>
        <?py for x in xrange(1,len(item)):?>${splitechar}${item[x]}<?py
         splitechar="," 
          #endfor ?>
    <?py
    splitechar="],\n["
    #endfor ?>
    ]
<?py #endif ?>
]
