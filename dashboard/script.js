$(document).ready(function() {
    const apiUrl = 'http://localhost:8000/sentiment-summary';

    $.get(apiUrl, function(data) {
        // Sentiment Score Chart
        $("#sentiment-chart").dxChart({
            dataSource: data,
            title: "Average Sentiment Scores by Group",
            series: [{
                argumentField: "group_name",
                valueField: "average_sentiment_score",
                type: "bar",
                name: "Average Sentiment"
            }],
            legend: {
                visible: true
            },
            export: {
                enabled: true
            }
        });

        // Volume Chart
        $("#volume-chart").dxChart({
            dataSource: data,
            title: "Total Volume by Issue Type",
            series: [{
                argumentField: "issue_type",
                valueField: "total_volume",
                type: "pie",
                label: {
                    visible: true,
                    connector: {
                        visible: true
                    }
                }
            }]
        });

        // Data Grid
        $("#grid-container").dxDataGrid({
            dataSource: data,
            columns: [
                "group_name",
                "issue_type",
                "total_sentiment_score",
                "average_sentiment_score",
                "total_volume",
                "priority",
                {
                    dataField: "threshold_met",
                    dataType: "boolean"
                },
                {
                    dataField: "created_at",
                    dataType: "datetime"
                }
            ],
            filterRow: { visible: true },
            searchPanel: { visible: true },
            groupPanel: { visible: true },
            export: {
                enabled: true
            },
            paging: {
                pageSize: 10
            },
            pager: {
                showPageSizeSelector: true,
                allowedPageSizes: [5, 10, 20]
            }
        });
    });
}); 