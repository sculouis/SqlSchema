% for fields in mapRows:
    % if fields['Key'] == 'FK':
ALTER TABLE ${TableName} 
ADD FOREIGN KEY (${fields['欄位英文名稱']}) REFERENCES ${fields['外來鍵資料表']}(${fields['欄位英文名稱']});
    % endif
% endfor
