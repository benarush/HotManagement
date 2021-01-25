function downloadCSV(csv, filename) {
    var csvFile;
    var downloadLink;


    // CSV file can change it in the parameter on the function , See how i add it to the export buttom
    csvFile = new Blob([csv], {type: "text/csv;utf-8"});

    // Download link
    downloadLink = document.createElement("a");

    // File name
    downloadLink.download = filename;

    // Create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);

    // Hide download link
    downloadLink.style.display = "none";

    // Add the link to DOM
    document.body.appendChild(downloadLink);

    // Click download link
    downloadLink.click();
}

function exportTableToCSV(api_data) {
    var csv = [];
    var rows = document.querySelectorAll("table tr");
    task_first_row = [];
    api_data.task;
    "task": {
        "id": 35,
        "problem": "ללכת לאכול בפארק",
        "days": 3,
        "description": "רעב רצחחחחחחחח חיייייייבבבב אוכלללללל",
        "date_created": "2021-01-20T20:35:26.623884Z",
        "email_attached_file": "/media/Emails_Files_Tasks/Ht.png",
        "start_date": "2021-01-21T22:35:00Z"
    },
    for (var i = 0; i < rows.length; i++) {
        var row = [];

        row.push(String.fromCharCode(0xFEFF) + cols.c1);
		row.push(String.fromCharCode(0xFEFF) + cols.c2);
		console.log(row);
        csv.push(row.join(","));
    }

    // Download CSV file
    downloadCSV(csv.join("\n"), filename);
}