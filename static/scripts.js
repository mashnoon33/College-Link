// Variables
var prompt = $('#prompt')
var params = {
    adm_rate: [0, .35],
    sat_avg: [1, 1300],
    md_earn_wne_p10: [0, 70000],
    region_id: "None",
    actcmmid: [1, 28],
    costt4_a: [0, 45000],
    degree: 3,
    owner: "None"
}
var owner = ["#pub", "#priv", "#all"] // list of buttons
var degree = ["#ass", "#bac", "#grad"]
var table = document.getElementById("results");
var dropdown = $('.ui.dropdown.second')

// Constants
const encodeGetParams = p =>
    Object.entries(p).map(kv => kv.map(encodeURIComponent).join("=")).join("&");

// Intiate stuffs
$("#mytable").hide()
$('.ui.sidebar').sidebar({
    context: $('.bottom.segment')
})


/// TODO: CREATE A FUNCTION FOR DOING THE LOOPS

// Initializes all the buttons
$("#pub").on("click", function() {
    if ($("#pub").hasClass("positive")) {
        $("#pub").toggleClass("positive")
        params.owner = null
    } else {
        for (item of owner) {
            if ($(item).hasClass("positive")) {
                $(item).toggleClass("positive")
            }
        }
        $("#pub").toggleClass("positive")
        prompt.val("")
        params.owner = 1
    }
});

$("#priv").on("click", function() {
    if ($("#priv").hasClass("positive")) {
        $("#priv").toggleClass("positive")
        params.owner = null
    } else {
        for (item of owner) {
            if ($(item).hasClass("positive")) {
                $(item).toggleClass("positive")
            }
        }
        $("#priv").toggleClass("positive")
        prompt.val("")
        params.owner = 2
    }
});

$("#all").on("click", function() {
    if ($("#all").hasClass("positive")) {
        $("#all").toggleClass("positive")
    } else {
        for (item of owner) {
            if ($(item).hasClass("positive")) {
                $(item).toggleClass("positive")
            }
        }
        $("#all").toggleClass("positive")
        prompt.val("")
        params.owner = "None"
    }
});

$("#ass").on("click", function() {
    if ($("#ass").hasClass("positive")) {
        $("#ass").toggleClass("positive")
        params.degree = null
    } else {
        for (item of degree) {
            if ($(item).hasClass("positive")) {
                $(item).toggleClass("positive")
            }
        }
        $("#ass").toggleClass("positive")
        prompt.val("")
        params.degree = 2

    }
});

$("#bac").on("click", function() {
    if ($("#bac").hasClass("positive")) {
        $("#bac").toggleClass("positive")
        params.degree = null
    } else {
        for (item of degree) {
            if ($(item).hasClass("positive")) {
                $(item).toggleClass("positive")
            }
        }
        $("#bac").toggleClass("positive")
        prompt.val("")
        params.degree = 3

    }
});


$("#grad").on("click", function() {
    if ($("#grad").hasClass("positive")) {
        $("#grad").toggleClass("positive")
        params.degree = null
    } else {
        for (item of degree) {
            if ($(item).hasClass("positive")) {
                $(item).toggleClass("positive")
            }
        }
        $("#grad").toggleClass("positive")
        prompt.val("")
        params.degree = 4

    }
});


$("#search").on("click", function() {
    $("#welcome").hide()
    $("#mytable").show()
    $("#mytable > tbody").html("");

    if (params.degree == null) { // checks for null and safeguards agains incomplete queries
        alert("Select a degree before searching")
    } else if (params.owner == null) {
        alert("Select a Owndership before searching")
    } else if (prompt.val() != "") {
        search_by_name(prompt.val());
    } else {
        search();
    }
});

// Initialize the dropdown for regions
dropdown.dropdown({
    apiSettings: {
        url: 'http://perlman.mathcs.carleton.edu:' + api_port + '/regions/',
    },
    onChange: function(value, text) {
        prompt.val("")
        if (value != 10) {
            params.region_id = value
        } else {
            params.region_id = "None"
        }
    }
});


// Functions

function dynamicEvent() {
    var queryURL = 'http://perlman.mathcs.carleton.edu:' + api_port + '/school/?opeid=' + this.id
    $.getJSON(queryURL, function(data) {
        var logo = document.getElementById("logo");
        while (logo.firstChild) {
            logo.removeChild(logo.firstChild);
        }
        var img = document.createElement('img');
        img.src = "https://logo.clearbit.com/" + data["insturl"].toString().replace("www.", "")
        logo.appendChild(img);
        $("#name").text(data["name"])
        $("#location").text(data["city"] + ", " + data["state"])
        $("#adm_rate").text(Math.round(data["adm_rate"] * 100) + "% Acceptance Rate")

        // destroy previous stuffs
        var toDestroy = ["#sat_info", "#act_info", "#divr_info", "#major_info"]

        for (item of toDestroy) {
          $(item).empty()
        }


        //fetches the modified dictionary definition
        $.getJSON(link2Dict, function(dict) {
            //fetches the divs to then populate
            var field_sat = $("#sat_info")
            var field_act = $("#act_info")
            var field_divr = $("#divr_info")
            var field_major = $("#major_info")

            // loops through the JSON object and populates the modal with relevant information
            for (var key in data) {
                if (key.includes("sat")) {
                  if (data[key] != null) {
                      var number = data[key]
                  } else {
                      var number = "Not found"
                  }
                    field_sat.append("<p>" + dict[key.toUpperCase()] + " : " +number + "</p>")
                }

                if (key.includes("act")) {
                    if (data[key] != null) {
                        var number = data[key]
                    } else {
                        var number = "Not found"
                    }
                    field_act.append("<p>" + dict[key.toUpperCase()] + " : " + number + "</p>")
                }
                if (key.includes("ugds")) {
                    field_divr.append("<p>" + dict[key.toUpperCase()] + " : " + Math.round(data[key] * 100) + "%" + "</p>")
                }
                if (key.includes("pcip")) {
                    field_major.append("<p>" + dict[key.toUpperCase()] + " : " + Math.round(data[key] * 100) + "%" + "</p>")
                }

            }
        });
    });
    $('.ui.modal').modal({
        centered: false
    })
    $('.ui.modal').modal('show') // Shows the modal when the data is done loading
}


async function search() {
    $.getJSON("http://perlman.mathcs.carleton.edu:" + api_port + "/schools/?" + encodeGetParams(params), function(data) {
        populateResultTable(data)
    });
    $('table').tablesort()
}

async function search_by_name(name) {
    $.getJSON("http://perlman.mathcs.carleton.edu:" + api_port + "/schools/name/" + name, function(data) {
        populateResultTable(data)
    });
    $('table').tablesort()
}

function populateResultTable(data) {
    // takes the json response and populates the table of results
    for (item of data) {
        var row = table.insertRow(table.rows.length);
        var x = row.insertCell(0);
        var img = document.createElement('img');
        img.src = "https://logo.clearbit.com/" + item["insturl"].toString().replace("www.", "") + "?size=20"
        x.appendChild(img);
        row.insertCell(1).innerHTML = item["name"]
        row.insertCell(2).innerHTML = item["city"] + ", " + item["state"]
        row.insertCell(3).innerHTML = Math.round(item["adm_rate"] * 100) + "%"
        row.insertCell(4).innerHTML = item["sat_avg"]
        row.insertCell(5).innerHTML = item["actcmmid"]
        row.insertCell(6).innerHTML = item["costt4_a"]
        row.insertCell(7).innerHTML = item["md_earn_wne_p10"]
        var y = row.insertCell(8);
        var but = document.createElement('button');
        but.className = 'ui button'
        but.innerHTML = 'view'
        but.id = item["opeid"]
        y.appendChild(but);
        but.onclick = dynamicEvent;
    }
}

// Initialize the Ranges
$('#sat').range({
    min: 0,
    max: 1600,
    start: 1300,
    step: 10,

    function() {
        $self = $(this),
            firstVal = $self.range('get thumb value'),
            secVal = $self.range('get thumb value', 'second');
        $('#sat_score').html(secVal + " - " + firstVal);
    },

    onChange: function(value) {
        prompt.val("") // Resets the name input when the variables are used
        $self = $(this),
            firstVal = $self.range('get thumb value'),
            secVal = $self.range('get thumb value', 'second');
        $('#sat_score').html(secVal + " - " + firstVal);
        params.sat_avg = [secVal, firstVal]
    }
});

$('#act').range({
    min: 0,
    max: 36,
    start: 28,
    step: 1,
    function() {
        $self = $(this),
            firstVal = $self.range('get thumb value'),
            secVal = $self.range('get thumb value', 'second');
        $('#act_score').html(secVal + " - " + firstVal);
    },
    onChange: function(value) {
        prompt.val("")
        $self = $(this),
            firstVal = $self.range('get thumb value'),
            secVal = $self.range('get thumb value', 'second');
        $('#act_score').html(secVal + " - " + firstVal);
        params.actcmmid = [secVal, firstVal]

    }
});

$('#cost').range({
    min: 0,
    max: 100000,
    start: 45000,
    step: 1000,
    function() {
        $self = $(this),
            firstVal = $self.range('get thumb value'),
            secVal = $self.range('get thumb value', 'second');
        $('#cost_n').html(secVal + " - " + firstVal);
    },
    onChange: function(value) {
        prompt.val("")
        $self = $(this),
            firstVal = $self.range('get thumb value'),
            secVal = $self.range('get thumb value', 'second');
        $('#cost_n').html(secVal + " - " + firstVal);
        params.costt4_a = [secVal, firstVal]

    }
});

$('#salary').range({
    min: 0,
    max: 200000,
    start: 70000,
    step: 1000,
    function() {
        $self = $(this),
            firstVal = $self.range('get thumb value'),
            secVal = $self.range('get thumb value', 'second');
        $('#salary_n').html(secVal + " - " + firstVal);
    },
    onChange: function(value) {
        prompt.val("")
        $self = $(this),
            firstVal = $self.range('get thumb value'),
            secVal = $self.range('get thumb value', 'second');
        $('#salary_n').html(secVal + " - " + firstVal);
        params.md_earn_wne_p10 = [secVal, firstVal]

    }
});

$('#selective').range({
    min: 0,
    max: 100,
    start: 35,
    step: 1,
    function() {
        $self = $(this),
            firstVal = $self.range('get thumb value'),
            secVal = $self.range('get thumb value', 'second');
        $('#selective_n').html(secVal + " - " + firstVal);
    },
    onChange: function(value) {
        prompt.val("")
        $self = $(this),
            firstVal = $self.range('get thumb value'),
            secVal = $self.range('get thumb value', 'second');
        $('#selective_n').html(secVal + " - " + firstVal);
        params.adm_rate = [secVal / 100, firstVal / 100]

    }
});
