var reportGeneratorSpec = {
    buildReport: '{{ build_report_url }}',
    elementsGridDataUrl: '{{ row_data_url }}',
    newRowUrl: '{{ new_row_url }}',
    editRowUrl: '{{ edit_row_url }}',
    deleteRowUrl: '{{ delete_row_url }}'
};

reportGenerator.spec.setSpec(reportGeneratorSpec);
var reportGeneratorApp = reportGenerator.app();
reportGeneratorApp.startApp();