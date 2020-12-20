$(document).ready(function(){
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
                $(this).html(input);
                $(this).removeClass("editable")
            });

            $(document).on("blur",".input-data",function(){
                var value=$(this).val();
                var data_type=$(this).data("type");
                console.log(data_type);
                var td=$(this).parent("td");
                $(this).remove();
                td.html(value);
                td.addClass("editable");
                var type=td.data("type");
                sendEditToServer(td.data("id"),value,type);
            });
            $(document).on("keypress",".input-data",function(e){
                var key=e.which;
                if(key==13){
                    var value=$(this).val();
                    var td=$(this).parent("td");
                  //  $(this).remove();
                    td.html(value);
                    td.addClass("editable");
                   var type=td.data("type");
                   sendEditToServer(td.data("id"),value,type);
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
                    console.log(response);
                })
                .fail(function(){
                   alert("failed to load the data at the server , mybe value too big to field in db ... call tomer");
                });
            }

            $(".delete-btn").click(function() {
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
                console.log(id);
                $.ajax({
                    url:deleteUrl,
                    type:"POST",
                    data:{id:id},
                })
                .done(function(response){
                    console.log(response);
                })
                .fail(function(){
                   alert("failed to load the data at the server , Something wend Wrong... talk with tomer");
                });
            }
            });


            $('#createSubTask').click(function() {
                console.log(this);
                let task_id = $(this).data('task');
                let email = document.getElementById("inputEmail4").value;
                let problem = document.getElementById("Problem").value;
                let mission = document.getElementById("Mission").value;
                let status = document.getElementById("status").value;
                let responsibility = document.getElementById("responsibility").value;
                console.log("taskid="+task_id);
                console.log("email="+email);
                console.log("problem="+problem);
                console.log("mission="+mission);
                console.log("status="+status);
                console.log("responsibility="+responsibility);
                let dict_data ={
                    task_id : task_id,
                    email : email,
                    problem : problem,
                    mission : mission,
                    status : status,
                    responsibility: responsibility,
                };
                let serverResponse = sendCreateToServer(dict_data);
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
                    return response;
                })
                .fail(function(response){
                   alert("failed to load the data at the server , mybe value too big to field in db ... call tomer");
                   return response;
                });
            }

});