$(document).ready(function(){

    //Function when change Area
    $('#area').change(function(){
        $.ajax({
            url:'filter_wo_area',
            type:'get',
            data:{
                area:$('#area option:selected').text(),
                location:$('#location option:selected').text(),
                asset:$('#asset option:selected').text(),
                createdby:$('#createdby option:selected').text(),
                status:$('#status option:selected').text()
            },
            success:function(response){
                $('#location').find('option').remove().end();
                $('#location').append(`<option>Location</option>`);
                $('.display').empty();
                $('.wodetails').empty();

                //Populate Location dropdown
                $.each(response[0].locations, function(key,value){
                    $('#location').append($(`<option value=${value}>${value}</option>`))
                });

                //Update Work Order list
                $.each(response[1].data, function(key,value){
                    updateList(value);
                });
            }
        });    
    });
    
    //Function when change Location
    $('#location').change(function(){
        $.ajax({
            url:'filter_wo_location',
            type:'get',
            data:{
                area:$('#area option:selected').text(),
                location:$('#location option:selected').text(),
                asset:$('#asset option:selected').text(),
                createdby:$('#createdby option:selected').text(),
                status:$('#status option:selected').text()
            },
            success:function(response){
                $('#asset').find('option').remove().end();
                $('#asset').append(`<option>Asset</option>`);
                $('.display').empty();

                //Populate asset dropdown
                $.each(response[0].assets, function(key,value){
                    $('#asset').append(`<option value=${value}>${value}</option>`);
                });

                //Update Work Order list
                $.each(response[1].data, function(key,value){
                    updateList(value);
                });
            }
        });    
    });

    //Function when change Created By
    $('#createdby').change(function(){
        $.ajax({
            url:'filter_wo_createdby',
            type:'get',
            data:{
                area:$('#area option:selected').text(),
                location:$('#location option:selected').text(),
                asset:$('#asset option:selected').text(),
                createdby:$('#createdby option:selected').text(),
                status:$('#status option:selected').text()
            },
            success:function(response){
                $('.display').empty();

                //Update Work Order list
                $.each(response.data, function(key,value){
                    updateList(value);
                });
            }
        });    
    });

    //Function when change Status
    $('#status').change(function(){
        $.ajax({
            url:'filter_wo_status',
            type:'get',
            data:{
                area:$('#area option:selected').text(),
                location:$('#location option:selected').text(),
                asset:$('#asset option:selected').text(),
                createdby:$('#createdby option:selected').text(),
                status:$('#status option:selected').text()
            },
            success:function(response){
                $('.display').empty();              

                //Update Work Order list
                $.each(response.data, function(key,value){
                    updateList(value);
                });
            }
        });    
    });

    //WOrk Order List Display Pan
    $(document).on('click','.WOnumber',function(){
         //$('.wodetails').empty()
        $.ajax({
            url:'display_wo',
            type:'get',
            data:{
                wonumber:$(this).attr("value"),
            },
            success:function(response){
                updateDetailsPan(response);
            }
        });
        
    });

    //Add event function
    $(document).on('click','.btnevent',function(){
        $.ajax({
            url:'add_wo_event',
            type:'get',
            data:{
                wonumber:$('#wonum').text(),
                _event:$('.text-event').val()
            },
            success:function(response){
                updateDetailsPan(response);
                console.log(response[0].events)
            }
        });
    });
});


//update details pan
function updateDetailsPan(response){
    $(".wodetails").empty();
    const data = response[1].data
                const events = response[0].events
                var h5=$('<h7/>', {class:"wonumber card-header",
                                    id:"wonum", 
                                    text:"WO-"+data[0]['id']});
                var card_body=$('<div/>',{class:'card-body'}); 
                var card_events=$('<div/>',{class:'card-body'})
                var h6=$('<h5/>',{class:'card-title',
                                    text:data[0]['area'] +" | "+ data[0]['location']+" | "+data[0]['asset']});
                var p1=$('<p/>',{class:'card-text',
                                    text:data[0]['description'],
                                class: "wo-description fw-normal"});
                var p2=$("<p/>",{text:"Created On - " + data[0]['createdTime'],
                                class: "fs-6"});
                var p3=$("<p/>",{text:"Status - " + data[0]['status'],
                                class: "fs-6"});
                var p4=$("<p/>",{text:"Action - " + data[0]['action'],
                                class: "fs-6"});
                var img = $("<img/>",{
                                width:'200px',
                                height:'200px',
                                src:data[0]['image_file'],});
                var div_event_add=$('<div/>',{
                                    class:"div-event"});
                var add_text=$('<input/>',{
                                class:"text-event form-floating",
                                type:"text",});                
                var add_button=$('<button/>',{
                                class:"btnevent btn btn-success btn-sm",
                                text:"Add Event"});
                card_body.append(h6).append(p1).append(p2)
                .append(p3).append(p4).append(img).append(div_event_add);

                div_event_add.append(add_text).append(add_button);

                $.each(events,function(key,value){
                    var single_event=$('<div/>',{
                        class:'events'
                    });
                    var h5_1 = $("<p/>",{
                        class:"fs-6",
                        text:events[key]['event']});
                    var badge1=$("<span/>",{
                        class:'badge bg-primary',
                        text:events[key]['editedBy']});
                    var badge2=$("<span/>",{
                        class:'badge bg-info',
                        text:events[key]['editedTime']});
                    single_event.append(h5_1).append(badge2).append(badge1)
                    card_events.append(single_event)
                });
                $('.wodetails').append(h5)
                $('.wodetails').append(card_body).append(card_events);
}

//Function for updating list when change any dropdown list 
function updateList(value){
    var card=$('<div/>', {class:"card"});
    var card_body=$('<div/>',{class:'card-body'});
    var h5 = ($("<h5/>",{
                    class:"card-title",
                    text:value['area']
                    +"|"+value['location']+"|"
                    + value['asset']}))
                    .append($("<h6/>",{
                    class:"card-subtitle mb2 text-muted",
                    text:value['description']}));
    var button = ($("<button/>",{
                        text:"WO Number - " + value['id'],
                        value:value['id'],
                        class:"WOnumber btn btn-outline-primary btn-sm"}));
    var span1 = ($("<span/>",{
                        class:"badge bg-primary",
                        text:value['createdBy']}));                
    var span2 = ($("<span/>",{
                        class:"badge bg-secondary",
                        text:value['status']}));
    card_body.append(h5).append(button).append(span1).append(span2);
    card.append(card_body);  
    $('.display').append(card);
}

