## 判斷資料表是否存在
IF (EXISTS (SELECT * 
                 FROM INFORMATION_SCHEMA.TABLES 
                 WHERE TABLE_SCHEMA = 'ERP' 
                 AND  TABLE_NAME = '${TableName}'))
BEGIN
    print N'資料表:ERP.${TableName}已存在，刪除此資料表再新增'
    drop Table ERP.${TableName}
END

Create Table ERP.${TableName}
(\
% for fields in mapRows:
    % if fields.Key == 'PK':
        <% genPK(fields) %>\
    %elif fields.Key == 'FK':
        <% genFK(fields) %>\
    % else:
        % if ((fields.資料型態 == 'decimal') or ( fields.資料型態 == 'varchar') or ( fields.資料型態 == 'nvarchar')): 
            ${genFieldHaveLen(fields)}\
        % else:
            ${genField(fields)}\
        % endif
    % endif
% endfor
)

% for fields in (x for x in mapRows if x.Key == 'FK'):
CREATE NONCLUSTERED INDEX ix_nonclustered_${fields.欄位英文名稱} ON ERP.${TableName}(${fields.欄位英文名稱})
% endfor
% for fields in mapRows:
EXEC sys.sp_addextendedproperty
    @name = N'MS_Description'
    ,@value = N'${fields.欄位中文名稱}'
    ,@level0type = N'SCHEMA'
    ,@level0name = N'ERP'
    ,@level1type = N'TABLE'
    ,@level1name = N'${TableName}'
    ,@level2type = N'COLUMN'
    ,@level2name = N'${fields.欄位英文名稱}'
% endfor 
<%def name="genPK(fields)">
    % if fields.資料型態 == 'uniqueidentifier':
        % if fields.預設值 == '(newid())':
    ${fields.欄位英文名稱} UNIQUEIDENTIFIER ${fields.Null} ${'DEFAULT NEWID()' },
        % else:
    ${fields.欄位英文名稱} UNIQUEIDENTIFIER ${fields.Null},
        % endif    
    % elif fields.資料型態 == 'int':
    ${fields.欄位英文名稱} Int ${fields.Null} Identity(1,1),
    % endif
    CONSTRAINT PK_${TableName} PRIMARY KEY CLUSTERED(${fields.欄位英文名稱}),\
</%def>
<%def name="genFK(fields)">
    ${fields.欄位英文名稱} ${fields.資料型態} ${fields.Null} FOREIGN KEY REFERENCES ERP.${fields.外來鍵資料表}(${fields.欄位英文名稱}),\
</%def>

<%def name="genFieldHaveLen(fields)">
    % if fields.Null == 'NotNull':
    ${fields.欄位英文名稱} ${fields.資料型態}(${fields.長度}),\
    % else:
    ${fields.欄位英文名稱} ${fields.資料型態}(${fields.長度}) Null,\
    % endif
</%def>
<%def name="genField(fields)">
    % if fields.Null == 'NotNull':
    ${fields.欄位英文名稱} ${fields.資料型態},\
    % else:
    ${fields.欄位英文名稱} ${fields.資料型態} Null,\
    % endif
</%def>