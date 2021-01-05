$(document).ready(function () {
    prepare_graph(months_list, quantity_list);

    $("#submit").on("click", function () {
        $("#submit").addClass("is-loading disabled");
        let start = $("#start_date");
        let end = $("#end_date");
        if (!validate_dates(start.val(), end.val())) {
            alert("End date cannot be greater than start date");
            start.val(start_date);
            end.val(end_date);
            $("#submit").removeClass("is-loading disabled");
        } else {
            $.ajax({
                url: "/get_transactions/?start_date=" + String(start.val()) + "&end_date=" + String(end.val()),
                type: "GET",

                success: function (data) {
                    $("#submit").removeClass("is-loading disabled");

                    let months_list = JSON.parse(data["months_list"]);
                    let quantity_list = JSON.parse(data["quantity_list"]);

                    if (months_list.length > 0 && quantity_list.length > 0) {
                        $("#main").removeClass("d-none");
                        $("#no-results").addClass("d-none");

                        prepare_graph(months_list, quantity_list);
                    } else {
                        $("#main").addClass("d-none");
                        $("#no-results").removeClass("d-none");
                    }
                },

                error: function (data) {
                    $("#submit").removeClass("is-loading disabled");
                    alert("An error occurred! Please try again!!");
                    location.reload();
                }
            });
        }
    });
});

function validate_dates(start, end) {
    return new Date(end) >= new Date(start);
}

function prepare_graph(months_list, quantity_list) {
    // based on prepared DOM, initialize echarts instance
    let myChart = echarts.init(document.getElementById('main'));


    // specify chart configuration item and data
    let option = {
        title: {
            text: "Purchases"
        },
        legend: [
            {
                data: ["Quantity"]
            }
        ],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        xAxis: [
            {
                type: 'category',
                data: months_list,
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                splitArea: {show: true}
            }
        ],
        series: [
            {
                name: 'Quantity',
                type: 'bar',
                data: quantity_list
            }
        ]
    };

    // use configuration item and data specified to show chart
    myChart.setOption(option, true);
}