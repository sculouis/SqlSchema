<template>
<SectionEdit title="文件資訊">
% for box in Boxs:
% if "table_" in box.BoxName:
    <Box title="${box.BoxName}">
    <TableBase v-bind:tableData="noDelData">
% for row in box.Datas:
        % if row[0] ==  1:
        <template slot="FirstHead">
            <th class="th-title w5">no</th>
        % for fields in row[1]:
            <th class="th-title w15">${fields.標題名稱}</th>
        % endfor   
        </template>
        <template v-slot:FirstDetail = "{ data,index }">
            <td v-text="index + 1" rowspan="200"></td>
        % for fields in row[1]:
            <td> ${genTagDesc(fields.寬度,fields.標題名稱,fields.欄位類型,fields.是否必輸,fields.欄位名稱,fields.提示說明,fields.備註)}</td>
        % endfor  
        </template>
        % elif row[0] ==  2:
        <template v-slot:SecondDetailHead>
        % for fields in row[1]:
            <th class="th-title-1 w15">${fields.標題名稱}</th>
        % endfor    
        </template>
        <template v-slot:SecondDetail= "{ data }">
        % for fields in row[1]:
                <td>${genTagDesc(fields.寬度,fields.標題名稱,fields.欄位類型,fields.是否必輸,fields.欄位名稱,fields.提示說明,fields.備註)}</td>
        % endfor
        </template>
        % elif row[0] ==  3:
        <template v-slot:ThirdHead="{ data }">
        % for fields in row[1]:
            <th class="th-title-1">${fields.標題名稱}</th>
        % endfor    
        </template>
        <template v-slot:ThirdDetail="{ subdata,index }">
        % for fields in row[1]:
                <td>${genTagDesc(fields.寬度,fields.標題名稱,fields.欄位類型,fields.是否必輸,fields.欄位名稱,fields.提示說明,fields.備註)}</td>
        % endfor
        </template>
        % endif
        % endfor
        </TableBase>
    </Box>
% else:
    <Box title="${box.BoxName}">
% for row in box.Datas:
        <div class="row">\
        % for fields in row[1]:
        ${genField(fields.寬度,fields.標題名稱,fields.欄位類型,fields.是否必輸,fields.欄位名稱,fields.提示說明,fields.備註)} \
        % endfor

        </div>
% endfor
    </Box>
% endif    
% endfor
</SectionEdit>
</template>

<script>
    import SectionEdit from '../components/SectionEdit.vue'
    import Box from '../components/Box.vue'
    import Selecter from '../components/Selecter.vue'
    import TextNumber from '../components/TextNumber.vue'
    import TextString from '../components/TextString.vue'
    import DatePicker from '../components/DatePicker.vue'
    import CheckBox from '../components/CheckBox.vue'
    import RadioButton from '../components/RadioButton.vue'
    import ButtonAction from '../components/ButtonAction.vue'
    import DisableText from '../components/DisableText.vue'
    import Popup from '../components/Popup.vue'
    import TableBase from '../components/TableBase.vue'
    import { required } from 'vuelidate/lib/validators'
    import { mapGetters, mapMutations } from 'vuex'

export default {
            components: {
            SectionEdit,
            Box,
            Selecter,
            TextNumber,
            TextString,
            DatePicker,
            CheckBox,
            RadioButton,
            ButtonAction,
            DisableText,
            Popup,
            TableBase
        },
        data() {
            return {\
        % for box in Boxs:
            % for row in box.Datas:
                % if "table_" not in box.BoxName:
                    % for fields in row[1]:
                            % if fields.欄位類型 != "ButtonAction":
                                ${genDataModel(fields.欄位名稱)}\
                            % endif   
                    % endfor
                % endif
            % endfor
        % endfor
            }
        },
        validations:{
                val:{
                        required,
                        greaterThan(value){
                            if (value !== ""){
                                return Number(value) > -1
                            }else {
                                return true
                            }
                        }
            },
                numValue:{
                        required,
            },
            myDate:{
                        required,
            }
        },
        mounted(){
            console.log(this.$v.$reset())
            var tableData = [{\
        % for box in Boxs:
            % for row in box.Datas:
                % if "table_"  in box.BoxName:
                    % if row[0] == 3:
                            subDatas:[{
                            % for fields in row[1]:
                            % if fields.欄位類型 != "ButtonAction":
                                ${genDataModel(fields.欄位名稱)}\
                            % endif   
                    % endfor
                             } ],
                    % else:
                    % for fields in row[1]:
                            % if fields.欄位類型 != "ButtonAction":
                                ${genDataModel(fields.欄位名稱)}\
                            % endif   
                    % endfor
                % endif
                % endif
            % endfor
        % endfor 
            isdelete:0,
            isDetailOpen: false,
            isSubOpen: false
            }]
            this.initData(tableData)    
    },
    computed:{...mapGetters('table',['noDelData'])},
    methods:{...mapMutations('table',['initData']),
            submit(){
                this.submitted = true
            }
        }
}
</script>
<%def name="genField(collen,title,type,required,fieldName,placeholder,remark)">
            <div class="col-sm-${collen} content-box">
                <div class="w100 title">
                    <b class="float-left">${title}</b>
                    % if required == 'Y':
                    <b class="required-icon">*</b>
                    % endif
                </div>\
                    ${genTagDesc(collen,title,type,required,fieldName,placeholder,remark)}\
            </div>\
</%def>\
<%def name="genTagDesc(collen,title,type,required,fieldName,placeholder,remark)">
        % if type == "Popup":
                <${type} bgColor="btn-02-blue"  iconName="icon-search"  remodalId="${fieldName}" title="彈出視窗" buttonName="按鈕"></${type}>
        % elif type== "CheckBox":
                <${type} v-model="${fieldName}" title="${title}"></${type}>
        % elif type== "DisableText":
                <${type} v-model="${fieldName}" placeHolder="${placeholder}"></${type}>
        % elif type== "TextString":
                <${type} v-model="${fieldName}" placeHolder="${placeholder}"></${type}>
        % elif type== "ButtonAction":
        % for button in remark.split(","):
                % if  button.split(":")[1] == "btn-02-blue":
                    <${type} bgColor="${button.split(":")[1]}"  iconName="icon-search">${button.split(":")[0]}</${type}>
                % else:
                    <${type} bgColor="${button.split(":")[1]}"  iconName="glyphicon glyphicon-remove">${button.split(":")[0]}</${type}>
                % endif
        % endfor
        %else:
                <${type} v-model="${fieldName}"></${type}>
        % endif
</%def>\
<%def name="genDataModel(fieldName)">
                        ${fieldName}:"",\
</%def>