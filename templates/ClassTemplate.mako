using System;
namespace MyNameSpace
{
    public class ${TableName}
    {
        % for row in mapRows:
        /// <summary>
        /// ${row['fieldDesc'].decode()}
        /// </summary>
        public ${row['fieldType']} ${row['columnName']} { get; set; }
        
        % endfor
    }
}
