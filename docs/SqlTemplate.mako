Create Table ${TableName}
(\
% for fields in mapRows:
    % if fields['Key'] == 'PK':
        <% genPK(fields) %>\
    % else:
        % if ((fields['資料型態'] == 'decimal') or ( fields['資料型態'] == 'varchar') or ( fields['資料型態'] == 'nvarchar')): 
            ${genFieldHaveLen(fields)}\
        % else:
            ${genField(fields)}\
        % endif
    % endif
% endfor

)

% for fields in mapRows:
EXEC sys.sp_addextendedproperty
    @name = N'MS_Description'
    ,@value = N'${fields['欄位中文名稱']}'
    ,@level0type = N'SCHEMA'
    ,@level0name = N'ERP'
    ,@level1type = N'TABLE'
    ,@level1name = N'${TableName}'
    ,@level2type = N'COLUMN'
    ,@level2name = N'${fields['欄位英文名稱']}'
% endfor 
<%def name="genPK(fields)">
    % if fields['資料型態'] == 'uniqueidentifier':
    ${fields['欄位英文名稱']} UNIQUEIDENTIFIER DEFAULT NEWID(),
        % elif fields['資料型態'] == 'int':
    ${fields['欄位英文名稱']} Int Not Null Identity(1,1),
        % endif
    CONSTRAINT PK_${TableName} PRIMARY KEY CLUSTERED(${fields['欄位英文名稱']}),\
</%def>
<%def name="genFieldHaveLen(fields)">
    % if fields['CanNull'] == 'Y':
    ${fields['欄位英文名稱']} ${fields['資料型態']}(${fields['長度']}) Null,\
    % else:
    ${fields['欄位英文名稱']} ${fields['資料型態']}(${fields['長度']}),\
    % endif
</%def>
<%def name="genField(fields)">
    % if fields['CanNull'] == 'Y':
    ${fields['欄位英文名稱']} ${fields['資料型態']} Null,\
    % else:
    ${fields['欄位英文名稱']} ${fields['資料型態']},\
    % endif
</%def>