$(document).ready(function(){
    $('#area').change(function(){   
        $('#location').find('option').remove().end();
        $('#asset').find('option').remove().end() ;
        $.ajax({
            url:'selectlocation',
            type:'get',
            data:{
                area:$('#area option:selected').text()
            },
            success:function(response){
                $.each(response.data, function(key,value){
                    $('#location').append($(`<option value=${value}>${value}</option>`))
                })     
            },
        });
    });

    $('#location').change(function(){
        $('#asset').find('option').remove().end() ;
        $.ajax({
            url:'selectasset',
            type:'get',
            data:{
                area:$('#area option:selected').text(),
                location:$('#location option:selected').text()
            },
            success:function(response){
                $.each(response.data, function(key,value){
                    $('#asset').append($(`<option value=${value}>${value}</option>`))
                })
            }
        });
    });

});