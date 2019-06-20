using System;
namespace MyNameSpace
{
    public class ${TableName}
    {
        % for row in mapRows:
        /// <summary>
        /// ${row['fieldDesc'].decode()}
        /// </summary>
        /// <value>The identifier.</value>
        public ${row['fieldType']} ${row['columnName']} { get; set; }
        
        % endfor
    }
}
