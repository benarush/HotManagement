
class CSV_Creator {

    constructor(name, year) {
        this.task_problem = document.getElementById("task_Problem").innerText;
        this.task_days = document.getElementById("task_days").innerText;
        this.task_description = document.getElementById("task_description").innerText;
        this.task_start_date = document.getElementById("task_start_date").innerText;
    }

    allTasks_CSV() {
        const file_name = "All Tasks.csv";
        let tasks_dict = this.getAllTasks();
        console.log(tasks_dict);
        let csv = this.buildAllTasksCSV(tasks_dict);
        this.downloadCSV(csv, file_name);
    }

    buildAllTasksCSV(tasks_dict_data) {
        let csv = [], row =[];
        row = this.taskPropertiesRow();
        row.push(String.fromCharCode(0xFEFF) + "Created Date");
        row.push(String.fromCharCode(0xFEFF) + "Email_Attached");
        row.push(String.fromCharCode(0xFEFF) + "author");
        row.push(String.fromCharCode(0xFEFF) + "id");
        csv.push(row.join(","));
        while (row.length) { row.pop() };

        for (let i = 0; i < tasks_dict_data.length; i++) {
            row.push(String.fromCharCode(0xFEFF) + tasks_dict_data[i].problem.replace(",", ""));
            row.push(String.fromCharCode(0xFEFF) + tasks_dict_data[i].description.replace(",", ""));
            row.push(String.fromCharCode(0xFEFF) + tasks_dict_data[i].days);
            row.push(String.fromCharCode(0xFEFF) + tasks_dict_data[i].start_date);
            row.push(String.fromCharCode(0xFEFF) + tasks_dict_data[i].date_created);
            row.push(String.fromCharCode(0xFEFF) + tasks_dict_data[i].email_attached_file);
            row.push(String.fromCharCode(0xFEFF) + tasks_dict_data[i].author);
            row.push(String.fromCharCode(0xFEFF) + tasks_dict_data[i].id);
            csv.push(row.join(","));
            while (row.length) { row.pop() };
        }
        return csv.join("\n");;
        
    }

    taskPropertiesRow(csv) {
        let row = [];
        row.push(String.fromCharCode(0xFEFF) + "Task Problem");
        row.push(String.fromCharCode(0xFEFF) + "Task Description");
        row.push(String.fromCharCode(0xFEFF) + "Days of Work");
        row.push(String.fromCharCode(0xFEFF) + "Start_Date");
        return row
    }

    getAllTasks() {
        var response_data;
        $.ajax({
            url: all_tasks_api,
            type: "GET",
            async: false,
        })
        .done(function (response) {
            response_data = response;
        })
        .fail(function () {
            alert("failed to load the data at the server , Something wend Wrong... talk with tomer");
        });
        return response_data;
    }

    taskWithDetailsCSV() {
        const file_name = "SimpleTask.csv";
        let csv = this.addTaskDetailstoCSV();
        csv = this.exportTableToCSV(csv);
        this.downloadCSV(csv, file_name);
    }

    addTaskDetailstoCSV() {
        let row = [], csv = [];
        csv.push(this.taskPropertiesRow(csv).join(","));
        row.push(String.fromCharCode(0xFEFF) + this.task_problem);
        row.push(String.fromCharCode(0xFEFF) + this.task_description);
        row.push(String.fromCharCode(0xFEFF) + this.task_days);
        row.push(String.fromCharCode(0xFEFF) + this.task_start_date);
        csv.push(row.join(","));
        while (row.length) { row.pop() };
        csv.push(row.join(","));
        return csv;
    }

    exportTableToCSV(csv) {
        let rows = document.querySelectorAll("table tr");
        for (let i = 0; i < rows.length; i++) {
            let row = [], cols = rows[i].querySelectorAll("td, th");

            for (let j = 0; j < cols.length - 1; j++)
                row.push(String.fromCharCode(0xFEFF) + cols[j].innerText);

            csv.push(row.join(","));
        }
        return csv.join("\n");
    }


    downloadCSV(csv, file_name) {
        let csvFile;
        let downloadLink;
        // CSV file can change it in the parameter on the function , See how i add it to the export buttom
        csvFile = new Blob([csv], { type: "text/csv;utf-8" });
        // Download link
        downloadLink = document.createElement("a");
        // File name
        downloadLink.download = file_name;
        // Create a link to the file
        downloadLink.href = window.URL.createObjectURL(csvFile);
        // Hide download link
        downloadLink.style.display = "none";
        // Add the link to DOM
        document.body.appendChild(downloadLink);
        // Click download link
        downloadLink.click();
    }

}

function makeCSV() {
    csv = new CSV_Creator();
    const task_details_input = document.getElementById("Task_With_Details").className;
    if (task_details_input.includes("active")) {
        csv.taskWithDetailsCSV();
    } else {
        csv.allTasks_CSV();
    }
    
}
