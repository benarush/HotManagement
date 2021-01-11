$(document).ready(function(){

    // the varriable lastEditValue for holding the value before editing , cuz if the value are same
    // it will be more effective to reduce the api calls

    var lastEditValue;

    // .editable class is will change to inputmode on double click
    $(document).on("dblclick",".editable",function(){
        var value=$(this).text();
        var data_type=$(this).data("type");
        var input_type="text";
        if(data_type=="created_at")
        {
            input_type="datetime-local";
        }
        if(data_type=="email")
        {
           input_type="email";
        }
        console.log("type:" + data_type);
        if(data_type!="status")
        {
            var input="<input type='"+input_type+"' class='input-data' value='"+value+"' class='form-control'>";
        }
        else
        {
            var input= `<select id="cars" name="cars" class='input-data' data-type="status">
            <option value="open">Open</option>
            <option value="closed">Closed</option>
            </select>`;
        }
        lastEditValue = value ;
        $(this).html(input);
        $(this).removeClass("editable")
    });
    // after removing focus , the apicalls will send to update only if the value has been changed
    $(document).on("blur",".input-data",function(){
        var value=$(this).val();
        var data_type=$(this).data("type");
        console.log(data_type);
        var td=$(this).parent("td");
        $(this).remove();
        td.html(value);
        td.addClass("editable");
        var type=td.data("type");
        if (lastEditValue != value)
        {
            sendEditToServer(td.data("id"),value,type);
        }
    });

    // after click Enter , the apicalls will send to update only if the value has been changed
    $(document).on("keypress",".input-data",function(e){
        var key=e.which;
        if(key==13){
            var value=$(this).val();
            var td=$(this).parent("td");
          //  $(this).remove();
            td.html(value);
            td.addClass("editable");
            var type=td.data("type");
            if(lastEditValue != value)
            {
//               no need to send to server on enter , because its already sending after the class changing
//                sendEditToServer(td.data("id"),value,type);
            }
        }
    });

    function sendEditToServer(id,value,type){
        console.log(id);
        console.log(value);
        console.log(type);
        $.ajax({
            url:editUrl,
            type:"POST",
            data:{id:id,type:type,value:value},
        })
        .done(function(response){
            if (type === "status" ){
                let isOpen = value ==="closed";
                delete_update_graphs(isOpen);
                add_update_graphs(!isOpen);
                document.getElementById(id).className = value === "closed" ? "alert-success" : "alert-danger";
            }

            console.log(response);
        })
        .fail(function(){
           alert("failed to load the data at the server , mybe value too big to field in db ... call tomer");
        });
    }

    $(document).on('click', '.delete-btn', function(){
        console.log(this);
        let td=$(this).parent("td");
        console.log(td);
        console.log(td.data("id"));
        if(confirm("Are You sure that you want to delete this sub task?"))
        {
            sendDeleteToServer(td.data("id"));
        }
        else
        {
            console.log("Nothing Happen");
            return;
        }
        document.getElementById(""+td.data("id")).remove();

        function sendDeleteToServer(id){
            let isOpen = document.getElementById(id).className.includes("danger");
            $.ajax({
                url:deleteUrl,
                type:"POST",
                data:{id:id},
            })
            .done(function(response){
                console.log(response);
                delete_update_graphs(isOpen);
            })
            .fail(function(){
               alert("failed to load the data at the server , Something wend Wrong... talk with tomer");
            });
        }
    });
     $(document).on("dblclick",'#createSubTask',function(){
        console.log("cancel");
     });
    $('#createSubTask').click(function() {
        console.log(this);
        let task_id = $(this).data('task');
        let email = document.getElementById("inputEmail4").value;
        let problem = document.getElementById("Problem").value;
        let mission = document.getElementById("Mission").value;
        let status = document.getElementById("status").value;
        let responsibility = document.getElementById("responsibility").value;
        let dict_data ={
            task_id : task_id,
            email : email,
            problem : problem,
            mission : mission,
            status : status,
            responsibility: responsibility,
        };
        let serverResponse = sendCreateToServer(dict_data);
        console.log(serverResponse);
    })

    function sendCreateToServer(post_dict_data){
        console.log(post_dict_data);
        $.ajax({
            url:CreateUrl,
            type:"POST",
            data:post_dict_data,
        })
        .done(function(response){
            console.log(response);
            $('#formModel').modal('hide');
            td_danger_success = response.current_status == "Close" ? "alert-success": "alert-danger";
            $(".table").find('tbody').append(`
            <tr id="` +response.id+ `" class="` + td_danger_success + `">
            <td class="editable" data-id="`+response.id+`" data-type="problem">` + response.problem +`</td>
            <td class="editable" data-id="`+response.id+`" data-type="mission">` + response.mission +`</td>
            <td class="editable" data-id="`+response.id+`" data-type="responsibility">` + response.responsibility +`</td>
            <td class="editable" data-id="`+response.id+`" data-type="status">` + response.current_status +`</td>
            <td class="editable" data-id="`+response.id+`" data-type="email">` + response.email +`</td>
            <td data-id="`+response.id+`"><a data-id="`+response.id+ `" class="delete-btn ml-1" href="#">
            <img data-id="` +response.id+`" src="`+ deleteIMG_url + `"></a></td></tr>`);
            add_update_graphs(response.current_status === "Open" ? true: false)
            return response;
        })
        .fail(function(response){
           emailExp = response.responseJSON.hasOwnProperty('email') ? response.responseJSON.email[0] : "OK";
           problem = response.responseJSON.hasOwnProperty('problem') ? response.responseJSON.problem[0] : "OK";
           mission = response.responseJSON.hasOwnProperty('mission') ? response.responseJSON.problem[0] : "OK";
           alert("email -" + emailExp + "\n" +"problem -" + problem + "\n" +"mission -" + mission);
           return response;
        });
    }

    function add_update_graphs(isOpen){
        if (isOpen)
        {
            myChart.data.datasets[0].data[0]= myChart.data.datasets[0].data[0] + 1;
            myChart2.data.datasets[0].data[1]= myChart2.data.datasets[0].data[1] + 1;
            myChart.update()
            myChart2.update()
        }
        else
        {
            myChart.data.datasets[0].data[1] = myChart.data.datasets[0].data[1] + 1;
            myChart2.data.datasets[0].data[0] = myChart2.data.datasets[0].data[0] + 1;
            myChart2.update()
            myChart.update()

        }
    }

    function delete_update_graphs(isOpen){
        if (isOpen)
        {
            myChart.data.datasets[0].data[0]= myChart.data.datasets[0].data[0] - 1;
            myChart2.data.datasets[0].data[1] = myChart2.data.datasets[0].data[1] - 1;
            myChart.update()
            myChart2.update()
        }
        else
        {
            myChart.data.datasets[0].data[1] = myChart.data.datasets[0].data[1] - 1;
            myChart2.data.datasets[0].data[0] = myChart2.data.datasets[0].data[0] - 1;
            myChart.update()
            myChart2.update()
        }
    }
});