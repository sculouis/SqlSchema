<template>
<SectionEdit title="文件資訊">
% for box in Boxs:
    <Box title="${box.BoxName}">
% for row in box.Datas:
        <div class="row">\
        % for fields in row[1]:
        ${genField(fields.寬度,fields.標題名稱,fields.欄位類型,fields.是否必輸,fields.欄位名稱)} \
        % endfor

        </div>
% endfor
    </Box>
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
    import { required } from 'vuelidate/lib/validators'

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
            Popup
        },
        data() {
            return {\
        % for box in Boxs:
            % for row in box.Datas:
                % for fields in row[1]:
                        % if fields.欄位類型 != "ButtonAction":
                            ${genDataModel(fields.欄位名稱)}\
                        % endif   
                % endfor
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
        },
        methods:{
            submit(){
                this.submitted = true
            }
        }
        }
</script>
<%def name="genField(collen,title,type,required,fieldName)">
            <div class="col-sm-${collen} content-box">
                <div class="w100 title">
                    <b class="float-left">${title}</b>
                    % if required == 'Y':
                    <b class="required-icon">*</b>
                    % endif
                </div>
                    % if type == "Popup":
                    <${type} bgColor="btn-02-blue"  iconName="icon-search"  remodalId="${fieldName}" title="彈出視窗" buttonName="按鈕"></${type}>
                    % else:
                    <${type} v-model="${fieldName}"></${type}>
                    % endif
            </div>\
</%def>
<%def name="genDataModel(fieldName)">
                        ${fieldName}:"",\
</%def>
